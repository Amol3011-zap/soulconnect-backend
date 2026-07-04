import React, { useState } from 'react';
import MirrorStage from './healing/MirrorStage';
import ExplorerStage from './healing/ExplorerStage';
import ReframerStage from './healing/ReframerStage';
import ActionStage from './healing/ActionStage';
import VictoryStage from './healing/VictoryStage';

export default function GuidedHealing({ problemType, matchName, userId }) {
  const [stage, setStage] = useState('mirror'); // mirror, explorer, reframer, action, victory
  const [stageData, setStageData] = useState({});
  const [conversationHistory, setConversationHistory] = useState([]);

  const handleStageComplete = (data) => {
    setStageData({ ...stageData, ...data });
    setConversationHistory([...conversationHistory, data]);
    
    // Auto progress to next stage
    const stageOrder = ['mirror', 'explorer', 'reframer', 'action', 'victory'];
    const currentIndex = stageOrder.indexOf(stage);
    if (currentIndex < stageOrder.length - 1) {
      setStage(stageOrder[currentIndex + 1]);
    }
  };

  const handleGoBack = () => {
    const stageOrder = ['mirror', 'explorer', 'reframer', 'action', 'victory'];
    const currentIndex = stageOrder.indexOf(stage);
    if (currentIndex > 0) {
      setStage(stageOrder[currentIndex - 1]);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
      {/* Progress Bar */}
      <div className="mb-6">
        <div className="flex justify-between text-sm mb-2">
          <span className="font-semibold text-gray-700">Your Healing Journey</span>
          <span className="text-gray-500">Step {['mirror', 'explorer', 'reframer', 'action', 'victory'].indexOf(stage) + 1}/5</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div 
            className="bg-gradient-to-r from-purple-600 to-pink-600 h-2 rounded-full transition-all"
            style={{ width: `${((['mirror', 'explorer', 'reframer', 'action', 'victory'].indexOf(stage) + 1) / 5) * 100}%` }}
          />
        </div>
      </div>

      {/* Stage Components */}
      {stage === 'mirror' && (
        <MirrorStage 
          problemType={problemType}
          matchName={matchName}
          onComplete={handleStageComplete}
        />
      )}

      {stage === 'explorer' && (
        <ExplorerStage 
          problemType={problemType}
          matchName={matchName}
          onComplete={handleStageComplete}
          onBack={handleGoBack}
          stageData={stageData}
        />
      )}

      {stage === 'reframer' && (
        <ReframerStage 
          problemType={problemType}
          matchName={matchName}
          onComplete={handleStageComplete}
          onBack={handleGoBack}
          stageData={stageData}
        />
      )}

      {stage === 'action' && (
        <ActionStage 
          problemType={problemType}
          matchName={matchName}
          onComplete={handleStageComplete}
          onBack={handleGoBack}
          stageData={stageData}
        />
      )}

      {stage === 'victory' && (
        <VictoryStage 
          problemType={problemType}
          matchName={matchName}
          stageData={stageData}
          conversationHistory={conversationHistory}
          onBack={handleGoBack}
        />
      )}
    </div>
  );
}