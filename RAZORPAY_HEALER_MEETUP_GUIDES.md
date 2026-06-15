# 💳 RAZORPAY INTEGRATION GUIDE

## Step 1: Get Razorpay Credentials

1. Visit https://razorpay.com/dashboard
2. Sign up / Login
3. Go to Settings → API Keys
4. Copy **Key ID** and **Key Secret**
5. Add to backend .env:
   ```
   RAZORPAY_KEY_ID=your_key_id
   RAZORPAY_KEY_SECRET=your_key_secret
   ```

---

## Step 2: Create Payment API Endpoint

Add to backend/app/routes/payments.py:

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import HealerSession, Subscription
from app.services.razorpay_service import RazorpayService
from app.routes.users import get_current_user
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class CreateOrderRequest(BaseModel):
    amount: int  # in paise (₹100 = 10000 paise)
    type: str  # "healer_session" or "premium_subscription"
    item_id: int  # session_id or subscription_id

@router.post("/create-order")
async def create_order(
    request: CreateOrderRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create Razorpay order for payment"""
    
    # Verify item exists and belongs to user
    if request.type == "healer_session":
        session = db.query(HealerSession).filter(
            HealerSession.id == request.item_id,
            HealerSession.user_id == current_user.id
        ).first()
        
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        description = f"Healer Session: {session.healer.name}"
    
    elif request.type == "premium_subscription":
        # Amount should be ₹299 * 100 = 29900 paise
        description = "Premium Subscription - 1 Month"
    
    else:
        raise HTTPException(status_code=400, detail="Invalid type")
    
    # Create Razorpay order
    order_response = RazorpayService.create_order(
        amount=request.amount,
        receipt=f"{request.type}_{request.item_id}",
        description=description,
        customer_notify=1
    )
    
    if not order_response['success']:
        raise HTTPException(status_code=500, detail="Failed to create order")
    
    return {
        "order_id": order_response['order_id'],
        "amount": order_response['amount'],
        "currency": order_response['currency'],
        "key_id": os.getenv("RAZORPAY_KEY_ID")  # Frontend needs this
    }

class VerifyPaymentRequest(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str
    type: str  # "healer_session" or "premium_subscription"
    item_id: int

@router.post("/verify-payment")
async def verify_payment(
    request: VerifyPaymentRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Verify Razorpay payment and update database"""
    
    # Verify signature
    is_valid = RazorpayService.verify_payment(
        request.razorpay_order_id,
        request.razorpay_payment_id,
        request.razorpay_signature
    )
    
    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid payment signature")
    
    # Update database based on type
    if request.type == "healer_session":
        session = db.query(HealerSession).filter(
            HealerSession.id == request.item_id,
            HealerSession.user_id == current_user.id
        ).first()
        
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session.razorpay_payment_id = request.razorpay_payment_id
        session.payment_status = "completed"
        session.status = "confirmed"
        
        db.commit()
        
        return {
            "success": True,
            "message": "Payment successful! Your healer session is confirmed.",
            "session_id": session.id
        }
    
    elif request.type == "premium_subscription":
        # Create subscription record
        subscription = Subscription(
            user_id=current_user.id,
            plan="premium",
            amount=299,
            status="active",
            razorpay_subscription_id=request.razorpay_order_id,
            razorpay_payment_id=request.razorpay_payment_id,
            payment_status="completed"
        )
        
        db.add(subscription)
        db.commit()
        db.refresh(subscription)
        
        return {
            "success": True,
            "message": "Welcome to Premium! Enjoy unlimited meetups & healer discounts.",
            "subscription_id": subscription.id
        }
```

---

## Step 3: Frontend Payment Implementation

Add to frontend/src/pages/Premium.jsx:

```jsx
import React, { useState } from 'react';
import { paymentAPI } from '../services/api';

export default function Premium() {
  const [loading, setLoading] = useState(false);

  const handleSubscribe = async () => {
    setLoading(true);
    try {
      // Step 1: Create order
      const orderResponse = await paymentAPI.createOrder(
        29900,  // ₹299 in paise
        "Premium Subscription"
      );

      // Step 2: Open Razorpay checkout
      const options = {
        key: orderResponse.data.key_id,  // From backend
        amount: orderResponse.data.amount,
        currency: orderResponse.data.currency,
        order_id: orderResponse.data.order_id,
        handler: async (response) => {
          // Step 3: Verify payment
          const verifyResponse = await paymentAPI.verifyPayment({
            razorpay_order_id: response.razorpay_order_id,
            razorpay_payment_id: response.razorpay_payment_id,
            razorpay_signature: response.razorpay_signature,
            type: "premium_subscription",
            item_id: 0  // Not used for subscription
          });

          if (verifyResponse.data.success) {
            alert('✅ ' + verifyResponse.data.message);
            // Redirect to account page
            window.location.href = '/account';
          }
        },
        prefill: {
          name: "User Name",
          email: "user@example.com",
          contact: "9876543210"
        },
        notes: {
          project_name: "SoulConnect"
        },
        theme: {
          color: "#7c3aed"
        }
      };

      const rzp = new window.Razorpay(options);
      rzp.open();
    } catch (error) {
      alert('Payment failed: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Upgrade to Premium</h1>

      <div className="bg-purple-600 text-white rounded-lg p-8">
        <h2 className="text-2xl font-bold mb-4">Premium - ₹299/month</h2>
        
        <ul className="space-y-2 mb-6">
          <li>✓ Priority matching (10 min)</li>
          <li>✓ Unlimited meetups</li>
          <li>✓ 20% healer discounts</li>
          <li>✓ Expanded search radius</li>
          <li>✓ Progress tracking</li>
          <li>✓ Ad-free experience</li>
        </ul>

        <button
          onClick={handleSubscribe}
          disabled={loading}
          className="w-full bg-white text-purple-600 py-3 rounded-lg font-bold hover:bg-gray-100 disabled:opacity-50"
        >
          {loading ? 'Processing...' : 'Subscribe Now'}
        </button>
      </div>
    </div>
  );
}
```

Add Razorpay script to index.html:

```html
<!-- In <head> -->
<script src="https://checkout.razorpay.com/v1/checkout.js"></script>
```

---

## Step 4: Test Payment

### Test Credentials (Razorpay Sandbox)

Use these for testing WITHOUT actual payment:
- Card: 4111 1111 1111 1111
- Expiry: Any future date
- CVV: Any 3 digits

### Test Payment Flow

1. Click "Subscribe Now"
2. Razorpay modal opens
3. Enter test card details
4. Click "Pay ₹299"
5. Payment processes (in test mode)
6. See confirmation on website

---

# 👨‍⚕️ HEALER ONBOARDING TEMPLATE

## Email to Send to Healers (Copy & Send)

---

### Subject: SoulConnect - Join Our Verified Healer Network

Dear [Healer Name],

I'm reaching out because I'm building **SoulConnect**, a platform connecting people dealing with emotional/spiritual challenges with verified, trusted healers.

**What We're Looking For:**
Pranic healers, energy workers, spiritual counselors who want to help people heal while building a sustainable practice.

**Why Join SoulConnect?**
- ✅ Pre-screened, verified client pipeline
- ✅ Flexible scheduling (set your own hours)
- ✅ Keep 75% of session fees (we take 25% platform fee)
- ✅ Build reviews & reputation on platform
- ✅ Reach people actively seeking help
- ✅ No upfront fees or commitments

**How It Works:**
1. You register (name, phone, specializations, rate)
2. We verify your credentials
3. Your profile goes live
4. Users book sessions with you
5. You deliver healing via video/voice/chat
6. You get paid directly (75% of session amount)

**What We Need From You:**

To register, please reply with:
1. Your full name
2. Phone number
3. Email address
4. What problems do you specialize in? (choose from: Breakup Healing, Anxiety Release, Chakra Balancing, Trauma Release, Confidence Building, Energy Clearing, etc.)
5. Your hourly rate (₹500-₹2000 recommended)
6. Years of experience
7. Brief bio (what do you offer?)
8. Link to your certification/credentials PDF (Google Drive link, etc.)

**Example:**
```
Name: Pooja Sharma
Phone: 9876543210
Email: pooja@example.com
Specializations: Breakup Healing, Heart Chakra Balancing, Emotional Release
Rate: ₹800/hour
Experience: 5 years
Bio: "I specialize in healing heartbreak and emotional wounds using Pranic healing techniques. I help clients release stored pain and rebuild confidence."
Certification: https://drive.google.com/file/d/... (link to PDF)
```

**Timeline:**
- Upon registration: Your profile submitted for verification
- Within 48 hours: We verify your credentials
- Once verified: Your profile goes live, users can book!

**Questions?**
Reply to this email or call me at [Your Phone]

Looking forward to having you on the platform!

Warm regards,
[Your Name]
SoulConnect Founder
[Your Phone]

---

# 🤝 MEETUP COORDINATOR PLAYBOOK

## What is a Meetup?

Weekly in-person gathering (1-1.5 hours) for 6-8 people dealing with the **same problem** (breakup, anxiety, marriage issues, etc.) to connect, share strategies, and support each other.

---

## Before the Meetup

### 1. Choose Your Problem & Time
- Pick problem: Breakup, Anxiety, Marriage Problems, Loneliness, etc.
- Pick day/time: Same day every week (e.g., Monday 7pm)
- Pick location: Café, park, coworking space (free/cheap)

### 2. Create Meetup Event (In SoulConnect App)
```
Title: "Breakup Support Circle - Chembur"
Problem: Relationship Breakup
Location: Café Coffee Day, Chembur
Date/Time: Monday 7:00 PM - 8:30 PM
Max Attendees: 8
Description: "Come talk with others healing from breakup. Share your journey, get advice, make friends. No judgment, just support."
```

### 3. Prepare (Day Before)
- [ ] Confirm venue has space for 6-8 people
- [ ] If food: Order snacks/order from café menu
- [ ] Test location WiFi (if using video for anyone who joins remotely)
- [ ] Create simple agenda:
  - Intro round (5 min): Names, how long in recovery
  - Share/discuss (45 min): Open conversation
  - Resources/tips (20 min): Share what's helped
  - Exchange contacts (10 min): Optional, people who want to stay in touch

---

## During the Meetup

### Opening (5 min)
```
"Hi everyone, welcome to Breakup Support Circle! 

I'm [Name]. This is a safe space where we all share the same experience - healing from breakup. No judgment, no lectures. Just people who get it.

Quick intro: What's your name, and how long since your breakup?"
```

### Facilitation Tips
- Listen more than you talk
- If someone gets deep: "That's important. Want to talk about it?" or "How are you handling that?"
- If someone dominates: "Thanks for sharing. Let's hear from [person] next."
- If awkward silence: Ask specific question: "What's one thing that helped you this week?"
- Be empathetic but not therapeutic (you're peer support, not therapist)

### Topics You Can Bring Up
**Breakup Circle:**
- How to stop checking their social media
- When to reach out vs. when to stay silent
- Dealing with seeing them with someone new
- Rebuilding your life
- When you'll be ready to date again
- Red flags to avoid next time

**Anxiety Circle:**
- What triggers your anxiety
- What helps you calm down (breathing, exercise, talking)
- How anxiety affects your relationships/work
- Therapy vs. self-help approaches
- Medication experiences (if comfortable)

---

## After the Meetup

### Immediate (Same Day)
- [ ] Thank everyone for coming
- [ ] Ask: "Rate this meetup 1-5 stars"
- [ ] Ask: "Would you come again?"
- [ ] Collect feedback: "Anything we should do differently?"

### Within 24 Hours
- [ ] Enter ratings in SoulConnect app
- [ ] Send follow-up message to attendees:
  ```
  "Hi everyone,
  
  Thanks so much for coming last night. I loved the conversation - especially when [person] shared [topic]. 
  
  If anyone wants to stay in touch, feel free to exchange numbers (optional).
  
  Same time next week! See you Monday 7pm at the café.
  
  [Your name]"
  ```

### Monthly Review
- [ ] How many attendees on average? (goal: 6-8)
- [ ] What's the feedback? (positive, suggestions)
- [ ] Is the time/location working?
- [ ] Do attendees keep coming? (retention = success)

---

## Scaling Model

### Phase 1: Manual (Weeks 1-4)
- You personally host 1 meetup/week
- Location: 1 café/park
- Problem: 1 issue (start with Breakup)
- Time: 2-3 hours setup + facilitation

### Phase 2: Expand (Weeks 5-12)
- Add 2nd problem (Anxiety)
- Add 2nd location/time slot
- You still facilitate all

### Phase 3: Train Leaders (Month 3+)
- Find 2-3 enthusiastic attendees
- Train them to facilitate next week
- You pay them ₹500-1000 per meetup
- You expand to 6+ meetups/week

### Revenue at Phase 3
```
8 meetups/week × 6 people × ₹199 per meetup = ₹9,500/week
OR (if premium model): 200 premium subscribers × ₹299/month = ₹60,000/month
```

---

## Troubleshooting

**No one showed up:**
- Maybe wrong time/location
- Maybe need better marketing
- Try different day/time next week
- Post in app: "Meetup is on! Come join"

**Too many people (>8):**
- Great! Next week, create 2nd session at different time
- Keep groups intimate (6-8 is sweet spot)

**People aren't opening up:**
- Share something personal first (breaks the ice)
- Ask specific questions, not vague ones
- Give people permission: "If anyone wants to share something deep..."

**Person dominating conversation:**
- Gently: "Thanks for that. [Other person], your turn?"
- In private: "You're great. Could help others share too?"

**Awkward tension:**
- Pivot to lighter topic: "So what's helped you this week?"
- Take 2-min break (bathroom/coffee)
- Change activity (move to different spot, stand instead of sit)

---

## Sample Meetup Scripts

### Opening Script (Breakup)
```
"Hi everyone, welcome to Breakup Support Circle!

I'm [Name], and I started these meetups because I know how lonely a breakup can feel. You think everyone else is fine, but you're here - so you're not alone.

This is a completely safe space. What you share stays here. No judgment. No 'get over it' advice. Just people who actually understand what you're going through.

Super casual - we'll just talk, share what's helped us, maybe exchange numbers if we vibe.

Let's go around: Name, and how long since your breakup?"
```

### Middle Script (When Conversation Lags)
```
"So real question - and feel free to pass - but when did you start feeling a tiny bit better after the breakup? Like, not 100%, but maybe a moment where you weren't thinking about them?"
```

### Closing Script
```
"Thanks so much everyone. Seriously.

Before we go - quick rating: How was this on a scale of 1-5? [Get feedback]

If anyone wants to stay in touch, you can exchange numbers - totally optional, no pressure.

Same time next week! [Day] at [Time] at [Location].

You're all going to be okay."
```

---

## Marketing Your Meetup

1. **In-App Notification** - SoulConnect shows upcoming meetups
2. **Word of Mouth** - Attendees tell friends
3. **Problem-Specific Communities** (if added later) - Post in Breakup community
4. **Social Media** - Instagram posts with testimonials
5. **Local Groups** - WhatsApp groups for your city

Example post:
```
"🌟 Breakup Support Circle 
Monday 7pm | Chembur Café
6 people healing together

You're not alone. Join us. 💔→💪

[Link to sign up]"
```

---

**Remember:** The goal isn't perfection. It's creating a space where people feel less alone. If even 1 person leaves saying "I felt heard," you've won.

Now go build community! 🤝
