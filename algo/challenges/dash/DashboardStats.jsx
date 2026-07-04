import React, { useState, useEffect } from 'react';
import axios from 'axios';

/**
 * Dashboard Statistics Widget
 * Shows: Healing Streak, Live Souls Healing, Soul Points, Healing Sessions
 */
const DashboardStats = ({ userId }) => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  // Fetch dashboard stats
  useEffect(() => {
    const fetchStats = async () => {
      try {
        setLoading(true);
        const response = await axios.get(
          `${API_BASE_URL}/api/v1/dashboard/${userId}/stats`,
          {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('authToken')}`
            }
          }
        );
        setStats(response.data);
      } catch (error) {
        console.error('Error fetching dashboard stats:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
    
    // Refresh every 30 seconds (for live count)
    const interval = setInterval(fetchStats, 30000);
    return () => clearInterval(interval);
  }, [userId]);

  if (loading || !stats) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {[1, 2, 3, 4].map(i => (
          <div 
            key={i} 
            className="bg-gradient-to-br from-purple-900 to-purple-800 rounded-xl p-6 animate-pulse h-40"
          >
            <div className="h-12 bg-gray-700 rounded w-1/3 mb-4"></div>
            <div className="h-8 bg-gray-700 rounded w-1/2"></div>
          </div>
        ))}
      </div>
    );
  }

  const { 
    healing_streak, 
    souls_healing, 
    soul_points, 
    healing_sessions 
  } = stats;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {/* Card 1: Healing Streak */}
      <StatCard
        icon={healing_streak.icon}
        mainValue={healing_streak.current}
        mainLabel={healing_streak.label}
        subtitle={`Best: ${healing_streak.best} days`}
        accentColor="from-orange-600 to-red-700"
      />

      {/* Card 2: Souls Healing (Live) */}
      <StatCard
        icon={souls_healing.icon}
        mainValue={souls_healing.count.toLocaleString()}
        mainLabel={souls_healing.label}
        isLive={souls_healing.live}
        accentColor="from-teal-600 to-green-700"
      />

      {/* Card 3: Soul Points & Level */}
      <StatCard
        icon={soul_points.icon}
        mainValue={soul_points.current}
        mainLabel={soul_points.label}
        levelInfo={{
          current: soul_points.level,
          next: soul_points.next_level,
          progress: soul_points.progress,
          remaining: soul_points.to_next
        }}
        accentColor="from-purple-600 to-purple-700"
      />

      {/* Card 4: Healing Sessions */}
      <StatCard
        icon={healing_sessions.icon}
        mainValue={healing_sessions.total}
        mainLabel={healing_sessions.label}
        subtitle={`This week: ${healing_sessions.change_display} from last`}
        accentColor="from-yellow-600 to-orange-700"
      />
    </div>
  );
};

/**
 * Individual Stat Card Component
 */
const StatCard = ({ 
  icon, 
  mainValue, 
  mainLabel, 
  subtitle,
  levelInfo,
  isLive,
  accentColor 
}) => {
  return (
    <div className={`
      relative bg-gradient-to-br ${accentColor} 
      rounded-2xl p-6 text-white overflow-hidden
      border border-white border-opacity-10
      transition-all duration-300 hover:shadow-lg
      min-h-48 flex flex-col justify-between
    `}>
      {/* Animated background gradient */}
      <div className="absolute inset-0 bg-gradient-to-t from-black from-0% to-transparent to-100% opacity-40"></div>

      {/* Content */}
      <div className="relative z-10">
        {/* Icon */}
        <div className="text-4xl mb-4 opacity-80">
          {icon}
        </div>

        {/* Main Value */}
        <h3 className="text-5xl font-bold mb-1 leading-tight">
          {mainValue}
        </h3>

        {/* Main Label */}
        <p className="text-lg font-semibold text-gray-200 mb-3">
          {mainLabel}
        </p>

        {/* Level Info (if applicable) */}
        {levelInfo && (
          <div className="mt-4 space-y-2">
            <p className="text-sm text-gray-300">
              Level {levelInfo.current} · {levelInfo.remaining} pts to Level {levelInfo.next}
            </p>
            <div className="w-full bg-black bg-opacity-30 rounded-full h-2 overflow-hidden">
              <div
                className="bg-gradient-to-r from-yellow-400 to-yellow-500 h-full transition-all duration-500"
                style={{ width: `${Math.min(levelInfo.progress, 100)}%` }}
              ></div>
            </div>
          </div>
        )}

        {/* Live Indicator (if applicable) */}
        {isLive && (
          <div className="flex items-center gap-2 mt-3">
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
            <span className="text-sm text-green-400 font-semibold">LIVE</span>
          </div>
        )}

        {/* Subtitle */}
        {subtitle && !levelInfo && (
          <p className="text-sm text-gray-400 mt-3">
            {subtitle}
          </p>
        )}
      </div>
    </div>
  );
};

export default DashboardStats;
