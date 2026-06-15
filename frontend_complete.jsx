# frontend/src/App.jsx
# Main React App with Routing

import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useAuthStore } from './store/auth';

// Pages
import Landing from './pages/Landing';
import Signup from './pages/Signup';
import Matches from './pages/Matches';
import Chat from './pages/Chat';
import Healers from './pages/Healers';
import Meetups from './pages/Meetups';
import Premium from './pages/Premium';
import Account from './pages/Account';

// Components
import Navbar from './components/Navbar';
import CrisisResources from './components/CrisisResources';

function App() {
  const { user, token } = useAuthStore();

  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        {token && <Navbar />}
        <CrisisResources />
        
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<Landing />} />
          
          {/* Auth Routes */}
          {!token ? (
            <>
              <Route path="/signup" element={<Signup />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </>
          ) : (
            <>
              {/* Protected Routes */}
              <Route path="/matches" element={<Matches />} />
              <Route path="/chat/:matchId" element={<Chat />} />
              <Route path="/healers" element={<Healers />} />
              <Route path="/meetups" element={<Meetups />} />
              <Route path="/premium" element={<Premium />} />
              <Route path="/account" element={<Account />} />
              <Route path="*" element={<Navigate to="/matches" replace />} />
            </>
          )}
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;

---

# frontend/src/store/auth.ts
# Zustand Auth Store

import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface AuthState {
  user: any | null;
  token: string | null;
  setAuth: (user: any, token: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      setAuth: (user, token) => set({ user, token }),
      logout: () => set({ user: null, token: null }),
    }),
    {
      name: 'auth-store',
    }
  )
);

---

# frontend/src/services/api.ts
# API Service - All Backend Calls

