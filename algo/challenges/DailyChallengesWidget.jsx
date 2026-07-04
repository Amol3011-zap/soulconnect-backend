import React, { useState, useEffect } from 'react';
import axios from 'axios';

const DailyChallengesWidget = ({ userId }) => {
  const [progress, setProgress] = useState(null);
  const [loading, setLoading] = useState(true);

  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  // Fetch challenges on mount
  useEffect(() => {
    const fetchChallenges = async () => {
      try {
        setLoading(true);
        const response = await axios.get(
          `${API_BASE_URL}/api/v1/challenges/${userId}/today`,
          {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('authToken')}`
            }
          }
        );
        setProgress(response.data);
      } catch (error) {
        console.error('Error fetching challenges:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchChallenges();
  }, [userId]);

  const handleCompleteChallenge = async (challengeId) => {
    try {
      const response = await axios.post(
        `${API_BASE_URL}/api/v1/challenges/${userId}/complete/${challengeId}`,
        {},
        {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('authToken')}`
          }
        }
      );

      // Update local state
      setProgress(prev => ({
        ...prev,
        challenges: prev.challenges.map(c =>
          c.id === challengeId ? { ...c, completed: true } : c
        ),
        total_points: response.data.total_points,
        current_streak: response.data.current_streak
      }));

      // Show success toast
      console.log(`Challenge completed! +${response.data.total_points} points`);
    } catch (error) {
      console.error('Error completing challenge:', error);
    }
  };

  if (loading) {
    return (
      <div className="bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 rounded-xl p-6 animate-pulse">
        <div className="h-8 bg-gray-700 rounded w-1/3 mb-4"></div>
        <div className="space-y-4">
          {[1, 2, 3].map(i => (
            <div key={i} className="h-20 bg-gray-700 rounded"></div>
          ))}
        </div>
      </div>
    );
  }

  if (!progress) {
    return <div className="text-gray-400">Failed to load challenges</div>;
  }

  const { challenges, completed, total, current_streak, points_remaining } = progress;

  return (
    <div className="bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 rounded-xl p-6 text-white">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <span className="text-2xl">⚡</span>
            <h2 className="text-2xl font-bold">Daily Challenges</h2>
          </div>
          <p className="text-gray-400">Complete 3 challenges to earn 150 Soul Points</p>
        </div>
        <div className="text-right">
          <p className="text-sm text-gray-400">Streak</p>
          <p className="text-2xl font-bold text-orange-400">
            {current_streak}
            <span className="text-lg ml-1">🔥</span>
          </p>
        </div>
      </div>

      {/* Challenges List */}
      <div className="space-y-3 mb-6">
        {challenges.map((challenge, index) => (
          <ChallengeCard
            key={challenge.id}
            challenge={challenge}
            onComplete={() => handleCompleteChallenge(challenge.id)}
          />
        ))}
      </div>

      {/* Progress Summary */}
      <div className="text-sm text-gray-400 mb-4">
        {completed} of {total} completed · {points_remaining} pts remaining
      </div>

      {/* View All Challenges Button */}
      <button className="w-full border-2 border-purple-500 hover:border-purple-400 text-purple-300 hover:text-purple-200 font-semibold py-3 px-4 rounded-lg transition-all duration-300 hover:bg-purple-500 hover:bg-opacity-10">
        View All Challenges →
      </button>
    </div>
  );
};

// Individual Challenge Card Component
const ChallengeCard = ({ challenge, onComplete }) => {
  const [isLoading, setIsLoading] = useState(false);

  const handleClick = async () => {
    if (!challenge.completed) {
      setIsLoading(true);
      await onComplete();
      setIsLoading(false);
    }
  };

  return (
    <div
      onClick={handleClick}
      className={`
        border-2 rounded-lg p-4 transition-all duration-300 cursor-pointer
        ${challenge.completed
          ? 'border-teal-500 bg-teal-500 bg-opacity-10'
          : 'border-gray-700 bg-gray-800 bg-opacity-50 hover:border-gray-600 hover:bg-opacity-70'
        }
      `}
    >
      <div className="flex items-center justify-between">
        {/* Left Section: Icon, Name, Streak */}
        <div className="flex items-center gap-4 flex-1">
          {/* Status Circle */}
          <div className="relative w-12 h-12">
            {challenge.completed ? (
              <div className="w-full h-full rounded-full bg-teal-500 flex items-center justify-center text-white text-lg">
                ✓
              </div>
            ) : (
              <div className="w-full h-full rounded-full border-2 border-gray-600 flex items-center justify-center">
                <span className="text-lg opacity-50">{challenge.icon || '○'}</span>
              </div>
            )}
          </div>

          {/* Challenge Info */}
          <div className="flex-1">
            <h3 className="font-semibold text-white">{challenge.name}</h3>
            <p className="text-sm text-gray-400">
              {challenge.completed ? (
                <span className="text-teal-400 flex items-center gap-1">
                  {challenge.duration > 0 ? `${challenge.duration} min` : 'Tap to start'}
                </span>
              ) : (
                <>
                  {challenge.duration > 0 ? `${challenge.duration} min` : 'Tap to start'}
                  {challenge.streak_bonus > 0 && (
                    <span className="ml-2">🔥 Day {Math.ceil(challenge.streak_bonus / 5)} streak</span>
                  )}
                </>
              )}
            </p>
          </div>
        </div>

        {/* Points Badge */}
        <div className="text-right">
          <div className={`
            px-3 py-1 rounded-full font-semibold text-sm whitespace-nowrap
            ${challenge.completed
              ? 'bg-teal-500 text-white'
              : 'bg-gray-700 text-gray-300'
            }
          `}>
            +{challenge.points} pts
          </div>
        </div>
      </div>

      {/* Loading State */}
      {isLoading && (
        <div className="absolute inset-0 bg-black bg-opacity-50 rounded-lg flex items-center justify-center">
          <div className="animate-spin rounded-full h-6 w-6 border-2 border-white border-t-purple-500"></div>
        </div>
      )}
    </div>
  );
};

export default DailyChallengesWidget;
