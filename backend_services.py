# backend/app/config.py
# Configuration and Database Setup

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# ========== DATABASE CONFIGURATION ==========

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost:5432/soulconnect"
)

engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL logging
    pool_pre_ping=True,  # Verify connection before use
    pool_recycle=3600  # Recycle connections every hour
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ========== SECURITY CONFIGURATION ==========

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 24 * 60  # 30 days

# ========== RAZORPAY CONFIGURATION ==========

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "")

# ========== CORS CONFIGURATION ==========

ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://localhost:5173,https://soulconnect.com"
).split(",")

# ========== EMAIL CONFIGURATION ==========

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")
SENDGRID_FROM_EMAIL = os.getenv("SENDGRID_FROM_EMAIL", "noreply@soulconnect.com")

# ========== GOOGLE MAPS CONFIGURATION ==========

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")

# ========== REDIS CONFIGURATION ==========

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# ========== APP SETTINGS ==========

APP_NAME = "SoulConnect"
APP_VERSION = "1.0.0"
DEBUG = os.getenv("DEBUG", "False") == "True"

print("✅ Configuration loaded")

---

# backend/app/services/matching.py
# Matching Algorithm Service - Problem + Distance Based

from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from app.models import User, Match, ProblemEnum, MatchStatus
from math import radians, sin, cos, sqrt, atan2
from datetime import datetime
from typing import List, Tuple