import axios from 'axios';
import { useAuthStore } from '../store/auth';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add token
api.interceptors.request.use((config) => {
  const { token } = useAuthStore.getState();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authAPI = {
  signup: (data: any) => api.post('/auth/signup', data),
  login: (phone: string) => api.post('/auth/login', { phone }),
};

export const userAPI = {
  getProfile: () => api.get('/users/me'),
  updateProfile: (data: any) => api.put('/users/me', data),
};

export const matchAPI = {
  findMatches: () => api.post('/matches/find'),
  acceptMatch: (matchedUserId: number) => api.post('/matches/accept', { matched_user_id: matchedUserId }),
  getHistory: () => api.get('/matches/history'),
};

export const chatAPI = {
  sendMessage: (matchId: number, message: string) => 
    api.post('/chats/send', { match_id: matchId, message }),
  getHistory: (matchId: number) => api.get(`/chats/${matchId}/history`),
  rateMatch: (matchId: number, rating: number, feedback?: string) =>
    api.post('/chats/rate', { match_id: matchId, rating, feedback }),
};

export const healerAPI = {
  listHealers: (problem?: string) => api.get('/healers/', { params: { problem } }),
  getHealer: (healerId: number) => api.get(`/healers/${healerId}`),
  bookSession: (data: any) => api.post('/healers/book-session', data),
};

export const meetupAPI = {
  listMeetups: (problem?: string, city?: string) => 
    api.get('/meetups/', { params: { problem, city } }),
  getMeetup: (meetupId: number) => api.get(`/meetups/${meetupId}`),
  joinMeetup: (meetupId: number) => api.post('/meetups/join', { meetup_id: meetupId }),
  getMyMeetups: () => api.get('/meetups/my-meetups'),
};

export const adminAPI = {
  getStats: () => api.get('/admin/stats'),
};

export const paymentAPI = {
  createOrder: (amount: number, description: string) =>
    api.post('/payments/create-order', { amount, description }),
  verifyPayment: (data: any) => api.post('/payments/verify', data),
};

---

# frontend/src/pages/Landing.jsx
# Landing Page - Hero + Features

import React from 'react';
import { Link } from 'react-router-dom';

export default function Landing() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-600 to-blue-600">
      {/* Navigation */}
      <nav className="bg-white/10 backdrop-blur-md px-6 py-4">
        <div className="max-w-6xl mx-auto flex justify-between items-center">
          <h1 className="text-2xl font-bold text-white">🌟 SoulConnect</h1>
          <Link to="/signup" className="bg-white text-purple-600 px-6 py-2 rounded-full font-semibold hover:bg-gray-100">
            Get Started
          </Link>
        </div>
      </nav>

      {/* Hero */}
      <div className="max-w-6xl mx-auto px-6 py-20 text-center">
        <h2 className="text-5xl font-bold text-white mb-6">
          Stop Feeling Alone With Your Specific Problem
        </h2>
        
        <p className="text-xl text-gray-100 mb-8 max-w-2xl mx-auto">
          Match with someone dealing with breakup. Or anxiety. Or marriage problems. Or any of 25 specific issues.
          <br />
          <strong>Free peer support + verified healers = Actual solutions.</strong>
        </p>

        <Link 
          to="/signup"
          className="inline-block bg-white text-purple-600 px-8 py-4 rounded-lg font-bold text-lg hover:bg-gray-100 mb-12"
        >
          Find Your Match in 5 Minutes
        </Link>

        {/* Features */}
        <div className="grid md:grid-cols-3 gap-8 mt-16">
          <div className="bg-white/10 backdrop-blur-md text-white p-6 rounded-lg">
            <div className="text-4xl mb-4">💬</div>
            <h3 className="font-bold text-lg mb-2">Problem-Matched Peers</h3>
            <p>Find people dealing with YOUR exact problem, not just random emotion.</p>
          </div>

          <div className="bg-white/10 backdrop-blur-md text-white p-6 rounded-lg">
            <div className="text-4xl mb-4">🧘</div>
            <h3 className="font-bold text-lg mb-2">Verified Healers</h3>
            <p>When talking isn't enough, book a session with certified Pranic healers.</p>
          </div>

          <div className="bg-white/10 backdrop-blur-md text-white p-6 rounded-lg">
            <div className="text-4xl mb-4">🤝</div>
            <h3 className="font-bold text-lg mb-2">Real Meetups</h3>
            <p>Meet people IRL at weekly problem-specific gatherings in your city.</p>
          </div>
        </div>
      </div>

      {/* Social Proof */}
      <div className="bg-white/5 backdrop-blur-sm py-16">
        <div className="max-w-6xl mx-auto px-6">
          <h3 className="text-2xl font-bold text-white text-center mb-12">Real Stories</h3>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white/10 backdrop-blur-md text-white p-6 rounded-lg">
              <p className="italic mb-4">
                "I was dealing with a breakup and felt completely alone. SoulConnect matched me with someone 2 months into their journey. Finally, someone who understood."
              </p>
              <p className="font-semibold">— Priya, 28 | Breakup</p>
            </div>

            <div className="bg-white/10 backdrop-blur-md text-white p-6 rounded-lg">
              <p className="italic mb-4">
                "Anxiety was destroying my career until I found peers going through the same. We swap strategies. I went from 8/10 anxiety to 3/10 in 6 weeks."
              </p>
              <p className="font-semibold">— Rohan, 31 | Work Anxiety</p>
            </div>

            <div className="bg-white/10 backdrop-blur-md text-white p-6 rounded-lg">
              <p className="italic mb-4">
                "My marriage was falling apart. Matched with couples navigating the same issues. Their honesty helped me see I wasn't alone."
              </p>
              <p className="font-semibold">— Kavya, 35 | Marriage Problems</p>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Footer */}
      <div className="bg-black/20 backdrop-blur-sm py-12">
        <div className="max-w-6xl mx-auto px-6 text-center">
          <h3 className="text-2xl font-bold text-white mb-4">Ready to feel less alone?</h3>
          <Link 
            to="/signup"
            className="inline-block bg-white text-purple-600 px-8 py-3 rounded-lg font-bold hover:bg-gray-100"
          >
            Start Now
          </Link>
        </div>
      </div>
    </div>
  );
}

