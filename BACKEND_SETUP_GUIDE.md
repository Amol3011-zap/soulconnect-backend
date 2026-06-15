# 🚀 SOULCONNECT BACKEND - COMPLETE SETUP GUIDE

## STEP 1: Local Development Setup

### Create Project Structure

```bash
mkdir soulconnect-backend
cd soulconnect-backend

# Create folders
mkdir app
mkdir app/routes
mkdir app/services
mkdir tests

# Create files
touch app/__init__.py
touch app/main.py
touch app/models.py
touch app/config.py
touch app/database.py
touch requirements.txt
touch .env.example
touch Procfile
```

### Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose bcrypt python-multipart python-dotenv razorpay geopy redis

pip freeze > requirements.txt
```

### Create .env File

```bash
# Copy from .env.example
cp .env.example .env
```

### .env Template

```
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/soulconnect

# Security
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=43200

# Razorpay
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_key_secret

# Email (SendGrid)
SENDGRID_API_KEY=your_sendgrid_api_key
SENDGRID_FROM_EMAIL=noreply@soulconnect.com

# Google Maps
GOOGLE_MAPS_API_KEY=your_google_maps_api_key

# Redis
REDIS_URL=redis://localhost:6379

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,https://soulconnect.com

# App
DEBUG=False
PORT=8000
```

### Create requirements.txt

```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
python-jose==3.3.0
python-multipart==0.0.6
bcrypt==4.1.1
python-dotenv==1.0.0
razorpay==1.3.0
geopy==2.4.0
redis==5.0.1
pydantic==2.5.0
httpx==0.25.2
```

### Database Setup (Local PostgreSQL)

```bash
# Install PostgreSQL (if not already installed)
# macOS: brew install postgresql@15
# Ubuntu: sudo apt-get install postgresql postgresql-contrib
# Windows: Download from postgresql.org

# Start PostgreSQL
sudo service postgresql start  # Linux
brew services start postgresql  # macOS

# Create database
sudo -u postgres psql
CREATE DATABASE soulconnect;
CREATE USER soulconnect_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE soulconnect TO soulconnect_user;
\q
```

### Test Local Setup

```bash
# Run the app
python -m uvicorn app.main:app --reload

# You should see:
# INFO:     Uvicorn running on http://127.0.0.1:8000
# Visit http://localhost:8000/docs for API documentation
```

---

## STEP 2: Razorpay Setup

### Create Razorpay Account

1. Go to https://razorpay.com
2. Sign up with email
3. Verify email
4. Complete KYC (if in India)
5. Go to Settings → API Keys
6. Copy Key ID and Key Secret
7. Add to `.env`:
   ```
   RAZORPAY_KEY_ID=your_key_id
   RAZORPAY_KEY_SECRET=your_key_secret
   ```

### Test Razorpay Integration

```python
# In Python shell
import razorpay
from app.config import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

# Create test order
order = client.order.create({
    "amount": 50000,  # ₹500
    "currency": "INR",
    "receipt": "receipt#1",
    "notes": {
        "project_name": "SoulConnect"
    }
})

print(order)  # Should show order details
```

---

## STEP 3: Healer Onboarding

### Create Healer Admin Endpoint (Add to routes/admin.py)

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Healer, ProblemEnum
from pydantic import BaseModel

router = APIRouter()

class HealerRegistrationRequest(BaseModel):
    name: str
    phone: str
    email: str
    specializations: list  # List of ProblemEnum values
    hourly_rate: int  # ₹500-2000
    bio: str
    experience_years: int
    certification_url: str  # URL to PDF

@router.post("/healers/register")
async def register_healer(
    request: HealerRegistrationRequest,
    db: Session = Depends(get_db)
):
    """Register new healer (sends email to admin for verification)"""
    
    # Check if healer already exists
    existing = db.query(Healer).filter(Healer.phone == request.phone).first()
    if existing:
        raise HTTPException(status_code=400, detail="Healer already registered")
    
    # Create healer (not verified yet)
    healer = Healer(
        name=request.name,
        phone=request.phone,
        email=request.email,
        specializations=request.specializations,
        hourly_rate=request.hourly_rate,
        bio=request.bio,
        experience_years=request.experience_years,
        certification_url=request.certification_url,
        is_verified=False  # Manual verification by admin
    )
    
    db.add(healer)
    db.commit()
    db.refresh(healer)
    
    # TODO: Send email to admin for verification
    # send_email_to_admin(healer)
    
    return {
        "message": "Registration submitted. Verification pending.",
        "healer_id": healer.id
    }

@router.post("/healers/{healer_id}/verify")
async def verify_healer(
    healer_id: int,
    db: Session = Depends(get_db)
):
    """Admin endpoint to verify healer"""
    
    healer = db.query(Healer).filter(Healer.id == healer_id).first()
    
    if not healer:
        raise HTTPException(status_code=404, detail="Healer not found")
    
    healer.is_verified = True
    healer.verified_at = datetime.utcnow()
    db.commit()
    
    return {"message": f"{healer.name} is now verified!"}
```

