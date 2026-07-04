import React from 'react';

export default function VictoryStage({ problemType, matchName, stageData, conversationHistory, onBack }) {
  return (
    <div className="space-y-6">
      <div className="text-center">
        <p className="text-6xl mb-4">🌟</p>
        <h2 className="text-3xl font-bold text-gray-800 mb-2">You Did It!</h2>
        <p className="text-gray-600 text-lg">
          You just went through a complete healing journey with {matchName}
        </p>
      </div>

      {/* Your Journey Summary */}
      <div className="bg-gradient-to-r from-purple-50 to-pink-50 border-2 border-purple-300 rounded-lg p-6">
        <h3 className="text-xl font-bold text-purple-700 mb-4">Your Healing Journey</h3>

        <div className="space-y-3">
          <div className="bg-white p-4 rounded-lg border-l-4 border-blue-600">
            <p className="text-gray-600 text-sm">Stage 1: Mirror</p>
            <p className="text-gray-800 font-semibold">You were heard and validated</p>
          </div>

          <div className="bg-white p-4 rounded-lg border-l-4 border-purple-600">
            <p className="text-gray-600 text-sm">Stage 2: Explorer</p>
            <p className="text-gray-800 font-semibold">You discovered the root of your pain</p>
          </div>

          <div className="bg-white p-4 rounded-lg border-l-4 border-yellow-600">
            <p className="text-gray-600 text-sm">Stage 3: Reframer</p>
            <p className="text-gray-800 font-semibold">You shifted your perspective</p>
          </div>

          <div className="bg-white p-4 rounded-lg border-l-4 border-green-600">
            <p className="text-gray-600 text-sm">Stage 4: Action Partner</p>
            <p className="text-gray-800 font-semibold">You committed to change</p>
          </div>
        </div>
      </div>

      {/* What Happens Next */}
      <div className="bg-blue-50 border-2 border-blue-300 rounded-lg p-6">
        <h3 className="text-xl font-bold text-blue-700 mb-4">What Happens Next?</h3>

        <div className="space-y-3 text-gray-700">
          <p className="flex gap-3">
            <span className="text-2xl">📅</span>
            <span><strong>Check-Ins:</strong> Every 3 days, you and {matchName} check if you did your actions</span>
          </p>

          <p className="flex gap-3">
            <span className="text-2xl">📈</span>
            <span><strong>Progress Tracking:</strong> Watch your mood improve as you take action</span>
          </p>

          <p className="flex gap-3">
            <span className="text-2xl">🎉</span>
            <span><strong>Weekly Victory:</strong> Celebrate your wins together. Small wins = big momentum</span>
          </p>

          <p className="flex gap-3">
            <span className="text-2xl">🤝</span>
            <span><strong>Deeper Connection:</strong> As you both heal, your bond strengthens</span>
          </p>
        </div>
      </div>

      {/* Immediate Actions */}
      <div className="bg-green-50 border-2 border-green-300 rounded-lg p-6">
        <h3 className="text-xl font-bold text-green-700 mb-4">Today\'s Next Steps</h3>

        <div className="space-y-3">
          <button className="w-full bg-green-600 text-white py-3 rounded-lg font-semibold hover:bg-green-700">
            💬 Chat with {matchName} about this
          </button>

          <button className="w-full bg-white border-2 border-green-600 text-green-600 py-3 rounded-lg font-semibold hover:bg-green-50">
            📊 View Progress Dashboard
          </button>

          <button className="w-full bg-white border-2 border-green-600 text-green-600 py-3 rounded-lg font-semibold hover:bg-green-50">
            🎯 Start First Action Today
          </button>
        </div>
      </div>

      {/* Inspiration */}
      <div className="bg-white border-2 border-gray-300 rounded-lg p-6 text-center">
        <p className="text-2xl mb-3">💪</p>
        <p className="text-gray-800 font-semibold text-lg">
          "The fact that you went through this journey means you\'re already changing."
        </p>
        <p className="text-gray-600 mt-2">
          — {matchName}, your healing partner
        </p>
      </div>

      <button
        onClick={onBack}
        className="w-full bg-gray-600 text-white py-3 rounded-lg font-semibold hover:bg-gray-700"
      >
        Explore More or Go Back to Chat
      </button>
    </div>
  );
}