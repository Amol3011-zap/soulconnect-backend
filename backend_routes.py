# backend/app/routes/auth.py
# Authentication Routes - Signup, Login, Phone Verification

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.services.auth import AuthService
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class SignupRequest(BaseModel):
    phone: str
    name: str
    primary_problem: str
    secondary_problems: list = []
    latitude: float
    longitude: float
    address: str
    city: str
    timezone: str = "Asia/Kolkata"
    distance_preference: int = 10

class SignupResponse(BaseModel):
    id: int
    phone: str
    name: str
    access_token: str
    token_type: str = "bearer"

@router.post("/signup", response_model=SignupResponse)
async def signup(request: SignupRequest, db: Session = Depends(get_db)):
    """User Signup - temporarily disabled"""
    raise HTTPException(status_code=503, detail="Signup is temporarily disabled")

class LoginRequest(BaseModel):
    phone: str

@router.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """User Login - Phone-based authentication"""
    raise HTTPException(status_code=503, detail="Login is temporarily disabled")

---

# backend/app/routes/users.py
# User Profile Routes

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

def get_current_user(token: str = None, db: Session = Depends(get_db)) -> User:
    """Dependency to get current authenticated user"""
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    from app.services.auth import AuthService
    payload = AuthService.decode_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == int(user_id)).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.get("/me")
async def get_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile"""
    return {
        "id": current_user.id,
        "name": current_user.name,
        "phone": current_user.phone,
        "primary_problem": current_user.primary_problem,
        "secondary_problems": current_user.secondary_problems,
        "city": current_user.city,
        "distance_preference": current_user.distance_preference,
        "avatar_url": current_user.avatar_url,
        "bio": current_user.bio
    }

class UpdateProfileRequest(BaseModel):
    name: str = None
    bio: str = None
    avatar_url: str = None
    distance_preference: int = None

@router.put("/me")
async def update_profile(
    request: UpdateProfileRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user profile"""
    
    if request.name:
        current_user.name = request.name
    if request.bio:
        current_user.bio = request.bio
    if request.avatar_url:
        current_user.avatar_url = request.avatar_url
    if request.distance_preference:
        current_user.distance_preference = request.distance_preference
    
    current_user.last_active_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Profile updated"}

---

# backend/app/routes/matching.py
# Matching Routes - Find and accept matches

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Match, MatchStatus
from app.services.matching import MatchingService
from app.routes.users import get_current_user
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

