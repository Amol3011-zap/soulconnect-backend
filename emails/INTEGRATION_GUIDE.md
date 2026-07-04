# SoulConnect Email Integration Guide

Complete guide for integrating React Email components with existing FastAPI backend.

## Architecture Overview

```
Frontend (Next.js/React)
    ↓
API Route (Node.js)
    ↓
Resend Service
    ↓
Email Delivered
```

OR

```
Backend (FastAPI/Python)
    ↓
Render Email Component (via subprocess/API)
    ↓
Resend Service
    ↓
Email Delivered
```

## Option 1: Next.js API Route (Recommended)

### Setup

1. Create email in Next.js project:

```bash
npm install react-email resend
```

2. Add API route at `app/api/emails/welcome/route.ts`:

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { Resend } from 'resend';
import { WelcomeEmail } from '@/emails/WelcomeEmail';

const resend = new Resend(process.env.RESEND_API_KEY);

export async function POST(request: NextRequest) {
  try {
    const { userEmail, userName } = await request.json();

    const data = await resend.emails.send({
      from: 'SoulConnect <community@soulconnect.health>',
      to: userEmail,
      subject: userName
        ? `💜 Welcome to SoulConnect, ${userName.split(' ')[0]}`
        : '💜 Welcome to SoulConnect',
      react: <WelcomeEmail userEmail={userEmail} userName={userName} />,
    });

    return NextResponse.json(data);
  } catch (error) {
    console.error('Email send error:', error);
    return NextResponse.json({ error: 'Failed to send email' }, { status: 500 });
  }
}
```

3. Call from FastAPI backend:

```python
import httpx

async def send_welcome_email(user_email: str, user_name: str):
    """Send welcome email via Next.js API"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://your-next-app.com/api/emails/welcome",
                json={
                    "userEmail": user_email,
                    "userName": user_name
                },
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        print(f"Error sending welcome email: {e}")
        return {"error": str(e)}
```

## Option 2: Python Subprocess (Node.js Module)

### Setup

1. Create rendering script `render-email.js`:

```javascript
// render-email.js
import { render } from '@react-email/render';
import { WelcomeEmail } from './emails/WelcomeEmail.js';

const args = process.argv.slice(2);
const userEmail = args[0];
const userName = args[1];

async function renderEmail() {
  const html = await render(
    <WelcomeEmail userEmail={userEmail} userName={userName} />
  );
  console.log(html);
}

renderEmail().catch(console.error);
```

2. Python wrapper:

```python
import subprocess
import json
from typing import Tuple

def render_welcome_email(user_email: str, user_name: str) -> str:
    """Render React Email component to HTML"""
    try:
        result = subprocess.run(
            ["node", "render-email.js", user_email, user_name],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            raise RuntimeError(f"Rendering failed: {result.stderr}")
        
        return result.stdout.strip()
    except Exception as e:
        print(f"Error rendering email: {e}")
        raise

async def send_welcome_email(user_email: str, user_name: str):
    """Send welcome email via Resend"""
    from resend import Resend
    
    # Render HTML
    html = render_welcome_email(user_email, user_name)
    
    # Send via Resend
    client = Resend(api_key="your-resend-key")
    
    first_name = user_name.split()[0] if user_name else "there"
    subject = f"💜 Welcome to SoulConnect, {first_name}" if user_name else "💜 Welcome to SoulConnect"
    
    try:
        response = client.emails.send({
            "from": "SoulConnect <community@soulconnect.health>",
            "to": user_email,
            "subject": subject,
            "html": html
        })
        return response
    except Exception as e:
        print(f"Error sending email: {e}")
        raise
```

## Option 3: Python Resend Client (Easiest)

### Setup

1. Install Resend Python SDK:

```bash
pip install resend
```

2. Use Resend's built-in HTML support:

```python
from resend import Resend
from datetime import datetime

async def send_welcome_email_simple(user_email: str, user_name: str = None):
    """Send welcome email with pre-rendered HTML"""
    
    client = Resend(api_key="your-resend-key")
    
    # Use pre-rendered static HTML
    html = get_welcome_email_html(user_name)
    
    first_name = user_name.split()[0] if user_name else "there"
    subject = f"💜 Welcome to SoulConnect, {first_name}" if user_name else "💜 Welcome to SoulConnect"
    
    try:
        response = client.emails.send({
            "from": "SoulConnect <community@soulconnect.health>",
            "to": user_email,
            "subject": subject,
            "html": html
        })
        print(f"Email sent: {response}")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def get_welcome_email_html(user_name: str = None) -> str:
    """
    Return pre-rendered welcome email HTML.
    This would be your compiled React Email output.
    """
    first_name = user_name.split()[0] if user_name else "there"
    
    # This is the compiled HTML from React Email
    # You would generate this once and cache it, or render on-demand
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Welcome to SoulConnect</title>
        <style>
            /* Your CSS here */
        </style>
    </head>
    <body>
        <!-- Your email markup here, with {first_name} interpolated -->
    </body>
    </html>
    """
```

## FastAPI Integration Example

### Using with Early Access Endpoint

Update your existing endpoint to use new email:

```python
from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from datetime import datetime
import httpx

router = APIRouter()

