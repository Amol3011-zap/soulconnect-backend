import React, { useState } from 'react';

const REFRAMES = {
  'relationship_breakup': [
    {
      belief: 'They left me. I\'m unlovable.',
      reframe: 'They were the wrong person for you. That makes you smart, not unlovable.',
      why: 'Rejection of you ≠ rejection of your worth'
    },
    {
      belief: 'I\'ll never love again.',
      reframe: 'You\'ll love differently and better next time. You know more about yourself now.',
      why: 'Every heartbreak is practice for a healthy relationship'
    },
    {
      belief: 'I should have known better.',
      reframe: 'You learned something valuable. That\'s growth, not failure.',
      why: 'Hindsight is 20/20. You did the best you could with what you knew'
    },
    {
      belief: 'I\'m too broken for someone new.',
      reframe: 'You\'re not broken. You\'re healing. And that makes you strong.',
      why: 'Vulnerability + healing = magnetic personality'
    },
  ],
  'anxiety': [
    {
      belief: 'I can\'t handle this feeling.',
      reframe: 'You\'ve handled 100% of hard days. You can handle this too.',
      why: 'You\'re stronger than you think'
    },
    {
      belief: 'Something bad will definitely happen.',
      reframe: 'Your anxiety is predicting, not prophesying. It\'s often wrong.',
      why: 'Anxiety is a liar. Statistics are on your side'
    },
    {
      belief: 'I\'m losing control.',
      reframe: 'Actually, your breathing is 100% in your control right now.',
      why: 'Control over breath = control over nervous system'
    },
    {
      belief: 'I\'ll always be anxious.',
      reframe: 'You\'re learning to manage it. That\'s the goal, not elimination.',
      why: 'Management > elimination. Mastery > cure'
    },
  ],
  'depression': [
    {
      belief: 'I\'m worthless.',
      reframe: 'Your brain has a chemical imbalance, not a worth problem.',
      why: 'Depression = liar. Your value is intrinsic'
    },
    {
      belief: 'Nothing will help.',
      reframe: 'You took a walk yesterday and felt slightly better. That counts.',
      why: 'Small wins compound into big change'
    },
    {
      belief: 'I\'m a burden.',
      reframe: 'People want to help you. That\'s not burden, that\'s love.',
      why: 'Accepting help is strength, not weakness'
    },
    {
      belief: 'I\'ll feel like this forever.',
      reframe: 'Depression lies. Brain chemistry changes. You will feel better.',
      why: 'Neuroplasticity is real. Change is possible'
    },
  ],
  'loneliness': [
    {
      belief: 'Nobody cares about me.',
      reframe: 'You\'re reaching out right now and I care. You\'re not invisible.',
      why: 'One real connection > thousand fake ones'
    },
    {
      belief: 'I don\'t belong anywhere.',
      reframe: 'You haven\'t found your people yet. They\'re out there.',
      why: 'Everyone belongs somewhere. Keep looking'
    },
    {
      belief: 'I\'ll always be alone.',
      reframe: 'You connected with me. Connections can multiply from here.',
      why: 'One real friend is a foundation for many'
    },
    {
      belief: 'Nobody understands me.',
      reframe: 'I understand. And there are others like you out there.',
      why: 'You\'re not unique in your struggles. That\'s your superpower'
    },
  ]
};

export default function ReframerStage({ problemType, matchName, onComplete, onBack, stageData }) {
  const [currentReframe, setCurrentReframe] = useState(0);
  const [accepted, setAccepted] = useState({});

  const reframes = REFRAMES[problemType] || REFRAMES['anxiety'];
  const reframe = reframes[currentReframe];

  const handleAccept = () => {
    setAccepted({
      ...accepted,
      [currentReframe]: true
    });

    setTimeout(() => {
      if (currentReframe < reframes.length - 1) {
        setCurrentReframe(currentReframe + 1);
      } else {
        onComplete({
          stage: 'reframer',
          reframesAccepted: Object.keys(accepted).length,
          completedAt: new Date()
        });
      }
    }, 1500);
  };

  const isCurrentAccepted = accepted[currentReframe];

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-800 mb-2">🔄 Shifting Your Perspective</h2>
        <p className="text-gray-600">Depression, anxiety, loneliness... they all lie to us. Let\'s find the truth.</p>
      </div>

      <div className="bg-gradient-to-r from-yellow-50 to-orange-50 border-2 border-yellow-300 rounded-lg p-6">
        <div className="mb-6">
          <span className="text-sm font-semibold text-gray-600">
            Belief {currentReframe + 1} of {reframes.length}
          </span>
        </div>

        <div className="space-y-4 mb-6">
          <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded">
            <p className="text-red-700 font-semibold mb-1">What You Believe:</p>
            <p className="text-red-600 italic text-lg">"{reframe.belief}"</p>
          </div>

          <div className="text-center text-3xl text-yellow-600">⬇️</div>

          <div className="bg-green-50 border-l-4 border-green-500 p-4 rounded">
            <p className="text-green-700 font-semibold mb-1">What\'s Actually True:</p>
            <p className="text-green-600 text-lg">"{reframe.reframe}"</p>
            <p className="text-green-500 text-sm mt-2">💡 {reframe.why}</p>
          </div>
        </div>

        {!isCurrentAccepted ? (
          <div className="space-y-3">
            <p className="text-gray-700 text-center font-medium">
              Does this resonate with you?
            </p>
            <button
              onClick={handleAccept}
              className="w-full bg-gradient-to-r from-green-600 to-emerald-600 text-white py-3 rounded-lg font-semibold hover:opacity-90"
            >
              Yes, I Get It ✨
            </button>
            <button
              className="w-full bg-gray-200 text-gray-700 py-3 rounded-lg font-semibold hover:bg-gray-300"
            >
              I Need to Think About It
            </button>
          </div>
        ) : (
          <div className="bg-green-100 border-2 border-green-500 rounded-lg p-4 text-center">
            <p className="text-green-700 font-bold">✅ Truth Accepted!</p>
            <p className="text-green-600 text-sm mt-2">
              {currentReframe < reframes.length - 1 
                ? 'Loading next belief...' 
                : 'You\'ve reframed all the main beliefs!'}
            </p>
          </div>
        )}
      </div>

      <button
        onClick={onBack}
        className="text-blue-600 hover:text-blue-800 text-sm font-semibold"
      >
        ← Go Back
      </button>
    </div>
  );
}