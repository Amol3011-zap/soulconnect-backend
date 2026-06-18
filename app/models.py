from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Enum, ForeignKey, JSON, Text, Index
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.database import Base


# ========== ENUMS ==========

class ProblemEnum(str, enum.Enum):
    ANXIETY = "anxiety"
    DEPRESSION = "depression"
    OCD_INTRUSIVE_THOUGHTS = "ocd_intrusive_thoughts"
    PTSD_TRAUMA = "ptsd_trauma"
    PHOBIAS = "phobias"
    PANIC_ATTACKS = "panic_attacks"
    SELF_HARM = "self_harm"
    RELATIONSHIP_BREAKUP = "relationship_breakup"
    DIVORCE = "divorce"
    MARRIAGE_PROBLEMS = "marriage_problems"
    FAMILY_RELATIONSHIPS = "family_relationships"
    TRUST_ISSUES = "trust_issues"
    UNREQUITED_LOVE = "unrequited_love"
    LONELINESS = "loneliness"
    LACK_OF_CONFIDENCE = "lack_of_confidence"
    BULLYING_HARASSMENT = "bullying_harassment"
    GRIEF_LOSS = "grief_loss"
    WORK_CAREER_STRESS = "work_career_stress"
    FINANCIAL_STRESS = "financial_stress"
    IDENTITY_SEXUAL_ORIENTATION = "identity_sexual_orientation"
    ADDICTION_SUBSTANCE_ABUSE = "addiction_substance_abuse"
    HEALTH_ANXIETY = "health_anxiety"
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
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    bio = Column(String(500), nullable=True)
    role = Column(String, default="user")

    primary_problem = Column(Enum(ProblemEnum), nullable=False)
    secondary_problems = Column(JSON, default=list)
    problem_context = Column(String(500), nullable=True)

    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    country = Column(String, nullable=True)
    distance_preference = Column(Integer, default=10)
    hide_location = Column(Boolean, default=False)

    timezone = Column(String, default="Asia/Kolkata")

    is_active = Column(Boolean, default=True)
    interested_in_healer = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active_at = Column(DateTime, default=datetime.utcnow)

    matches = relationship("Match", foreign_keys="[Match.user_1_id]", back_populates="user_1")
    chats = relationship("Chat", back_populates="user")
    healer_sessions = relationship("HealerSession", back_populates="user")
    subscriptions = relationship("Subscription", back_populates="user")
    meetups = relationship("MeetupAttendee", back_populates="user")
    journey = relationship("UserJourney", back_populates="user", uselist=False)


# ========== MATCH MODEL ==========

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    user_1_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user_2_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    problem_matched = Column(Enum(ProblemEnum), nullable=False)
    distance_km = Column(Float)
    match_score = Column(Integer)
    match_reason = Column(String(500))
    status = Column(Enum(MatchStatus), default=MatchStatus.PENDING)

    matched_at = Column(DateTime, default=datetime.utcnow)
    accepted_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    rating_from_1 = Column(Integer, nullable=True)
    rating_from_2 = Column(Integer, nullable=True)
    feedback_from_1 = Column(Text, nullable=True)
    feedback_from_2 = Column(Text, nullable=True)

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

    specializations = Column(JSON, default=[])
    experience_years = Column(Integer, default=1)

    certification_url = Column(String, nullable=True)
    is_verified = Column(Boolean, default=False)
    verified_at = Column(DateTime, nullable=True)

    hourly_rate = Column(Integer, default=500)
    availability = Column(JSON, default={})

    total_rating = Column(Float, default=0)
    review_count = Column(Integer, default=0)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    sessions = relationship("HealerSession", back_populates="healer")


# ========== HEALER SESSION MODEL ==========

class HealerSession(Base):
    __tablename__ = "healer_sessions"

    id = Column(Integer, primary_key=True, index=True)
    healer_id = Column(Integer, ForeignKey("healers.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    problem_type = Column(Enum(ProblemEnum), nullable=False)

    scheduled_time = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, default=60)
    session_type = Column(String, default="video")

    status = Column(String, default="pending")

    amount = Column(Integer)
    platform_commission = Column(Integer)
    healer_earning = Column(Integer)
    payment_status = Column(String, default="pending")
    razorpay_payment_id = Column(String, nullable=True)

    user_notes = Column(Text, nullable=True)
    healer_notes = Column(Text, nullable=True)
    rating = Column(Integer, nullable=True)
    feedback = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    healer = relationship("Healer", back_populates="sessions")
    user = relationship("User", back_populates="healer_sessions")


# ========== MEETUP MODEL ==========

class Meetup(Base):
    __tablename__ = "meetups"

    id = Column(Integer, primary_key=True, index=True)
    problem_type = Column(Enum(ProblemEnum), nullable=False)

    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    location_name = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    city = Column(String, nullable=False)

    scheduled_time = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, default=90)

    max_attendees = Column(Integer, default=8)
    host_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    status = Column(String, default="upcoming")

    avg_rating = Column(Float, default=0)
    review_count = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)

    attendees = relationship("MeetupAttendee", back_populates="meetup")