class MatchingService:
    
    @staticmethod
    def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance between two coordinates using Haversine formula
        Returns distance in kilometers
        """
        if not all([lat1, lon1, lat2, lon2]):
            return float('inf')
        
        R = 6371  # Earth radius in km
        
        lat1_rad = radians(lat1)
        lat2_rad = radians(lat2)
        delta_lat = radians(lat2 - lat1)
        delta_lon = radians(lon2 - lon1)
        
        a = sin(delta_lat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(delta_lon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        
        return R * c
    
    @staticmethod
    def calculate_match_score(
        user_1: User,
        user_2: User,
        distance_km: float
    ) -> Tuple[int, str]:
        """
        Calculate match score (0-200) and reason
        
        Tier 1: Perfect Match (100+ points)
        - Primary problem exact match
        - Same timezone
        - Both online recently
        
        Tier 2: Strong Match (80+ points)
        - Primary problem exact match
        - Secondary overlap
        
        Tier 3: Good Match (60+ points)
        - Primary matches secondary
        - Same timezone
        
        Tier 4: Related Match (40+ points)
        - Problems related
        
        Tier 5: Similar Stage (20+ points)
        - Different problems, same life stage
        """
        
        score = 0
        reason_parts = []
        
        # ============ PROBLEM MATCHING ============
        
        # Check primary problem exact match
        if user_1.primary_problem == user_2.primary_problem:
            score += 100
            reason_parts.append("Same primary problem")
        
        # Check secondary problem overlap
        user_1_all_problems = [user_1.primary_problem] + user_1.secondary_problems
        user_2_all_problems = [user_2.primary_problem] + user_2.secondary_problems
        
        problem_overlap = set(user_1_all_problems) & set(user_2_all_problems)
        if len(problem_overlap) > 1:  # More than just primary
            score += 30
            reason_parts.append(f"{len(problem_overlap)} shared issues")
        
        # ============ DISTANCE MATCHING ============
        
        if distance_km <= 5:
            score += 30
            reason_parts.append(f"{distance_km:.1f}km away")
        elif distance_km <= 10:
            score += 20
            reason_parts.append(f"{distance_km:.1f}km away")
        elif distance_km <= 20:
            score += 10
            reason_parts.append(f"{distance_km:.1f}km away")
        elif distance_km <= user_2.distance_preference:
            score += 5
        
        # ============ TIMEZONE MATCHING ============
        
        if user_1.timezone == user_2.timezone:
            score += 15
            reason_parts.append("Same timezone")
        
        # ============ ACTIVITY MATCHING ============
        
        # Check if both online recently (last 4 hours)
        from datetime import timedelta
        now = datetime.utcnow()
        if (user_1.last_active_at and (now - user_1.last_active_at).total_seconds() < 4*3600 and
            user_2.last_active_at and (now - user_2.last_active_at).total_seconds() < 4*3600):
            score += 10
            reason_parts.append("Both recently active")
        
        # ============ RELATIONSHIP HISTORY ============
        
        # Bonus: avoid matching same person multiple times
        # (they've already chatted)
        existing_match = None  # Would query for existing match here
        if existing_match:
            score -= 20
        
        # ============ COMPILE REASON ============
        
        reason = " + ".join(reason_parts) if reason_parts else "Potential match"
        
        return min(score, 200), reason  # Cap at 200
    
    @staticmethod
    def find_matches(
        user: User,
        db: Session,
        limit: int = 3
    ) -> List[dict]:
        """
        Find best matches for a user based on:
        - Primary problem
        - Distance preference
        - Timezone
        """
        
        # Get all active users (excluding self, excluded users, and already matched)
        potential_matches = db.query(User).filter(
            User.id != user.id,
            User.is_active == True,
            User.primary_problem == user.primary_problem  # Start with same problem
        ).all()
        
        if not potential_matches:
            # If no same-problem matches, try secondary problems
            potential_matches = db.query(User).filter(
                User.id != user.id,
                User.is_active == True,
            ).all()
        
        # Calculate scores for each potential match
        scored_matches = []
        
        for potential_match in potential_matches:
            # Check if user prefers this distance
            if not potential_match.latitude or not potential_match.longitude:
                continue
            
            if not user.latitude or not user.longitude:
                continue
            
            distance_km = MatchingService.haversine_distance(
                user.latitude, user.longitude,
                potential_match.latitude, potential_match.longitude
            )
            
            # Check distance preference
            if distance_km > potential_match.distance_preference:
                continue  # Outside their distance preference
            
            if distance_km > user.distance_preference:
                continue  # Outside our distance preference
            
            # Calculate match score
            score, reason = MatchingService.calculate_match_score(
                user, potential_match, distance_km
            )
            
            # Check if match already exists
            existing = db.query(Match).filter(
                ((Match.user_1_id == user.id) & (Match.user_2_id == potential_match.id)) |
                ((Match.user_1_id == potential_match.id) & (Match.user_2_id == user.id))
            ).first()
            
            if existing:
                continue  # Skip if already matched
            
            scored_matches.append({
                "user": potential_match,
                "distance_km": distance_km,
                "score": score,
                "reason": reason
            })
        
        # Sort by score (descending) and return top matches
        scored_matches.sort(key=lambda x: x["score"], reverse=True)
        
        return scored_matches[:limit]
    
    @staticmethod
    def create_match(
        user_1_id: int,
        user_2_id: int,
        problem: ProblemEnum,
        distance_km: float,
        score: int,
        reason: str,
        db: Session
    ) -> Match:
        """Create a new match record"""
        
        match = Match(
            user_1_id=user_1_id,
            user_2_id=user_2_id,
            problem_matched=problem,
            distance_km=distance_km,
            match_score=score,
            match_reason=reason,
            status=MatchStatus.PENDING
        )
        
        db.add(match)
        db.commit()
        db.refresh(match)
        
        return match

---

# backend/app/services/auth.py
# Authentication Service - JWT Tokens

from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Optional
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password for storage"""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        
        return encoded_jwt
    
    @staticmethod
    def decode_token(token: str) -> Optional[dict]:
        """Decode JWT token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            return None

---

# backend/app/services/razorpay_service.py
# Razorpay Payment Integration

import razorpay
from app.config import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET
from typing import Optional

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

class RazorpayService:
    
    @staticmethod
    def create_order(
        amount: int,  # ₹ amount in paise (₹100 = 10000 paise)
        currency: str = "INR",
        receipt: str = None,
        description: str = None,
        customer_notify: int = 1
    ) -> dict:
        """
        Create a Razorpay order
        
        Args:
            amount: Amount in paise (₹100 = 10000)
            currency: "INR"
            receipt: Order ID for tracking
            description: Order description
        
        Returns:
            Order details with order_id
        """
        
        try:
            order = client.order.create({
                "amount": amount,  # In paise
                "currency": currency,
                "receipt": receipt or "receipt#1",
                "description": description or "SoulConnect Payment",
                "customer_notify": customer_notify
            })
            
            return {
                "success": True,
                "order_id": order["id"],
                "amount": order["amount"],
                "currency": order["currency"]
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def verify_payment(
        razorpay_order_id: str,
        razorpay_payment_id: str,
        razorpay_signature: str
    ) -> bool:
        """
        Verify Razorpay payment signature
        
        This should be called after user completes payment
        """
        
        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })
            return True
        except Exception as e:
            print(f"Payment verification failed: {e}")
            return False
    
    @staticmethod
    def fetch_payment(payment_id: str) -> Optional[dict]:
        """Fetch payment details from Razorpay"""
        try:
            payment = client.payment.fetch(payment_id)
            return payment
        except:
            return None
    
    @staticmethod
    def create_subscription(
        plan_id: str,
        customer_notify: int = 1,
        quantity: int = 1,
        total_count: int = 12  # 12 months
    ) -> dict:
        """Create recurring subscription"""
        try:
            subscription = client.subscription.create({
                "plan_id": plan_id,
                "customer_notify": customer_notify,
                "quantity": quantity,
                "total_count": total_count
            })
            return {"success": True, "subscription_id": subscription["id"]}
        except Exception as e:
            return {"success": False, "error": str(e)}
