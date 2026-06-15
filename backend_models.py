# backend/app/models.py
# SQLAlchemy Models - Database Schema

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Enum, ForeignKey, JSON, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()

# ========== ENUMS ==========

class ProblemEnum(str, enum.Enum):
    # Mental Health
    ANXIETY = "anxiety"
    DEPRESSION = "depression"
    OCD_INTRUSIVE_THOUGHTS = "ocd_intrusive_thoughts"
    PTSD_TRAUMA = "ptsd_trauma"
    PHOBIAS = "phobias"
    PANIC_ATTACKS = "panic_attacks"
    SELF_HARM = "self_harm"
    
    # Relationships
    RELATIONSHIP_BREAKUP = "relationship_breakup"
    DIVORCE = "divorce"
    MARRIAGE_PROBLEMS = "marriage_problems"
    FAMILY_RELATIONSHIPS = "family_relationships"
    TRUST_ISSUES = "trust_issues"
    UNREQUITED_LOVE = "unrequited_love"
    
    # Life Challenges
    LONELINESS = "loneliness"
    LACK_OF_CONFIDENCE = "lack_of_confidence"
    BULLYING_HARASSMENT = "bullying_harassment"
    GRIEF_LOSS = "grief_loss"
    WORK_CAREER_STRESS = "work_career_stress"
    FINANCIAL_STRESS = "financial_stress"
    
    # Life Transitions
    IDENTITY_SEXUAL_ORIENTATION = "identity_sexual_orientation"
    ADDICTION_SUBSTANCE_ABUSE = "addiction_substance_abuse"
    HEALTH_ANXIETY = "health_anxiety"
    
    # Lifestyle
    SLEEP_PROBLEMS = "sleep_problems"
    EATING_DISORDERS = "eating_disorders"
    ANGER_MANAGEMENT = "anger_management"

class MatchStatus(str, enum.Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    REJECTED = "rejected"

# ========== USER MODEL ==========

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String, unique=True, index=True, nullable=False)
    phone_verified = Column(Boolean, default=False)
    name = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    bio = Column(String(500), nullable=True)
    
    # Problems
    primary_problem = Column(Enum(ProblemEnum), nullable=False)
    secondary_problems = Column(JSON, default=[])  # List of problems
    problem_context = Column(String(500), nullable=True)  # "Breakup 2 months ago"
    
    # Location
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    address = Column(String, nullable=True)  # "Chembur, Mumbai"
    city = Column(String, nullable=True)  # "Mumbai"
    distance_preference = Column(Integer, default=10)  # 5, 10, 20, 999 (anywhere)
    hide_location = Column(Boolean, default=False)
    
    # Timezone
    timezone = Column(String, default="Asia/Kolkata")
    
    # Status
    is_active = Column(Boolean, default=True)
    interested_in_healer = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    matches = relationship("Match", foreign_keys="[Match.user_1_id]", back_populates="user_1")
    chats = relationship("Chat", back_populates="user")
    healer_sessions = relationship("HealerSession", back_populates="user")
    subscriptions = relationship("Subscription", back_populates="user")
    meetups = relationship("MeetupAttendee", back_populates="user")

# ========== MATCH MODEL ==========

class Match(Base):
    __tablename__ = "matches"
    
    id = Column(Integer, primary_key=True, index=True)
    user_1_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user_2_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    problem_matched = Column(Enum(ProblemEnum), nullable=False)
    distance_km = Column(Float)
    match_score = Column(Integer)  # 0-200
    match_reason = Column(String(500))  # "Same breakup + anxiety"
    status = Column(Enum(MatchStatus), default=MatchStatus.PENDING)
    
    matched_at = Column(DateTime, default=datetime.utcnow)
    accepted_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Ratings
    rating_from_1 = Column(Integer, nullable=True)  # 1-5
    rating_from_2 = Column(Integer, nullable=True)  # 1-5
    feedback_from_1 = Column(Text, nullable=True)
    feedback_from_2 = Column(Text, nullable=True)
    
    # Relationships
    user_1 = relationship("User", foreign_keys=[user_1_id], back_populates="matches")
    chats = relationship("Chat", back_populates="match")

# ========== CHAT MODEL ==========

class Chat(Base):
    __tablename__ = "chats"
    
    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    match = relationship("Match", back_populates="chats")
    user = relationship("User", back_populates="chats")

# ========== HEALER MODEL ==========

class Healer(Base):
    __tablename__ = "healers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    
    # Specializations
    specializations = Column(JSON, default=[])  # List of ProblemEnum values
    experience_years = Column(Integer, default=1)
    
    # Verification
    certification_url = Column(String, nullable=True)  # PDF/image URL
    is_verified = Column(Boolean, default=False)
    verified_at = Column(DateTime, nullable=True)
    
    # Pricing
    hourly_rate = Column(Integer, default=500)  # ₹500-2000
    
    # Availability (JSON format)
    # {"Monday": ["18:00-20:00"], "Wednesday": ["18:00-20:00"], ...}
    availability = Column(JSON, default={})
    
    # Rating & Reviews
    total_rating = Column(Float, default=0)  # Average rating
    review_count = Column(Integer, default=0)
    
    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    sessions = relationship("HealerSession", back_populates="healer")