### Manual Verification Process

1. Healer signs up with:
   - Name, phone, email
   - Specializations (problems they treat)
   - Hourly rate (₹500-2000)
   - Experience years
   - Certification URL (PDF link)

2. Email notification sent to admin (you)
3. You review certification
4. If valid: Verify healer in admin panel
5. Healer now visible to users

---

## STEP 4: Railway Deployment

### Create Railway Account

1. Go to https://railway.app
2. Sign up with GitHub
3. Create new project

### Deploy Backend

```bash
# 1. Create requirements.txt (already done)

# 2. Create Procfile
echo "web: uvicorn app.main:app --host 0.0.0.0 --port \$PORT" > Procfile

# 3. Create .railwayignore (optional)
echo "venv/" > .railwayignore
echo ".env" >> .railwayignore

# 4. Push to GitHub (required by Railway)
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/soulconnect-backend.git
git push -u origin main

# 5. In Railway dashboard:
# - Click "New Project"
# - Select GitHub repo
# - Configure environment variables (copy from .env)
# - Click "Deploy"
```

### Configure Railway Environment Variables

In Railway Dashboard:
1. Go to Variables
2. Add each variable from .env:
   - DATABASE_URL (Railway will provide PostgreSQL)
   - SECRET_KEY
   - RAZORPAY_KEY_ID
   - RAZORPAY_KEY_SECRET
   - Etc.

### Railway Database Setup

1. In Railway Dashboard → Plugins
2. Add PostgreSQL
3. Copy DATABASE_URL to environment variables
4. Deploy

---

## STEP 5: Production Checklist

- [ ] Change SECRET_KEY to random string
- [ ] Set DEBUG=False
- [ ] Set ALLOWED_ORIGINS correctly
- [ ] Verify Razorpay keys are correct
- [ ] Test database connection
- [ ] Test email sending (SendGrid)
- [ ] Test Google Maps API
- [ ] Set up HTTPS (Railway auto-includes)
- [ ] Set up database backups
- [ ] Monitor logs via Railway dashboard
- [ ] Test all API endpoints with production URL

### Test Production Endpoints

```bash
# Get health
curl https://your-api.railway.app/health

# Signup test
curl -X POST https://your-api.railway.app/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "9876543210",
    "name": "Test User",
    "primary_problem": "anxiety",
    "latitude": 19.0176,
    "longitude": 72.8479,
    "address": "Mumbai",
    "city": "Mumbai"
  }'
```

---

## Troubleshooting

### Database Connection Error

```
ERROR: could not translate host name "localhost" to address: nodename nor servname provided
```

**Solution:** Change DATABASE_URL to Railway PostgreSQL URL

### Razorpay Error

```
unauthorized: Invalid API Key
```

**Solution:** Verify RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET are correct

### CORS Error

```
Access to XMLHttpRequest blocked by CORS policy
```

**Solution:** Add frontend URL to ALLOWED_ORIGINS in .env

### Port Already in Use

```
OSError: [Errno 48] Address already in use
```

**Solution:** 
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

---

## Monitoring

### View Logs

```bash
# Railway CLI (if installed)
railway logs

# Or in Railway Dashboard → Logs
```

### Monitor Errors

Set up Sentry.io for error tracking:

```python
# In app/main.py
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0
)
```

---

## Next Steps

1. ✅ Backend deployed
2. 🔄 Deploy frontend (see FRONTEND_SETUP_GUIDE.md)
3. 🔄 Set up healer onboarding
4. 🔄 Launch to beta users