---

# frontend/src/pages/Signup.jsx
# Signup Page - Problem Selection + Location

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/auth';
import { authAPI } from '../services/api';

const PROBLEMS = [
  // Mental Health
  { value: 'anxiety', label: 'Anxiety', icon: '😰' },
  { value: 'depression', label: 'Depression', icon: '😢' },
  { value: 'ocd_intrusive_thoughts', label: 'OCD / Intrusive Thoughts', icon: '🔄' },
  { value: 'ptsd_trauma', label: 'PTSD / Trauma', icon: '⚠️' },
  { value: 'phobias', label: 'Phobias', icon: '😨' },
  { value: 'panic_attacks', label: 'Panic Attacks', icon: '💓' },
  { value: 'self_harm', label: 'Self-Harm / Suicidal Thoughts', icon: '🆘' },
  
  // Relationships
  { value: 'relationship_breakup', label: 'Relationship Breakup', icon: '💔' },
  { value: 'divorce', label: 'Divorce', icon: '📋' },
  { value: 'marriage_problems', label: 'Marriage Problems', icon: '💑' },
  { value: 'family_relationships', label: 'Family Relationships', icon: '👨‍👩‍👧' },
  { value: 'trust_issues', label: 'Trust Issues', icon: '🤝' },
  { value: 'unrequited_love', label: 'Unrequited Love', icon: '💭' },
  
  // Life Challenges
  { value: 'loneliness', label: 'Loneliness', icon: '😔' },
  { value: 'lack_of_confidence', label: 'Lack of Confidence', icon: '📉' },
  { value: 'bullying_harassment', label: 'Bullying / Harassment', icon: '😠' },
  { value: 'grief_loss', label: 'Grief / Loss', icon: '🕯️' },
  { value: 'work_career_stress', label: 'Work / Career Stress', icon: '💼' },
  { value: 'financial_stress', label: 'Financial Stress', icon: '💸' },
  
  // Others
  { value: 'identity_sexual_orientation', label: 'Identity / Sexual Orientation', icon: '🌈' },
  { value: 'addiction_substance_abuse', label: 'Addiction / Substance Abuse', icon: '⚕️' },
  { value: 'health_anxiety', label: 'Health Anxiety', icon: '🏥' },
  { value: 'sleep_problems', label: 'Sleep Problems', icon: '😴' },
  { value: 'eating_disorders', label: 'Eating Disorders', icon: '🍽️' },
  { value: 'anger_management', label: 'Anger Management', icon: '😤' },
];

