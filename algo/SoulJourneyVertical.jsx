import React, { useState, useEffect } from 'react';
import axios from 'axios';

const SoulJourneyVertical = ({ userId }) => {
  const [progress, setProgress] = useState(null);
  const [loading, setLoading] = useState(true);

  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  // Updated stage definitions to match your new design
  const stages = [
    {
      id: 'awareness',
      number: 1,
      name: 'Awareness',
      description: 'Awakening to the journey',
      icon: '✓',
      iconBg: 'bg-teal-500',
      iconColor: 'text-white',
      status: 'completed'
    },
    {
      id: 'healing',
      number: 2,
      name: 'Healing',
      description: 'Processing and releasing',
      icon: '🌙',
      iconBg: 'bg-purple-600',
      iconColor: 'text-white',
      status: 'current',
      badge: 'You are here'
    },
    {
      id: 'growth',
      number: 3,
      name: 'Growth',
      description: 'Expanding your awareness',
      icon: '🔒',
      iconBg: 'bg-gray-600',
      iconColor: 'text-orange-300',
      status: 'locked'
    },
    {
      id: 'transformation',
      number: 4,
      name: 'Transformation',
      description: 'Becoming your true self',
      icon: '🔒',
      iconBg: 'bg-gray-600',
      iconColor: 'text-orange-300',
      status: 'locked'
    },
    {
      id: 'awakening',
      number: 5,
      name: 'Awakening',
      description: 'Living in alignment',
      icon: '🔒',
      iconBg: 'bg-gray-600',
      iconColor: 'text-orange-300',
      status: 'locked'
    }
  ];

  // Fetch progress data
  useEffect(() => {
    const fetchProgress = async () => {
      try {
        setLoading(true);
        const response = await axios.get(
          `${API_BASE_URL}/api/v1/journey/${userId}/progress`,
          {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('authToken')}` // or however you store token
            }
          }
        );
        setProgress(response.data);
      } catch (error) {
        console.error('Error fetching progress:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchProgress();
    const interval = setInterval(fetchProgress, 30000);
    return () => clearInterval(interval);
  }, [userId]);

  // Map API stage to display stage
  const getCurrentStageIndex = () => {
    if (!progress) return 0;
    const stageMap = {
      'awareness': 0,
      'beginning': 0,
      'healing': 1,
      'growth': 2,
      'transformation': 3,
      'awakening': 4,
      'inner_harmony': 4
    };
    return stageMap[progress.current_stage] || 0;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-400 mx-auto mb-4"></div>
          <p className="text-gray-400">Loading your journey...</p>
        </div>
      </div>
    );
  }

  const currentStageIndex = getCurrentStageIndex();
  const currentStage = stages[currentStageIndex];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 p-8">
      <div className="max-w-2xl mx-auto">
        {/* Header */}
        <div className="mb-12">
          <div className="flex items-center gap-3 mb-4">
            <span className="text-3xl">✨</span>
            <h1 className="text-3xl md:text-4xl font-bold text-white">Soul Journey</h1>
          </div>
          <p className="text-gray-400 text-lg">
            Stage {currentStageIndex + 1} of {stages.length}: <span className="text-purple-300 font-semibold">{currentStage.name}</span>
          </p>
        </div>

        {/* Vertical Timeline */}
        <div className="relative">
          {/* Vertical line */}
          <div 
            className="absolute left-8 top-0 bottom-0 w-0.5 bg-gradient-to-b from-purple-600 to-gray-700"
            style={{
              height: `${((currentStageIndex + 1) / stages.length) * 100}%`
            }}
          ></div>
          <div 
            className="absolute left-8 top-0 bottom-0 w-0.5 bg-gray-700"
            style={{
              top: `${((currentStageIndex + 1) / stages.length) * 100}%`
            }}
          ></div>

          {/* Stages */}
          <div className="space-y-12">
            {stages.map((stage, index) => {
              const isCompleted = index < currentStageIndex;
              const isCurrent = index === currentStageIndex;
              const isLocked = index > currentStageIndex;

              return (
                <div key={stage.id} className="relative pl-24">
                  {/* Stage Icon */}
                  <div className="absolute left-0 top-0 flex items-center justify-center">
                    <div 
                      className={`w-16 h-16 rounded-full ${stage.iconBg} flex items-center justify-center text-2xl transition-all duration-300 ${
                        isCurrent ? 'ring-4 ring-purple-400 scale-110' : ''
                      }`}
                    >
                      <span className={`${stage.iconColor}`}>{stage.icon}</span>
                    </div>
                  </div>

                  {/* Stage Content */}
                  <div className={`pb-4 transition-opacity ${isLocked ? 'opacity-60' : 'opacity-100'}`}>
                    <div className="flex items-start justify-between mb-2">
                      <div>
                        <h3 className={`text-xl font-semibold ${
                          isCompleted ? 'text-teal-400' :
                          isCurrent ? 'text-white' :
                          'text-gray-500'
                        }`}>
                          {stage.name}
                        </h3>
                        <p className={`text-sm ${
                          isCompleted ? 'text-teal-300' :
                          isCurrent ? 'text-gray-300' :
                          'text-gray-600'
                        }`}>
                          {stage.description}
                        </p>
                      </div>

                      {/* Status Badge */}
                      {isCurrent && (
                        <div className="bg-purple-600 text-white text-xs px-3 py-1 rounded-full whitespace-nowrap ml-4">
                          {stage.badge}
                        </div>
                      )}
                      {isCompleted && (
                        <div className="text-teal-400 text-sm font-semibold ml-4">
                          Completed
                        </div>
                      )}
                    </div>

                    {/* Progress bar for current stage */}
                    {isCurrent && progress && (
                      <div className="mt-3">
                        <div className="flex justify-between items-center mb-2">
                          <span className="text-xs text-gray-400">Stage Progress</span>
                          <span className="text-sm font-semibold text-purple-300">
                            {Math.round(progress.stage_progress)}%
                          </span>
                        </div>
                        <div className="w-full bg-gray-700 rounded-full h-2 overflow-hidden">
                          <div
                            className="bg-gradient-to-r from-purple-500 to-purple-600 h-full transition-all duration-500"
                            style={{ width: `${progress.stage_progress}%` }}
                          ></div>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* View Full Journey Button */}
        <button className="w-full mt-12 border-2 border-purple-500 hover:border-purple-400 text-purple-300 hover:text-purple-200 font-semibold py-3 px-4 rounded-lg transition-all duration-300 hover:bg-purple-500 hover:bg-opacity-10">
          View Full Journey
        </button>

        {/* Stats Footer */}
        {progress && (
          <div className="mt-12 grid grid-cols-3 gap-4 pt-8 border-t border-gray-700">
            <div className="text-center">
              <p className="text-gray-400 text-sm mb-1">Wellness Score</p>
              <p className="text-2xl font-bold text-teal-400">{progress.overall_wellness_score}</p>
            </div>
            <div className="text-center">
              <p className="text-gray-400 text-sm mb-1">Weekly Growth</p>
              <p className="text-2xl font-bold text-purple-400">
                {progress.weekly_growth_percentage > 0 ? '+' : ''}{Math.round(progress.weekly_growth_percentage)}%
              </p>
            </div>
            <div className="text-center">
              <p className="text-gray-400 text-sm mb-1">Total Activities</p>
              <p className="text-2xl font-bold text-gray-300">{progress.total_activities}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default SoulJourneyVertical;