@router.post("/api/early-access/")
async def create_early_access(email: str, name: str = None, struggle: str = None):
    """
    Create early access entry and send welcome email
    """
    from resend import Resend
    
    # Check for duplicates
    stmt = select(EarlyAccess).where(EarlyAccess.email == email)
    existing = await db.execute(stmt)
    
    if existing.scalar():
        return {
            "success": True,
            "message": "You're already on the SoulConnect waitlist 💜"
        }
    
    try:
        # Create database entry
        entry = EarlyAccess(
            email=email,
            name=name,
            struggle=struggle,
            created_at=datetime.utcnow()
        )
        db.add(entry)
        await db.commit()
        
        # Send welcome email
        client = Resend(api_key=os.getenv("RESEND_API_KEY"))
        
        # Get pre-rendered HTML
        html = render_welcome_email(email, name)
        
        # Send email
        client.emails.send({
            "from": "SoulConnect <community@soulconnect.health>",
            "to": email,
            "subject": f"💜 Welcome to SoulConnect, {name.split()[0]}" if name else "💜 Welcome to SoulConnect",
            "html": html
        })
        
        # Send admin notification
        send_admin_notification(email, name, struggle)
        
        return {
            "success": True,
            "message": "Welcome to SoulConnect! 💜"
        }
        
    except Exception as e:
        print(f"Error: {e}")
        # Still success if email fails - don't block signup
        return {
            "success": True,
            "message": "Welcome to SoulConnect! 💜"
        }
```

## Environment Variables

### .env.production

```bash
# Resend API Key
RESEND_API_KEY=re_xxxxxx

# Email Configuration
EMAIL_FROM=SoulConnect <community@soulconnect.health>
EMAIL_ADMIN=admin@soulconnect.health
EMAIL_SUPPORT=support@soulconnect.health
```

### Railway Deployment

1. Add to Railway environment variables:
   - `RESEND_API_KEY` = your API key

2. Ensure Node.js modules are available if using subprocess approach

## Testing

### Test Email Sending

```python
import asyncio

async def test_send_email():
    from fastapi import FastAPI
    
    app = FastAPI()
    
    result = await send_welcome_email(
        user_email="test@example.com",
        user_name="Amol Londhe"
    )
    
    print(f"Email sent: {result}")

# Run test
asyncio.run(test_send_email())
```

### Check Rendered HTML

```bash
# Using Node.js
node render-email.js test@example.com "Amol Londhe"

# Or in Python
from render_email import render_welcome_email
html = render_welcome_email("test@example.com", "Amol Londhe")
print(html)
```

## Deployment Steps

### 1. Create React Email Components

```bash
mkdir emails
cp WelcomeEmail.tsx emails/
cp -r components emails/
cp -r helpers emails/
```

### 2. For Next.js Approach

```bash
npm install react-email resend
# Create API route
# Deploy to Vercel
```

### 3. For Python Approach

```bash
pip install resend

# Add render-email.js to repository
# Update FastAPI endpoints
# Deploy to Railway
```

### 4. Environment Setup

Add to Railway:
- `RESEND_API_KEY`

### 5. Test Before Production

```bash
# Test locally
python test_email.py

# Monitor Resend dashboard
# Check email client rendering
# Verify dark mode
```

## Troubleshooting

### Email Not Sending

1. Check `RESEND_API_KEY` is set correctly
2. Verify email domain is configured in Resend
3. Check email address format is valid
4. Look for rate limiting (Resend free tier: 100/day)

### HTML Not Rendering

1. Verify subprocess is working: `node render-email.js`
2. Check Node.js is installed on server
3. Verify dependencies are in package.json
4. Test HTML rendering locally

### Styling Not Showing

1. Inline CSS is used (not external stylesheets)
2. Some email clients strip certain CSS properties
3. Test in Litmus or Email on Acid
4. Use `!important` for critical styles if needed

### Dark Mode Not Working

1. Verify `@media (prefers-color-scheme: dark)` is in styles
2. Test in Gmail dark mode
3. Check email client dark mode support
4. May need explicit color overrides

## Performance Optimization

### Caching

```python
# Cache rendered HTML
from functools import lru_cache

@lru_cache(maxsize=100)
def get_welcome_email_html_cached(user_name: str = None) -> str:
    return render_welcome_email_html(user_name)
```

### Batch Sending

```python
async def send_batch_emails(emails: List[Dict]):
    """Send multiple emails efficiently"""
    client = Resend(api_key=os.getenv("RESEND_API_KEY"))
    
    for email_data in emails:
        html = render_welcome_email(
            email_data["email"],
            email_data["name"]
        )
        
        client.emails.send({
            "from": "SoulConnect <community@soulconnect.health>",
            "to": email_data["email"],
            "subject": f"💜 Welcome to SoulConnect",
            "html": html
        })
        
        await asyncio.sleep(0.1)  # Rate limiting
```

## Monitoring

### Setup Email Monitoring

```python
def log_email_sent(email: str, name: str, status: str):
    """Log email sends for monitoring"""
    print(f"[EMAIL] To: {email} | Name: {name} | Status: {status}")
    
    # Store in database for analytics
    db.email_logs.insert({
        "email": email,
        "name": name,
        "status": status,
        "timestamp": datetime.utcnow()
    })
```

### Check Resend Dashboard

- https://resend.com/emails
- Monitor open rates
- Check bounce/spam rates
- View email logs

## Next Steps

1. Choose integration approach (Next.js, subprocess, or direct Python)
2. Set up environment variables
3. Test email sending locally
4. Deploy to production
5. Monitor email deliverability
6. Iterate on design based on feedback

## Support Resources

- React Email Docs: https://react.email/docs
- Resend Docs: https://resend.com/docs
- Python Resend: https://github.com/resendlabs/resend-python