@router.post("/find")
async def find_matches(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Find best matches for current user by problem + distance"""
    
    matches = MatchingService.find_matches(current_user, db, limit=3)
    
    if not matches:
        return {
            "message": "No matches found yet",
            "matches": [],
            "count": 0
        }
    
    response = []
    for match_data in matches:
        response.append({
            "id": match_data["user"].id,
            "name": match_data["user"].name,
            "problem": match_data["user"].primary_problem,
            "distance_km": round(match_data["distance_km"], 1),
            "match_score": match_data["score"],
            "match_reason": match_data["reason"],
            "city": match_data["user"].city,
            "problem_context": match_data["user"].problem_context
        })
    
    return {
        "message": f"Found {len(response)} matches",
        "matches": response,
        "count": len(response)
    }

class AcceptMatchRequest(BaseModel):
    matched_user_id: int

@router.post("/accept")
async def accept_match(
    request: AcceptMatchRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Accept a match and create chat conversation"""
    
    matched_user = db.query(User).filter(
        User.id == request.matched_user_id
    ).first()
    
    if not matched_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Calculate match details
    from app.services.matching import MatchingService
    distance_km = MatchingService.haversine_distance(
        current_user.latitude, current_user.longitude,
        matched_user.latitude, matched_user.longitude
    )
    
    score, reason = MatchingService.calculate_match_score(
        current_user, matched_user, distance_km
    )
    
    # Create match
    match = MatchingService.create_match(
        user_1_id=current_user.id,
        user_2_id=matched_user.id,
        problem=current_user.primary_problem,
        distance_km=distance_km,
        score=score,
        reason=reason,
        db=db
    )
    
    match.status = MatchStatus.ACTIVE
    match.accepted_at = datetime.utcnow()
    db.commit()
    
    return {
        "match_id": match.id,
        "message": "Match accepted! Start chatting.",
        "matched_user": {
            "id": matched_user.id,
            "name": matched_user.name,
            "problem": matched_user.primary_problem
        }
    }

@router.get("/history")
async def match_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's match history"""
    
    matches = db.query(Match).filter(
        (Match.user_1_id == current_user.id) | (Match.user_2_id == current_user.id)
    ).order_by(Match.matched_at.desc()).all()
    
    return {
        "total_matches": len(matches),
        "matches": [
            {
                "id": m.id,
                "problem": m.problem_matched,
                "rating": m.rating_from_1 if m.user_1_id == current_user.id else m.rating_from_2,
                "matched_at": m.matched_at,
                "status": m.status
            }
            for m in matches
        ]
    }

---

# backend/app/routes/chats.py
# Chat Routes - Real-time messaging

from fastapi import APIRouter, Depends, HTTPException, WebSocket
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Match, Chat, MatchStatus
from app.routes.users import get_current_user
from app.models import User
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class SendMessageRequest(BaseModel):
    match_id: int
    message: str

@router.post("/send")
async def send_message(
    request: SendMessageRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send message in a match chat"""
    
    match = db.query(Match).filter(Match.id == request.match_id).first()
    
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    # Verify user is part of this match
    if match.user_1_id != current_user.id and match.user_2_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Create chat message
    chat = Chat(
        match_id=request.match_id,
        sender_id=current_user.id,
        message=request.message,
        is_read=False
    )
    
    db.add(chat)
    db.commit()
    db.refresh(chat)
    
    return {
        "id": chat.id,
        "message": request.message,
        "sent_at": chat.created_at
    }

@router.get("/{match_id}/history")
async def get_chat_history(
    match_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get chat history for a match"""
    
    match = db.query(Match).filter(Match.id == match_id).first()
    
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    # Verify authorization
    if match.user_1_id != current_user.id and match.user_2_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    messages = db.query(Chat).filter(Chat.match_id == match_id).order_by(Chat.created_at).all()
    
    return {
        "match_id": match_id,
        "total_messages": len(messages),
        "messages": [
            {
                "id": m.id,
                "sender_id": m.sender_id,
                "message": m.message,
                "created_at": m.created_at
            }
            for m in messages
        ]
    }

class RateMatchRequest(BaseModel):
    match_id: int
    rating: int  # 1-5
    feedback: str = None

@router.post("/rate")
async def rate_match(
    request: RateMatchRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Rate a completed match"""
    
    match = db.query(Match).filter(Match.id == request.match_id).first()
    
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    if request.rating < 1 or request.rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be 1-5")
    
    # Set rating based on who's rating
    if match.user_1_id == current_user.id:
        match.rating_from_1 = request.rating
        match.feedback_from_1 = request.feedback
    elif match.user_2_id == current_user.id:
        match.rating_from_2 = request.rating
        match.feedback_from_2 = request.feedback
    else:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    match.completed_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Rating saved"}

---

# backend/app/routes/healers.py
# Healer Routes - Directory and booking

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Healer, HealerSession
from app.routes.users import get_current_user
from app.models import User
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

@router.get("/")
async def list_healers(
    problem: str = None,
    city: str = None,
    db: Session = Depends(get_db)
):
    """List all verified healers, optionally filtered by problem"""
    
    query = db.query(Healer).filter(Healer.is_verified == True)
    
    if problem:
        # Filter healers with this specialization
        query = query.filter(Healer.specializations.contains([problem]))
    
    healers = query.all()
    
    return {
        "total": len(healers),
        "healers": [
            {
                "id": h.id,
                "name": h.name,
                "specializations": h.specializations,
                "hourly_rate": h.hourly_rate,
                "experience_years": h.experience_years,
                "rating": h.total_rating,
                "review_count": h.review_count,
                "avatar_url": h.avatar_url,
                "bio": h.bio
            }
            for h in healers
        ]
    }

@router.get("/{healer_id}")
async def get_healer_detail(
    healer_id: int,
    db: Session = Depends(get_db)
):
    """Get detailed healer profile"""
    
    healer = db.query(Healer).filter(
        Healer.id == healer_id,
        Healer.is_verified == True
    ).first()
    
    if not healer:
        raise HTTPException(status_code=404, detail="Healer not found")
    
    return {
        "id": healer.id,
        "name": healer.name,
        "bio": healer.bio,
        "specializations": healer.specializations,
        "experience_years": healer.experience_years,
        "hourly_rate": healer.hourly_rate,
        "rating": healer.total_rating,
        "review_count": healer.review_count,
        "availability": healer.availability,
        "avatar_url": healer.avatar_url,
        "certification_url": healer.certification_url
    }

class BookSessionRequest(BaseModel):
    healer_id: int
    scheduled_time: datetime
    problem_type: str
    duration_minutes: int = 60
    user_notes: str = None

@router.post("/book-session")
async def book_healer_session(
    request: BookSessionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Book a healer session"""
    
    healer = db.query(Healer).filter(
        Healer.id == request.healer_id,
        Healer.is_verified == True
    ).first()
    
    if not healer:
        raise HTTPException(status_code=404, detail="Healer not found")
    
    # Calculate amount
    amount = int((request.duration_minutes / 60) * healer.hourly_rate)
    commission = int(amount * 0.25)  # 25% platform commission
    healer_earning = amount - commission
    
    # Create session
    session = HealerSession(
        healer_id=request.healer_id,
        user_id=current_user.id,
        problem_type=request.problem_type,
        scheduled_time=request.scheduled_time,
        duration_minutes=request.duration_minutes,
        amount=amount,
        platform_commission=commission,
        healer_earning=healer_earning,
        user_notes=request.user_notes,
        status="pending"
    )
    
    db.add(session)
    db.commit()
    db.refresh(session)
    
    return {
        "session_id": session.id,
        "healer": healer.name,
        "scheduled_time": session.scheduled_time,
        "amount": amount,
        "status": "pending",
        "message": "Session booked. Waiting for payment."
    }

---

# backend/app/routes/meetups.py
# Meetup Routes - Browse and attend meetups

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Meetup, MeetupAttendee
from app.routes.users import get_current_user
from app.models import User
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

@router.get("/")
async def list_meetups(
    problem: str = None,
    city: str = None,
    db: Session = Depends(get_db)
):
    """List upcoming meetups"""
    
    query = db.query(Meetup).filter(Meetup.status == "upcoming")
    
    if problem:
        query = query.filter(Meetup.problem_type == problem)
    
    if city:
        query = query.filter(Meetup.city == city)
    
    meetups = query.order_by(Meetup.scheduled_time).all()
    
    return {
        "total": len(meetups),
        "meetups": [
            {
                "id": m.id,
                "title": m.title,
                "problem": m.problem_type,
                "location": m.location_name,
                "city": m.city,
                "scheduled_time": m.scheduled_time,
                "duration_minutes": m.duration_minutes,
                "attendees": len(m.attendees),
                "max_attendees": m.max_attendees,
                "rating": m.avg_rating,
                "description": m.description
            }
            for m in meetups
        ]
    }

@router.get("/{meetup_id}")
async def get_meetup_detail(
    meetup_id: int,
    db: Session = Depends(get_db)
):
    """Get detailed meetup info"""
    
    meetup = db.query(Meetup).filter(Meetup.id == meetup_id).first()
    
    if not meetup:
        raise HTTPException(status_code=404, detail="Meetup not found")
    
    return {
        "id": meetup.id,
        "title": meetup.title,
        "description": meetup.description,
        "problem": meetup.problem_type,
        "location": meetup.location_name,
        "coordinates": {"lat": meetup.latitude, "lng": meetup.longitude},
        "scheduled_time": meetup.scheduled_time,
        "duration_minutes": meetup.duration_minutes,
        "attendees": len(meetup.attendees),
        "max_attendees": meetup.max_attendees,
        "rating": meetup.avg_rating,
        "status": meetup.status
    }

class JoinMeetupRequest(BaseModel):
    meetup_id: int

@router.post("/join")
async def join_meetup(
    request: JoinMeetupRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Join a meetup"""
    
    meetup = db.query(Meetup).filter(Meetup.id == request.meetup_id).first()
    
    if not meetup:
        raise HTTPException(status_code=404, detail="Meetup not found")
    
    # Check if already joined
    existing = db.query(MeetupAttendee).filter(
        MeetupAttendee.meetup_id == request.meetup_id,
        MeetupAttendee.user_id == current_user.id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Already joined")
    
    # Check space available
    if len(meetup.attendees) >= meetup.max_attendees:
        raise HTTPException(status_code=400, detail="Meetup is full")
    
    # Add attendee
    attendee = MeetupAttendee(
        meetup_id=request.meetup_id,
        user_id=current_user.id,
        status="confirmed"
    )
    
    db.add(attendee)
    db.commit()
    
    return {
        "message": "Joined meetup!",
        "meetup": meetup.title,
        "scheduled_time": meetup.scheduled_time,
        "location": meetup.location_name
    }

@router.get("/my-meetups")
async def my_meetups(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's joined meetups"""
    
    attendances = db.query(MeetupAttendee).filter(
        MeetupAttendee.user_id == current_user.id
    ).all()
    
    return {
        "total": len(attendances),
        "meetups": [
            {
                "id": a.meetup.id,
                "title": a.meetup.title,
                "scheduled_time": a.meetup.scheduled_time,
                "location": a.meetup.location_name,
                "status": a.status,
                "rating": a.rating
            }
            for a in attendances
        ]
    }

---

# backend/app/routes/admin.py
# Admin Routes - Analytics and management

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Match, Healer, HealerSession, Meetup

router = APIRouter()

@router.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Get platform analytics"""
    
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    total_matches = db.query(Match).count()
    verified_healers = db.query(Healer).filter(Healer.is_verified == True).count()
    total_sessions = db.query(HealerSession).count()
    total_meetups = db.query(Meetup).count()
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "total_matches": total_matches,
        "verified_healers": verified_healers,
        "total_sessions": total_sessions,
        "total_meetups": total_meetups,
        "platform_health": "🟢 Healthy"
    }