export default function Signup() {
  const [step, setStep] = useState(1);
  const [phone, setPhone] = useState('');
  const [name, setName] = useState('');
  const [primaryProblem, setPrimaryProblem] = useState('');
  const [secondaryProblems, setSecondaryProblems] = useState([]);
  const [location, setLocation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const { setAuth } = useAuthStore();
  const navigate = useNavigate();

  // Get user location
  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition((position) => {
        setLocation({
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
        });
      });
    }
  }, []);

  const handleSignup = async () => {
    if (!phone || !name || !primaryProblem || !location) {
      setError('Please fill all fields');
      return;
    }

    setLoading(true);
    try {
      const response = await authAPI.signup({
        phone,
        name,
        primary_problem: primaryProblem,
        secondary_problems: secondaryProblems,
        latitude: location.latitude,
        longitude: location.longitude,
        address: 'Mumbai, India', // TODO: Get from location
        city: 'Mumbai',
        distance_preference: 10,
        timezone: 'Asia/Kolkata',
      });

      setAuth(response.data, response.data.access_token);
      navigate('/matches');
    } catch (err) {
      setError(err.response?.data?.detail || 'Signup failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-600 to-blue-600 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-xl p-8 max-w-md w-full">
        <h1 className="text-3xl font-bold text-purple-600 mb-2">SoulConnect</h1>
        <p className="text-gray-600 mb-6">Find your people, heal together</p>

        {/* Step Indicator */}
        <div className="flex gap-2 mb-8">
          {[1, 2, 3].map((s) => (
            <div
              key={s}
              className={`h-2 flex-1 rounded-full transition-all ${
                s <= step ? 'bg-purple-600' : 'bg-gray-300'
              }`}
            />
          ))}
        </div>

        {/* Step 1: Phone & Name */}
        {step === 1 && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Your Phone Number
            </label>
            <input
              type="tel"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              placeholder="9876543210"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg mb-4 focus:outline-none focus:border-purple-600"
            />

            <label className="block text-sm font-medium text-gray-700 mb-2">
              Your Name
            </label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="John Doe"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg mb-6 focus:outline-none focus:border-purple-600"
            />

            <button
              onClick={() => setStep(2)}
              className="w-full bg-purple-600 text-white py-2 rounded-lg font-semibold hover:bg-purple-700"
            >
              Next
            </button>
          </div>
        )}

        {/* Step 2: Primary Problem */}
        {step === 2 && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-4">
              What's your main problem?
            </label>

            <div className="grid grid-cols-2 gap-2 mb-6 max-h-64 overflow-y-auto">
              {PROBLEMS.map((prob) => (
                <button
                  key={prob.value}
                  onClick={() => setPrimaryProblem(prob.value)}
                  className={`p-3 rounded-lg text-sm text-center transition-all ${
                    primaryProblem === prob.value
                      ? 'bg-purple-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  <div className="text-lg">{prob.icon}</div>
                  <div className="text-xs">{prob.label}</div>
                </button>
              ))}
            </div>

            <div className="flex gap-3">
              <button
                onClick={() => setStep(1)}
                className="flex-1 bg-gray-300 text-gray-700 py-2 rounded-lg font-semibold hover:bg-gray-400"
              >
                Back
              </button>
              <button
                onClick={() => setStep(3)}
                disabled={!primaryProblem}
                className="flex-1 bg-purple-600 text-white py-2 rounded-lg font-semibold hover:bg-purple-700 disabled:opacity-50"
              >
                Next
              </button>
            </div>
          </div>
        )}

        {/* Step 3: Confirmation */}
        {step === 3 && (
          <div>
            <div className="bg-gray-100 p-4 rounded-lg mb-6">
              <p className="text-sm text-gray-600 mb-2">
                <strong>Phone:</strong> {phone}
              </p>
              <p className="text-sm text-gray-600 mb-2">
                <strong>Name:</strong> {name}
              </p>
              <p className="text-sm text-gray-600">
                <strong>Problem:</strong>{' '}
                {PROBLEMS.find((p) => p.value === primaryProblem)?.label}
              </p>
            </div>

            {error && (
              <div className="bg-red-100 text-red-700 p-3 rounded-lg mb-4 text-sm">
                {error}
              </div>
            )}

            <div className="flex gap-3">
              <button
                onClick={() => setStep(2)}
                className="flex-1 bg-gray-300 text-gray-700 py-2 rounded-lg font-semibold hover:bg-gray-400"
              >
                Back
              </button>
              <button
                onClick={handleSignup}
                disabled={loading}
                className="flex-1 bg-purple-600 text-white py-2 rounded-lg font-semibold hover:bg-purple-700 disabled:opacity-50"
              >
                {loading ? 'Creating...' : 'Create Account'}
              </button>
            </div>

            <p className="text-xs text-gray-500 text-center mt-4">
              By signing up, you agree to our Terms & Crisis Resources
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

---

# frontend/src/pages/Matches.jsx
# Matches Page - Find & Accept Matches

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { matchAPI } from '../services/api';

export default function Matches() {
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedMatch, setSelectedMatch] = useState(null);

  useEffect(() => {
    fetchMatches();
  }, []);

  const fetchMatches = async () => {
    setLoading(true);
    try {
      const response = await matchAPI.findMatches();
      setMatches(response.data.matches || []);
    } catch (err) {
      console.error('Error fetching matches:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAccept = async (userId) => {
    try {
      await matchAPI.acceptMatch(userId);
      setMatches(matches.filter((m) => m.id !== userId));
      // Redirect to chat
      const match = matches.find((m) => m.id === userId);
      if (match) {
        // Store match_id for chat
        alert('Match accepted! You can now chat.');
      }
    } catch (err) {
      console.error('Error accepting match:', err);
    }
  };

  if (loading) {
    return (
      <div className="max-w-2xl mx-auto px-4 py-8">
        <div className="text-center">
          <div className="animate-spin text-4xl mb-4">🔄</div>
          <p>Finding your match...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Find Your Match</h1>

      {matches.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-600 mb-4">No matches found yet.</p>
          <p className="text-gray-500">Come back in a few minutes!</p>
        </div>
      ) : (
        <div className="space-y-6">
          {matches.map((match) => (
            <div
              key={match.id}
              className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow"
            >
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-xl font-bold text-gray-800">{match.name}</h3>
                  <p className="text-gray-600">
                    {match.distance_km}km away • {match.city}
                  </p>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold text-purple-600">
                    {match.match_score}%
                  </div>
                  <p className="text-sm text-gray-500">Match</p>
                </div>
              </div>

              <div className="mb-4">
                <p className="text-sm font-semibold text-gray-700 mb-2">
                  {match.match_reason}
                </p>
                {match.problem_context && (
                  <p className="text-gray-600 italic text-sm">
                    "{match.problem_context}"
                  </p>
                )}
              </div>

              <div className="flex gap-3">
                <button className="flex-1 bg-gray-200 text-gray-700 py-2 rounded-lg font-semibold hover:bg-gray-300">
                  Skip
                </button>
                <button
                  onClick={() => handleAccept(match.id)}
                  className="flex-1 bg-purple-600 text-white py-2 rounded-lg font-semibold hover:bg-purple-700"
                >
                  Chat
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

---

# frontend/src/pages/Chat.jsx
# Chat Page - 1:1 Messaging

import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { chatAPI } from '../services/api';

export default function Chat() {
  const { matchId } = useParams();
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMessages();
  }, [matchId]);

  const fetchMessages = async () => {
    try {
      const response = await chatAPI.getHistory(matchId);
      setMessages(response.data.messages || []);
    } catch (err) {
      console.error('Error fetching messages:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSend = async () => {
    if (!newMessage.trim()) return;

    try {
      await chatAPI.sendMessage(matchId, newMessage);
      setNewMessage('');
      await fetchMessages();
    } catch (err) {
      console.error('Error sending message:', err);
    }
  };

  if (loading) {
    return <div className="text-center py-8">Loading chat...</div>;
  }

  return (
    <div className="max-w-2xl mx-auto px-4 py-8 h-[90vh] flex flex-col">
      <h1 className="text-2xl font-bold mb-4">Chat</h1>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto bg-gray-50 rounded-lg p-4 mb-4 space-y-4">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${msg.sender_id === 'current' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-xs px-4 py-2 rounded-lg ${
                msg.sender_id === 'current'
                  ? 'bg-purple-600 text-white'
                  : 'bg-gray-300 text-gray-800'
              }`}
            >
              {msg.message}
            </div>
          </div>
        ))}
      </div>

      {/* Input */}
      <div className="flex gap-2">
        <input
          type="text"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Type a message..."
          className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-purple-600"
        />
        <button
          onClick={handleSend}
          className="bg-purple-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-purple-700"
        >
          Send
        </button>
      </div>
    </div>
  );
}

---

# frontend/src/pages/Healers.jsx
# Healers Page - Browse & Book Sessions

import React, { useState, useEffect } from 'react';
import { healerAPI } from '../services/api';

export default function Healers() {
  const [healers, setHealers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedHealer, setSelectedHealer] = useState(null);

  useEffect(() => {
    fetchHealers();
  }, []);

  const fetchHealers = async () => {
    try {
      const response = await healerAPI.listHealers();
      setHealers(response.data.healers || []);
    } catch (err) {
      console.error('Error fetching healers:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-center py-8">Loading healers...</div>;
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Find a Healer</h1>

      <div className="grid md:grid-cols-2 gap-6">
        {healers.map((healer) => (
          <div key={healer.id} className="bg-white rounded-lg shadow-lg p-6">
            <div className="flex items-start gap-4 mb-4">
              {healer.avatar_url && (
                <img
                  src={healer.avatar_url}
                  alt={healer.name}
                  className="w-16 h-16 rounded-full"
                />
              )}
              <div>
                <h3 className="text-lg font-bold text-gray-800">{healer.name}</h3>
                <p className="text-yellow-500">
                  ⭐ {healer.rating.toFixed(1)} ({healer.review_count} reviews)
                </p>
              </div>
            </div>

            <p className="text-gray-600 text-sm mb-4">{healer.bio}</p>

            <div className="mb-4">
              <p className="text-sm font-semibold text-gray-700 mb-2">Specializations:</p>
              <div className="flex flex-wrap gap-2">
                {healer.specializations.map((spec) => (
                  <span key={spec} className="bg-purple-100 text-purple-700 px-2 py-1 rounded text-xs">
                    {spec}
                  </span>
                ))}
              </div>
            </div>

            <div className="flex justify-between items-center">
              <p className="font-bold text-lg text-gray-800">₹{healer.hourly_rate}/hr</p>
              <button className="bg-purple-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-purple-700">
                Book Session
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

---

# frontend/src/pages/Meetups.jsx
# Meetups Page - Browse & Join Events

import React, { useState, useEffect } from 'react';
import { meetupAPI } from '../services/api';

export default function Meetups() {
  const [meetups, setMeetups] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMeetups();
  }, []);

  const fetchMeetups = async () => {
    try {
      const response = await meetupAPI.listMeetups();
      setMeetups(response.data.meetups || []);
    } catch (err) {
      console.error('Error fetching meetups:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-center py-8">Loading meetups...</div>;
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Upcoming Meetups</h1>

      {meetups.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-600">No meetups scheduled yet.</p>
          <p className="text-purple-600 font-semibold">More coming soon!</p>
        </div>
      ) : (
        <div className="space-y-4">
          {meetups.map((meetup) => (
            <div key={meetup.id} className="bg-white rounded-lg shadow-lg p-6">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-lg font-bold text-gray-800">{meetup.title}</h3>
                  <p className="text-gray-600">📍 {meetup.location}</p>
                </div>
                <p className="text-yellow-500">⭐ {meetup.rating.toFixed(1)}</p>
              </div>

              <p className="text-gray-600 text-sm mb-4">{meetup.description}</p>

              <div className="grid grid-cols-2 gap-4 mb-4 text-sm">
                <div>
                  <p className="text-gray-500">Date & Time</p>
                  <p className="font-semibold text-gray-800">
                    {new Date(meetup.scheduled_time).toLocaleString()}
                  </p>
                </div>
                <div>
                  <p className="text-gray-500">Attendees</p>
                  <p className="font-semibold text-gray-800">
                    {meetup.attendees}/{meetup.max_attendees}
                  </p>
                </div>
              </div>

              <button className="w-full bg-purple-600 text-white py-2 rounded-lg font-semibold hover:bg-purple-700">
                Join Meetup
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

---

# frontend/src/pages/Premium.jsx
# Premium Page - Subscription

import React from 'react';

export default function Premium() {
  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Upgrade to Premium</h1>

      <div className="grid md:grid-cols-2 gap-8">
        {/* Free Tier */}
        <div className="bg-gray-50 rounded-lg p-8 border border-gray-300">
          <h2 className="text-2xl font-bold mb-4">Free</h2>
          <p className="text-gray-600 mb-6">Perfect for getting started</p>

          <p className="text-4xl font-bold mb-6">₹0<span className="text-lg text-gray-600">/month</span></p>

          <ul className="space-y-3 mb-6">
            <li className="flex items-center gap-2">
              <span className="text-green-600">✓</span>
              <span>Unlimited peer matching</span>
            </li>
            <li className="flex items-center gap-2">
              <span className="text-green-600">✓</span>
              <span>1:1 chat</span>
            </li>
            <li className="flex items-center gap-2">
              <span className="text-green-600">✓</span>
              <span>Browse healers</span>
            </li>
            <li className="flex items-center gap-2">
              <span className="text-gray-400">✗</span>
              <span className="text-gray-400">Priority matching</span>
            </li>
            <li className="flex items-center gap-2">
              <span className="text-gray-400">✗</span>
              <span className="text-gray-400">Unlimited meetups</span>
            </li>
          </ul>

          <button disabled className="w-full bg-gray-300 text-gray-600 py-3 rounded-lg font-semibold cursor-default">
            Current Plan
          </button>
        </div>

        {/* Premium Tier */}
        <div className="bg-purple-600 text-white rounded-lg p-8 shadow-xl border-2 border-purple-600 relative">
          <div className="absolute top-4 right-4 bg-yellow-400 text-purple-600 px-3 py-1 rounded-full text-xs font-bold">
            POPULAR
          </div>

          <h2 className="text-2xl font-bold mb-4">Premium</h2>
          <p className="mb-6">Unlock full potential</p>

          <p className="text-4xl font-bold mb-6">₹299<span className="text-lg opacity-90">/month</span></p>

          <ul className="space-y-3 mb-6">
            <li className="flex items-center gap-2">
              <span>✓</span>
              <span>Priority matching (10 min)</span>
            </li>
            <li className="flex items-center gap-2">
              <span>✓</span>
              <span>Unlimited meetups</span>
            </li>
            <li className="flex items-center gap-2">
              <span>✓</span>
              <span>20% healer discounts</span>
            </li>
            <li className="flex items-center gap-2">
              <span>✓</span>
              <span>Expand search (50km)</span>
            </li>
            <li className="flex items-center gap-2">
              <span>✓</span>
              <span>Progress tracking</span>
            </li>
            <li className="flex items-center gap-2">
              <span>✓</span>
              <span>Ad-free experience</span>
            </li>
          </ul>

          <button className="w-full bg-white text-purple-600 py-3 rounded-lg font-semibold hover:bg-gray-100">
            Upgrade Now
          </button>

          <p className="text-xs opacity-75 text-center mt-4">
            Cancel anytime. No questions asked.
          </p>
        </div>
      </div>
    </div>
  );
}

---

# frontend/src/pages/Account.jsx
# Account Page - Profile & Settings

import React, { useState, useEffect } from 'react';
import { useAuthStore } from '../store/auth';
import { userAPI } from '../services/api';

export default function Account() {
  const { user, logout } = useAuthStore();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const response = await userAPI.getProfile();
      setProfile(response.data);
    } catch (err) {
      console.error('Error fetching profile:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-center py-8">Loading profile...</div>;
  }

  return (
    <div className="max-w-2xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">My Account</h1>

      <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
        <h2 className="text-lg font-bold mb-4">Profile</h2>

        <div className="space-y-4">
          <div>
            <p className="text-gray-600 text-sm">Name</p>
            <p className="text-lg font-semibold">{profile?.name}</p>
          </div>

          <div>
            <p className="text-gray-600 text-sm">Phone</p>
            <p className="text-lg font-semibold">{profile?.phone}</p>
          </div>

          <div>
            <p className="text-gray-600 text-sm">Main Issue</p>
            <p className="text-lg font-semibold">{profile?.primary_problem}</p>
          </div>

          <div>
            <p className="text-gray-600 text-sm">City</p>
            <p className="text-lg font-semibold">{profile?.city}</p>
          </div>
        </div>

        <button className="mt-6 w-full bg-purple-600 text-white py-2 rounded-lg font-semibold hover:bg-purple-700">
          Edit Profile
        </button>
      </div>

      <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
        <h2 className="text-lg font-bold mb-4">Subscriptions</h2>
        <p className="text-gray-600 mb-4">No active subscriptions</p>
        <button className="w-full bg-purple-600 text-white py-2 rounded-lg font-semibold hover:bg-purple-700">
          Upgrade to Premium
        </button>
      </div>

      <button
        onClick={() => {
          logout();
          window.location.href = '/';
        }}
        className="w-full bg-red-600 text-white py-2 rounded-lg font-semibold hover:bg-red-700"
      >
        Logout
      </button>
    </div>
  );
}

---

# frontend/src/components/Navbar.jsx
# Navigation Component

import React from 'react';
import { Link, useLocation } from 'react-router-dom';

export default function Navbar() {
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  return (
    <nav className="bg-white shadow-md sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
        <Link to="/matches" className="text-2xl font-bold text-purple-600">
          🌟 SoulConnect
        </Link>

        <div className="flex gap-6">
          <Link
            to="/matches"
            className={`font-semibold ${isActive('/matches') ? 'text-purple-600' : 'text-gray-600 hover:text-purple-600'}`}
          >
            Matches
          </Link>
          <Link
            to="/healers"
            className={`font-semibold ${isActive('/healers') ? 'text-purple-600' : 'text-gray-600 hover:text-purple-600'}`}
          >
            Healers
          </Link>
          <Link
            to="/meetups"
            className={`font-semibold ${isActive('/meetups') ? 'text-purple-600' : 'text-gray-600 hover:text-purple-600'}`}
          >
            Meetups
          </Link>
          <Link
            to="/premium"
            className={`font-semibold ${isActive('/premium') ? 'text-purple-600' : 'text-gray-600 hover:text-purple-600'}`}
          >
            Premium
          </Link>
          <Link
            to="/account"
            className={`font-semibold ${isActive('/account') ? 'text-purple-600' : 'text-gray-600 hover:text-purple-600'}`}
          >
            Account
          </Link>
        </div>
      </div>
    </nav>
  );
}

---

# frontend/src/components/CrisisResources.jsx
# Crisis Resources - Floating Button

import React, { useState } from 'react';

export default function CrisisResources() {
  const [showResources, setShowResources] = useState(false);

  const resources = [
    { name: 'AASRA (India)', phone: '9820466726', country: 'India' },
    { name: 'iCall (India)', phone: '9152987821', country: 'India' },
    { name: 'Vandrevala Foundation', phone: '9999666555', country: 'India' },
    { name: 'Suicide & Crisis Lifeline (US)', phone: '988', country: 'US' },
    { name: 'Samaritans (UK)', phone: '116123', country: 'UK' },
  ];

  return (
    <>
      {/* Floating Button */}
      <button
        onClick={() => setShowResources(!showResources)}
        className="fixed bottom-6 right-6 w-14 h-14 bg-red-600 text-white rounded-full flex items-center justify-center font-bold text-2xl shadow-lg hover:bg-red-700 z-40"
        title="Crisis Help"
      >
        🆘
      </button>

      {/* Modal */}
      {showResources && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-xl p-6 max-w-md w-full">
            <h2 className="text-xl font-bold text-red-600 mb-4">Crisis Resources</h2>

            <div className="space-y-3 mb-6">
              {resources.map((resource, i) => (
                <div key={i} className="border border-gray-200 p-3 rounded-lg">
                  <p className="font-semibold text-gray-800">{resource.name}</p>
                  <p className="text-red-600 font-bold text-lg">{resource.phone}</p>
                  <p className="text-xs text-gray-500">{resource.country}</p>
                </div>
              ))}
            </div>

            <p className="text-sm text-gray-600 mb-4">
              <strong>In immediate danger?</strong> Call your local emergency services (911 in US, 100 in India).
            </p>

            <button
              onClick={() => setShowResources(false)}
              className="w-full bg-gray-300 text-gray-700 py-2 rounded-lg font-semibold hover:bg-gray-400"
            >
              Close
            </button>
          </div>
        </div>
      )}
    </>
  );
}
