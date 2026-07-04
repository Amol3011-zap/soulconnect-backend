import React, { useState } from 'react';

const POWER_QUESTIONS = {
  'relationship_breakup': [
    { q: 'How long were you together?', category: 'understand' },
    { q: 'What was the best part of this relationship?', category: 'learn' },
    { q: 'If you\'re honest, what was missing?', category: 'growth' },
    { q: 'What did this relationship teach you about yourself?', category: 'insight' },
    { q: 'What would your best friend say about this breakup?', category: 'perspective' },
  ],
  'anxiety': [
    { q: 'What specifically triggers your anxiety the most?', category: 'trigger' },
    { q: 'When you feel anxious, what\'s the first thought that pops up?', category: 'thought' },
    { q: 'What\'s the worst thing you think will happen?', category: 'fear' },
    { q: 'Has that worst thing ever actually happened?', category: 'reality' },
    { q: 'What helps you calm down, even a little?', category: 'solution' },
  ],
  'depression': [
    { q: 'When did you first notice feeling depressed?', category: 'timeline' },
    { q: 'What was happening in your life around that time?', category: 'trigger' },
    { q: 'What activities used to bring you joy?', category: 'memory' },
    { q: 'What\'s ONE thing that made you smile recently?', category: 'hope' },
    { q: 'If you could change one thing right now, what would it be?', category: 'action' },
  ],
  'loneliness': [
    { q: 'When did you start feeling lonely?', category: 'timeline' },
    { q: 'Who in your life cares about you?', category: 'reality' },
    { q: 'What stops you from reaching out to them?', category: 'barrier' },
    { q: 'What would your ideal friendship look like?', category: 'vision' },
    { q: 'What\'s stopping you from creating that?', category: 'action' },
  ]
};

export default function ExplorerStage({ problemType, matchName, onComplete, onBack, stageData }) {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState({});
  const [userAnswer, setUserAnswer] = useState('');
  const [showResponse, setShowResponse] = useState(false);

  const questions = POWER_QUESTIONS[problemType] || POWER_QUESTIONS['anxiety'];
  const question = questions[currentQuestion];

  const handleSubmitAnswer = () => {
    if (!userAnswer.trim()) return;

    setAnswers({
      ...answers,
      [currentQuestion]: userAnswer
    });

    setShowResponse(true);
  };

  const handleNextQuestion = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
      setUserAnswer('');
      setShowResponse(false);
    } else {
      onComplete({
        stage: 'explorer',
        answers: answers,
        completedAt: new Date()
      });
    }
  };

  const responses = {
    'understand': 'That helps me understand the depth of what you\'re going through.',
    'learn': 'That\'s beautiful. And that\'s what you\'ll take forward.',
    'growth': 'This is important. This is where growth happens.',
    'insight': 'This right here. This is self-awareness. This is power.',
    'perspective': 'Your best friend is right. And so am I.',
    'trigger': 'Okay, so we found the trigger. That\'s huge.',
    'thought': 'That thought keeps you in a loop. But it\'s just a thought, not reality.',
    'fear': 'Let\'s sit with that fear for a second.',
    'reality': 'Exactly. Your anxiety is lying to you.',
    'solution': 'There it is. Your superpower. Remember this.',
    'timeline': 'Okay, so it wasn\'t always like this. That\'s important.',
    'trigger': 'Something changed. We need to understand what.',
    'memory': 'Good. You CAN feel joy. Your brain knows how.',
    'hope': 'Right there. That\'s your light. Hold onto it.',
    'action': 'That\'s your next step. We\'ll get there together.',
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-800 mb-2">🔍 Understanding Your Story</h2>
        <p className="text-gray-600">These questions help us find the real roots. No judgment. Just truth.</p>
      </div>

      <div className="bg-gradient-to-r from-blue-50 to-purple-50 border-2 border-blue-300 rounded-lg p-6">
        <div className="flex justify-between items-center mb-4">
          <span className="text-sm font-semibold text-gray-600">
            Question {currentQuestion + 1} of {questions.length}
          </span>
          <div className="flex gap-1">
            {questions.map((_, idx) => (
              <div
                key={idx}
                className={`h-2 w-2 rounded-full transition-all ${
                  idx <= currentQuestion ? 'bg-blue-600' : 'bg-gray-300'
                }`}
              />
            ))}
          </div>
        </div>

        <p className="text-xl font-semibold text-gray-800 mb-6">
          {matchName}: {question.q}
        </p>

        {!showResponse ? (
          <div>
            <textarea
              value={userAnswer}
              onChange={(e) => setUserAnswer(e.target.value)}
              placeholder="Be honest. Share what's real for you..."
              className="w-full p-4 border-2 border-blue-300 rounded-lg focus:outline-none focus:border-blue-500 resize-none"
              rows="4"
            />

            <button
              onClick={handleSubmitAnswer}
              disabled={!userAnswer.trim()}
              className="mt-4 w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Share This
            </button>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="bg-white p-4 rounded-lg border-l-4 border-blue-600">
              <p className="text-gray-700 italic">You: "{userAnswer}"</p>
            </div>

            <div className="bg-white p-4 rounded-lg border-l-4 border-purple-600">
              <p className="text-purple-700">
                {matchName}: {responses[question.category]}
              </p>
            </div>

            <button
              onClick={handleNextQuestion}
              className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 rounded-lg font-semibold hover:opacity-90"
            >
              {currentQuestion < questions.length - 1 ? 'Next Question' : 'Done Exploring'}
            </button>
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