# ========== MEETUP ATTENDEE MODEL ==========

class MeetupAttendee(Base):
    __tablename__ = "meetup_attendees"

    id = Column(Integer, primary_key=True, index=True)
    meetup_id = Column(Integer, ForeignKey("meetups.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    status = Column(String, default="confirmed")
    joined_at = Column(DateTime, default=datetime.utcnow)

    rating = Column(Integer, nullable=True)
    feedback = Column(Text, nullable=True)

    meetup = relationship("Meetup", back_populates="attendees")
    user = relationship("User", back_populates="meetups")


# ========== SUBSCRIPTION MODEL ==========

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    plan = Column(String, default="premium")
    amount = Column(Integer, default=299)

    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)
    status = Column(String, default="active")

    razorpay_subscription_id = Column(String, nullable=True)
    razorpay_payment_id = Column(String, nullable=True)
    payment_status = Column(String, default="pending")

    features = Column(JSON, default={
        "priority_matching": True,
        "unlimited_meetups": True,
        "healer_discount": 0.20,
        "expanded_search_radius": 50,
        "progress_tracking": True,
        "no_ads": True
    })

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="subscriptions")


# ========== SAFETY FLAG MODEL ==========

# ========== SOUL JOURNEY ENUMS ==========

class JourneyStageEnum(str, enum.Enum):
    BEGINNING = "beginning"
    HEALING = "healing"
    GROWTH = "growth"
    TRANSFORMATION = "transformation"
    INNER_HARMONY = "inner_harmony"


class ActivityTypeEnum(str, enum.Enum):
    MEDITATION = "meditation"
    JOURNAL = "journal"
    CHAT_SESSION = "chat_session"
    HEALER_BOOKING = "healer_booking"
    CHECK_IN = "check_in"
    REFLECTION = "reflection"


# ========== USER JOURNEY MODEL ==========

class UserJourney(Base):
    __tablename__ = "user_journeys"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    current_stage = Column(Enum(JourneyStageEnum), default=JourneyStageEnum.BEGINNING)
    joined_at = Column(DateTime, default=datetime.utcnow)
    total_activities = Column(Integer, default=0)

    user = relationship("User", back_populates="journey")
    activities = relationship("JourneyActivity", back_populates="journey", cascade="all, delete-orphan")


# ========== JOURNEY ACTIVITY MODEL ==========

class JourneyActivity(Base):
    __tablename__ = "journey_activities"

    id = Column(Integer, primary_key=True, index=True)
    journey_id = Column(Integer, ForeignKey("user_journeys.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    activity_type = Column(Enum(ActivityTypeEnum), nullable=False)
    duration_minutes = Column(Integer, default=0)
    intensity = Column(Integer, default=5)  # 1–10
    notes = Column(Text, default="")
    logged_at = Column(DateTime, default=datetime.utcnow)

    journey = relationship("UserJourney", back_populates="activities")

    __table_args__ = (
        Index("ix_journey_activities_user_date", "user_id", "logged_at"),
    )


# ========== SAFETY FLAG MODEL ==========

class SafetyFlag(Base):
    __tablename__ = "safety_flags"

    id = Column(Integer, primary_key=True, index=True)
    flagged_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reporter_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    flag_type = Column(String)
    description = Column(Text)

    is_resolved = Column(Boolean, default=False)
    resolution_notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)


# ========== CRISIS RESOURCES MODEL ==========

class CrisisResource(Base):
    __tablename__ = "crisis_resources"

    id = Column(Integer, primary_key=True, index=True)
    country = Column(String)
    organization = Column(String)
    phone = Column(String)
    email = Column(String, nullable=True)
    website = Column(String, nullable=True)
    description = Column(Text)
    available_24_7 = Column(Boolean, default=True)
