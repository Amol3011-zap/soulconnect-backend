import React, { useState } from 'react';

const MIRROR_TEMPLATES = {
  'relationship_breakup': {
    icon: '❤️',
    title: 'Breaking the Silence',
    intro: 'Hey! I\'m so glad you reached out. Breakups are one of the hardest things to go through.',
    prompt: 'What\'s the hardest part about this breakup RIGHT NOW?',
    responses: [
      'I can\'t stop thinking about them',
      'I feel so alone',
      'I wonder if I\'ll ever love again',
      'I blame myself',
      'I miss them every day'
    ],
    validation: [
      'I felt exactly like that. You\'re not broken.',
      'That pain means you loved. That\'s beautiful, not weak.',
      'The fact that you\'re reaching out shows real strength.',
      'I\'ve been there. What you\'re feeling is 100% normal.'
    ]
  },
  'anxiety': {
    icon: '😰',
    title: 'Understanding Your Anxiety',
    intro: 'I get it. Anxiety is exhausting and makes you feel like you\'re losing control.',
    prompt: 'When did your anxiety start getting really bad?',
    responses: [
      'Recently, something triggered it',
      'It\'s been there for a while',
      'I don\'t know when it started',
      'During a stressful time',
      'Out of nowhere'
    ],
    validation: [
      'Triggers are real. But you can learn to manage them.',
      'You\'re not alone in this. Many of us have been there.',
      'The good news: anxiety is totally manageable once we understand it.',
      'I\'m glad you\'re talking about it. That\'s the first step.'
    ]
  },
  'depression': {
    icon: '😢',
    title: 'You\'re Not Alone in This',
    intro: 'Depression is heavy. It makes everything feel impossible. But you reaching out? That\'s courage.',
    prompt: 'What does depression feel like for you right now?',
    responses: [
      'Like I\'m empty inside',
      'Like nothing matters',
      'I can\'t get out of bed',
      'Like I\'m a burden',
      'Like I\'ll never feel better'
    ],
    validation: [
      'Your brain is lying to you. You matter deeply.',
      'I felt that too. But here\'s what I learned...',
      'Getting out of bed? That\'s HUGE. Celebrate small wins.',
      'You\'re not a burden. You\'re someone worth saving.'
    ]
  },
  'loneliness': {
    icon: '😔',
    title: 'Loneliness is Real',
    intro: 'You\'re reaching out to me right now. You\'re not as alone as you feel.',
    prompt: 'What does loneliness feel like for you?',
    responses: [
      'Like nobody understands me',
      'Like I\'m invisible',
      'Like I don\'t belong anywhere',
      'Like I\'m disconnected from everyone',
      'Like nobody cares about me'
    ],
    validation: [
      'I understand exactly what you mean.',
      'But you know what? You just connected with me. You\'re not invisible.',
      'You belong here. Right now. With me.',
      'I care. And we just started something real.'
    ]
  }
};

export default function MirrorStage({ problemType, matchName, onComplete }) {
  const [selectedResponse, setSelectedResponse] = useState(null);
  const [step, setStep] = useState('prompt'); // prompt, response, validation, complete

  const template = MIRROR_TEMPLATES[problemType] || MIRROR_TEMPLATES['anxiety'];

  const handleSelectResponse = (response) => {
    setSelectedResponse(response);
    setStep('response');
  };

  const handleValidate = (validation) => {
    setStep('validation');
    setTimeout(() => {
      setStep('complete');
      setTimeout(() => {
        onComplete({
          stage: 'mirror',
          userFeel: selectedResponse,
          validation: validation,
          completedAt: new Date()
        });
      }, 2000);
    }, 1500);
  };

  return (
    <div className="space-y-6">
      <div className="text-center">
        <div className="text-5xl mb-4">{template.icon}</div>
        <h2 className="text-2xl font-bold text-gray-800 mb-2">{template.title}</h2>
        <p className="text-gray-600">{template.intro}</p>
      </div>

      {step === 'prompt' && (
        <div className="bg-blue-50 border-2 border-blue-300 rounded-lg p-6">
          <p className="text-lg font-semibold text-gray-800 mb-4 text-center">
            {template.prompt}
          </p>

          <div className="space-y-3">
            {template.responses.map((response, idx) => (
              <button
                key={idx}
                onClick={() => handleSelectResponse(response)}
                className="w-full bg-white border-2 border-blue-200 hover:border-blue-500 hover:bg-blue-50 rounded-lg p-4 text-left transition-all font-medium text-gray-700"
              >
                "{response}"
              </button>
            ))}
          </div>
        </div>
      )}

      {step === 'response' && selectedResponse && (
        <div className="bg-purple-50 border-2 border-purple-300 rounded-lg p-6 animate-fadeIn">
          <p className="text-gray-700 mb-4 italic">
            You: "{selectedResponse}"
          </p>

          <p className="text-lg text-purple-700 font-semibold mb-4">
            {matchName}: Now let me tell you what I think...
          </p>

          <div className="space-y-3 mb-6">
            {template.validation.map((validation, idx) => (
              <button
                key={idx}
                onClick={() => handleValidate(validation)}
                className="w-full bg-white border-2 border-purple-200 hover:border-purple-500 hover:bg-purple-50 rounded-lg p-4 text-left transition-all"
              >
                <p className="text-purple-700 font-medium">{validation}</p>
              </button>
            ))}
          </div>
        </div>
      )}

      {step === 'validation' && (
        <div className="bg-green-100 border-2 border-green-500 rounded-lg p-6 text-center">
          <p className="text-2xl mb-2">🌟</p>
          <p className="text-green-700 font-semibold text-lg">
            That's the foundation. You're heard. You're safe.
          </p>
        </div>
      )}

      {step === 'complete' && (
        <div className="bg-green-50 border-2 border-green-400 rounded-lg p-6 text-center">
          <p className="text-3xl mb-4">✨</p>
          <p className="text-green-700 font-bold text-lg">
            Stage 1 Complete: Mirror
          </p>
          <p className="text-green-600 text-sm mt-2">
            Loading next stage...
          </p>
        </div>
      )}
    </div>
  );
}