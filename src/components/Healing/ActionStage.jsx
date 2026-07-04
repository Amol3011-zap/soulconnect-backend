import React, { useState } from 'react';

const ACTIONS_BY_PROBLEM = {
  'relationship_breakup': [
    { action: 'Take a 20-min walk', benefit: 'Dopamine boost' },
    { action: 'Journal: What did I learn?', benefit: 'Processing' },
    { action: 'Call a friend (not them)', benefit: 'Connection' },
    { action: 'Do something that makes you feel alive', benefit: 'Joy' }
  ],
  'anxiety': [
    { action: '4-7-8 Breathing (2x daily)', benefit: 'Calm nervous system' },
    { action: 'Cold shower (1 min)', benefit: 'Reset body' },
    { action: 'Walk outside (15 min)', benefit: 'Serotonin' },
    { action: 'Journal your anxieties', benefit: 'Externalize' }
  ],
  'depression': [
    { action: 'Walk (20 min)', benefit: 'Dopamine' },
    { action: 'Gratitude list (3 items)', benefit: 'Perspective' },
    { action: 'One small task', benefit: 'Achievement' },
    { action: 'Reach out to someone', benefit: 'Connection' }
  ],
  'loneliness': [
    { action: 'Call/text someone', benefit: 'Connection' },
    { action: 'Volunteer (1 hour)', benefit: 'Purpose' },
    { action: 'Join a group activity', benefit: 'Belonging' },
    { action: 'Pet or nature time', benefit: 'Bonding' }
  ]
};

export default function ActionStage({ problemType, matchName, onComplete, onBack, stageData }) {
  const [selectedActions, setSelectedActions] = useState([]);
  const [step, setStep] = useState('select'); // select, commit, tracking

  const actions = ACTIONS_BY_PROBLEM[problemType] || ACTIONS_BY_PROBLEM['anxiety'];

  const handleSelectAction = (action) => {
    if (selectedActions.includes(action)) {
      setSelectedActions(selectedActions.filter(a => a !== action));
    } else {
      setSelectedActions([...selectedActions, action]);
    }
  };

  const handleCommit = () => {
    if (selectedActions.length === 0) return;
    setStep('commit');
  };

  const handleAcceptCommitment = () => {
    setStep('tracking');
    setTimeout(() => {
      onComplete({
        stage: 'action',
        commitment: selectedActions,
        committedAt: new Date()
      });
    }, 2000);
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-800 mb-2">💪 Building Your Action Plan</h2>
        <p className="text-gray-600">We\'re not just talking. We\'re doing. Together.</p>
      </div>

      {step === 'select' && (
        <div className="bg-gradient-to-r from-green-50 to-emerald-50 border-2 border-green-300 rounded-lg p-6">
          <p className="text-gray-800 font-semibold mb-4">
            This week, commit to doing:
          </p>

          <div className="space-y-3 mb-6">
            {actions.map((item, idx) => (
              <button
                key={idx}
                onClick={() => handleSelectAction(item.action)}
                className={`w-full p-4 rounded-lg border-2 text-left transition-all ${
                  selectedActions.includes(item.action)
                    ? 'bg-green-600 text-white border-green-600'
                    : 'bg-white border-green-300 text-gray-800 hover:border-green-600'
                }`}
              >
                <div className="flex justify-between items-start">
                  <div>
                    <p className="font-semibold">{item.action}</p>
                    <p className={`text-sm ${selectedActions.includes(item.action) ? 'text-green-100' : 'text-gray-600'}`}>
                      {item.benefit}
                    </p>
                  </div>
                  <span className="text-xl">
                    {selectedActions.includes(item.action) ? '✅' : '☐'}
                  </span>
                </div>
              </button>
            ))}
          </div>

          <button
            onClick={handleCommit}
            disabled={selectedActions.length === 0}
            className="w-full bg-gradient-to-r from-green-600 to-emerald-600 text-white py-3 rounded-lg font-semibold hover:opacity-90 disabled:opacity-50"
          >
            {selectedActions.length === 0 
              ? 'Select at least one action' 
              : `Commit to ${selectedActions.length} Action${selectedActions.length > 1 ? 's' : ''}`}
          </button>
        </div>
      )}

      {step === 'commit' && (
        <div className="bg-blue-50 border-2 border-blue-300 rounded-lg p-6">
          <h3 className="text-xl font-bold text-blue-800 mb-4">
            {matchName} & You: Weekly Commitment
          </h3>

          <div className="bg-white p-4 rounded-lg mb-6 border-l-4 border-blue-600">
            <p className="text-blue-700 font-semibold mb-3">We commit to:</p>
            <ul className="space-y-2">
              {selectedActions.map((action, idx) => (
                <li key={idx} className="text-gray-700 flex gap-2">
                  <span>✓</span>
                  <span>{action}</span>
                </li>
              ))}
            </ul>
          </div>

          <div className="bg-yellow-50 p-4 rounded-lg mb-6 border-l-4 border-yellow-500">
            <p className="text-yellow-800 font-semibold mb-2">Check-in Schedule:</p>
            <p className="text-yellow-700 text-sm">
              We\'ll check in every 3 days. Did you do it? How did it feel?
            </p>
          </div>

          <button
            onClick={handleAcceptCommitment}
            className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 rounded-lg font-semibold hover:opacity-90"
          >
            I\'m Ready. Let\'s Go! 🚀
          </button>
        </div>
      )}

      {step === 'tracking' && (
        <div className="bg-green-100 border-2 border-green-500 rounded-lg p-6 text-center">
          <p className="text-3xl mb-2">🎯</p>
          <p className="text-green-700 font-bold text-lg">Commitment Locked!</p>
          <p className="text-green-600 text-sm mt-2">
            You\'re ready to take action. Let\'s change your life together.
          </p>
        </div>
      )}

      <button
        onClick={onBack}
        className="text-blue-600 hover:text-blue-800 text-sm font-semibold"
      >
        ← Go Back
      </button>
    </div>
  );
}