# ========== HEALER SESSION MODEL ==========

class HealerSession(Base):
    __tablename__ = "healer_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    healer_id = Column(Integer, ForeignKey("healers.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    problem_type = Column(Enum(ProblemEnum), nullable=False)
    
    # Scheduling
    scheduled_time = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, default=60)
    session_type = Column(String, default="video")  # video, voice, chat, distant
    
    # Status
    status = Column(String, default="pending")  # pending, confirmed, completed, cancelled
    
    # Pricing
    amount = Column(Integer)  # ₹ amount agreed
    platform_commission = Column(Integer)  # 25% of amount
    healer_earning = Column(Integer)  # 75% of amount
    payment_status = Column(String, default="pending")  # pending, completed, refunded
    razorpay_payment_id = Column(String, nullable=True)
    
    # Feedback
    user_notes = Column(Text, nullable=True)  # What user wants to work on
    healer_notes = Column(Text, nullable=True)  # Session notes
    rating = Column(Integer, nullable=True)  # 1-5
    feedback = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    healer = relationship("Healer", back_populates="sessions")
    user = relationship("User", back_populates="healer_sessions")

# ========== MEETUP MODEL ==========

class Meetup(Base):
    __tablename__ = "meetups"
    
    id = Column(Integer, primary_key=True, index=True)
    problem_type = Column(Enum(ProblemEnum), nullable=False)
    
    title = Column(String, nullable=False)  # "Breakup Support Circle"
    description = Column(Text, nullable=True)
    
    # Location
    location_name = Column(String, nullable=False)  # "Café Coffee Day, Chembur"
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    city = Column(String, nullable=False)
    
    # Timing
    scheduled_time = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, default=90)
    
    # Details
    max_attendees = Column(Integer, default=8)
    host_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # User or admin
    
    # Status
    status = Column(String, default="upcoming")  # upcoming, ongoing, completed
    
    # Rating
    avg_rating = Column(Float, default=0)
    review_count = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    attendees = relationship("MeetupAttendee", back_populates="meetup")

# ========== MEETUP ATTENDEE MODEL ==========

class MeetupAttendee(Base):
    __tablename__ = "meetup_attendees"
    
    id = Column(Integer, primary_key=True, index=True)
    meetup_id = Column(Integer, ForeignKey("meetups.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    status = Column(String, default="confirmed")  # confirmed, attended, skipped
    joined_at = Column(DateTime, default=datetime.utcnow)
    
    # Feedback
    rating = Column(Integer, nullable=True)  # 1-5
    feedback = Column(Text, nullable=True)
    
    # Relationships
    meetup = relationship("Meetup", back_populates="attendees")
    user = relationship("User", back_populates="meetups")

# ========== SUBSCRIPTION MODEL ==========

class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    plan = Column(String, default="premium")  # premium
    amount = Column(Integer, default=299)  # ₹299/month
    
    # Billing
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)  # NULL if ongoing
    status = Column(String, default="active")  # active, cancelled, expired
    
    # Payment
    razorpay_subscription_id = Column(String, nullable=True)
    razorpay_payment_id = Column(String, nullable=True)
    payment_status = Column(String, default="pending")  # pending, completed, failed
    
    # Features unlocked
    features = Column(JSON, default={
        "priority_matching": True,
        "unlimited_meetups": True,
        "healer_discount": 0.20,  # 20% discount
        "expanded_search_radius": 50,  # 50km instead of 10km
        "progress_tracking": True,
        "no_ads": True
    })
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="subscriptions")

# ========== SAFETY FLAG MODEL ==========

class SafetyFlag(Base):
    __tablename__ = "safety_flags"
    
    id = Column(Integer, primary_key=True, index=True)
    flagged_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reporter_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    flag_type = Column(String)  # inappropriate_behavior, harassment, spam, etc.
    description = Column(Text)
    
    is_resolved = Column(Boolean, default=False)
    resolution_notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

# ========== CRISIS RESOURCES MODEL ==========

class CrisisResource(Base):
    __tablename__ = "crisis_resources"
    
    id = Column(Integer, primary_key=True, index=True)
    country = Column(String)  # "India", "US", "UK"
    organization = Column(String)  # "AASRA", "iCall"
    phone = Column(String)
    email = Column(String, nullable=True)
    website = Column(String, nullable=True)
    description = Column(Text)
    available_24_7 = Column(Boolean, default=True)
