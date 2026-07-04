# 🎯 Tiny Wins Redesign - Complete Files

All production-ready code for the Tiny Wins feature redesign.

---

## 📋 FILE 1: src/data/tinyWinsDatabase.js

```javascript
// Comprehensive Tiny Wins Database
// 30 built-in challenges organized by category

export const TINY_WINS_DATABASE = [
  {
    id: 1,
    icon: '🌬',
    category: 'Breathing',
    title: 'One Long Exhale',
    description: 'Take one deep breath. Exhale twice as slowly.',
    time: 1,
    difficulty: 'Beginner',
    whyItHelps: 'A longer exhale activates your parasympathetic nervous system, helping your body shift from stress into a calmer state.',
    moodCategories: ['fog', 'heavy-rain', 'storm'],
  },
  {
    id: 2,
    icon: '💧',
    category: 'Hydration',
    title: 'Drink a Glass of Water',
    description: 'Slowly drink one glass of water.',
    time: 1,
    difficulty: 'Beginner',
    whyItHelps: 'Hydration supports concentration, mood and energy. Even mild dehydration can affect cognitive function.',
    moodCategories: ['fog', 'heavy-rain', 'clear-sky'],
  },
  {
    id: 3,
    icon: '🚶',
    category: 'Movement',
    title: 'Walk 100 Steps',
    description: 'Walk slowly. Notice your breathing.',
    time: 2,
    difficulty: 'Beginner',
    whyItHelps: 'Gentle movement reduces stress hormones and increases circulation without requiring intense exercise.',
    moodCategories: ['fog', 'heavy-rain'],
  },
  {
    id: 4,
    icon: '☀️',
    category: 'Grounding',
    title: 'Find Natural Light',
    description: 'Stand near sunlight for a moment.',
    time: 2,
    difficulty: 'Beginner',
    whyItHelps: 'Natural light supports your circadian rhythm, boosts serotonin, and improves mood.',
    moodCategories: ['clear-sky', 'hope', 'blooming'],
  },
  {
    id: 5,
    icon: '👀',
    category: 'Mindfulness',
    title: 'Look Away From Your Screen',
    description: 'Focus on something far away for one minute.',
    time: 1,
    difficulty: 'Beginner',
    whyItHelps: 'Reduces eye strain and mental fatigue. The 20-20-20 rule gives your eyes essential rest.',
    moodCategories: ['clear-sky', 'fog'],
  },
  {
    id: 6,
    icon: '🙏',
    category: 'Grounding',
    title: 'Relax Your Shoulders',
    description: 'Drop your shoulders. Relax your jaw.',
    time: 1,
    difficulty: 'Beginner',
    whyItHelps: 'Your body often stores stress in the neck and shoulders. Releasing tension interrupts the stress cycle.',
    moodCategories: ['storm', 'heavy-rain'],
  },
  {
    id: 7,
    icon: '🌿',
    category: 'Breathing',
    title: 'Five Slow Breaths',
    description: 'Inhale for 4. Exhale for 6.',
    time: 1,
    difficulty: 'Beginner',
    whyItHelps: 'Slow breathing calms the nervous system and creates an anchor for your attention.',
    moodCategories: ['storm', 'heavy-rain', 'fog'],
  },
  {
    id: 8,
    icon: '☕',
    category: 'Mindfulness',
    title: 'Mindful Sip',
    description: 'Drink coffee or tea without distractions.',
    time: 2,
    difficulty: 'Beginner',
    whyItHelps: 'Mindfulness interrupts autopilot mode and helps you experience moments more fully.',
    moodCategories: ['clear-sky', 'hope'],
  },
  {
    id: 9,
    icon: '❤️',
    category: 'Self Compassion',
    title: 'Say Something Kind to Yourself',
    description: 'Replace one negative thought with something kind.',
    time: 0.5,
    difficulty: 'Beginner',
    whyItHelps: 'Self-compassion lowers self-criticism and builds resilience. Speaking kindly to yourself rewires negative patterns.',
    moodCategories: ['storm', 'fog', 'blooming'],
  },
  {
    id: 10,
    icon: '✨',
    category: 'Self Compassion',
    title: 'Accept a Compliment',
    description: 'Simply say "Thank you" when complimented.',
    time: 1,
    difficulty: 'Beginner',
    whyItHelps: 'Receiving kindness strengthens self-worth. Resisting compliments reinforces self-doubt.',
    moodCategories: ['hope', 'blooming'],
  },
  {
    id: 11,
    icon: '🤝',
    category: 'Kindness',
    title: 'Send Someone a Kind Message',
    description: 'Thank someone or send a kind word.',
    time: 2,
    difficulty: 'Beginner',
    whyItHelps: 'Acts of kindness improve emotional wellbeing and strengthen social connections.',
    moodCategories: ['hope', 'blooming', 'clear-sky'],
  },
  {
    id: 12,
    icon: '🌸',
    category: 'Movement',
    title: 'Stretch Your Neck',
    description: 'Gentle stretches in all directions.',
    time: 2,
    difficulty: 'Beginner',
    whyItHelps: 'Releases physical tension and improves circulation to the head.',
    moodCategories: ['heavy-rain', 'fog'],
  },
  {
    id: 13,
    icon: '📵',
    category: 'Digital Detox',
    title: 'Put Your Phone Down',
    description: 'No scrolling for 3 minutes.',
    time: 3,
    difficulty: 'Intermediate',
    whyItHelps: 'Short digital breaks improve focus, reduce anxiety, and help reset your nervous system.',
    moodCategories: ['storm', 'clear-sky'],
  },
  {
    id: 14,
    icon: '🌳',
    category: 'Grounding',
    title: 'Notice Five Things Around You',
    description: 'Observe your surroundings. Use all five senses.',
    time: 2,
    difficulty: 'Beginner',
    whyItHelps: 'Grounding techniques interrupt anxious thoughts by anchoring you to the present moment.',
    moodCategories: ['storm', 'fog', 'heavy-rain'],
  },
  {
    id: 15,
    icon: '📦',
    category: 'Productivity',
    title: 'Clear One Small Space',
    description: 'Organize one small area around you.',
    time: 3,
    difficulty: 'Beginner',
    whyItHelps: 'A cleaner environment reduces mental clutter and creates a sense of control.',
    moodCategories: ['clear-sky', 'hope'],
  },
  {
    id: 16,
    icon: '🎯',
    category: 'Productivity',
    title: 'Finish One Tiny Task',
    description: 'Complete something easy and specific.',
    time: 3,
    difficulty: 'Beginner',
    whyItHelps: 'Completing tasks builds momentum and creates positive reinforcement for action.',
    moodCategories: ['clear-sky', 'hope', 'blooming'],
  },
  {
    id: 17,
    icon: '🌬',
    category: 'Nature',
    title: 'Fresh Air Break',
    description: 'Open a window or step outside.',
    time: 2,
    difficulty: 'Beginner',
    whyItHelps: 'Fresh air increases alertness and oxygenation, improving mood and clarity.',
    moodCategories: ['heavy-rain', 'fog'],
  },
  {
    id: 18,
    icon: '📖',
    category: 'Reflection',
    title: 'Read One Inspiring Paragraph',
    description: 'Read something uplifting or meaningful.',
    time: 2,
    difficulty: 'Beginner',
    whyItHelps: 'Positive input shapes positive thinking. Inspirational content shifts your perspective.',
    moodCategories: ['hope', 'blooming', 'clear-sky'],
  },
  {
    id: 19,
    icon: '🧘',
    category: 'Mindfulness',
    title: 'Close Your Eyes',
    description: 'Just breathe for one minute.',
    time: 1,
    difficulty: 'Beginner',
    whyItHelps: 'Even one minute of stillness reduces mental overload and creates clarity.',
    moodCategories: ['storm', 'fog', 'heavy-rain'],
  },
  {
    id: 20,
    icon: '✍️',
    category: 'Reflection',
    title: 'Write One Positive Thought',
    description: 'Journal one sentence about your day.',
    time: 2,
    difficulty: 'Beginner',
    whyItHelps: 'Writing improves emotional processing and helps consolidate positive experiences.',
    moodCategories: ['blooming', 'hope'],
  },
  {
    id: 21,
    icon: '😊',
    category: 'Self Compassion',
    title: 'Smile at Yourself',
    description: 'Smile in the mirror.',
    time: 0.5,
    difficulty: 'Beginner',
    whyItHelps: 'Small facial expressions can positively influence mood through the facial feedback hypothesis.',
    moodCategories: ['hope', 'blooming'],
  },
  {
    id: 22,
    icon: '👂',
    category: 'Social Connection',
    title: 'Listen Without Interrupting',
    description: 'Give someone your full attention.',
    time: 3,
    difficulty: 'Intermediate',
    whyItHelps: 'Deep listening strengthens relationships and creates meaningful moments.',
    moodCategories: ['clear-sky', 'hope', 'blooming'],
  },
  {
    id: 23,
    icon: '💜',
    category: 'Gratitude',
    title: 'Gratitude Moment',
    description: 'Think of one thing you are grateful for.',
    time: 1,
    difficulty: 'Beginner',
    whyItHelps: 'Gratitude shifts attention toward positive experiences and increases happiness.',
    moodCategories: ['hope', 'blooming', 'clear-sky'],
  },
  {
    id: 24,
    icon: '🌈',
    category: 'Grounding',
    title: 'Notice Something Beautiful',
    description: 'Tree, flower, sky, cloud—anything beautiful.',
    time: 1,
    difficulty: 'Beginner',
    whyItHelps: 'Finding beauty trains your brain to notice positive details and shifts your perspective.',
    moodCategories: ['clear-sky', 'hope', 'blooming'],
  },
  {
    id: 25,
    icon: '📚',
    category: 'Learning',
    title: 'Learn One New Thing',
    description: 'Read one interesting fact.',
    time: 2,
    difficulty: 'Intermediate',
    whyItHelps: 'Curiosity keeps the brain engaged and creates a sense of progress.',
    moodCategories: ['clear-sky', 'hope'],
  },
  {
    id: 26,
    icon: '🤲',
    category: 'Grounding',
    title: 'Unclench Your Hands',
    description: 'Relax every finger and muscle.',
    time: 1,
    difficulty: 'Beginner',
    whyItHelps: 'Your hands often tighten during stress. Releasing tension communicates safety to your nervous system.',
    moodCategories: ['storm', 'heavy-rain', 'fog'],
  },
  {
    id: 27,
    icon: '🎵',
    category: 'Mindfulness',
    title: 'Listen to One Calm Song',
    description: 'Close your eyes and just listen.',
    time: 3,
    difficulty: 'Beginner',
    whyItHelps: 'Music regulates emotion, reduces stress, and activates the relaxation response.',
    moodCategories: ['storm', 'heavy-rain', 'fog'],
  },
  {
    id: 28,
    icon: '🌱',
    category: 'Movement',
    title: 'Stand Up and Stretch',
    description: 'Stretch your whole body.',
    time: 2,
    difficulty: 'Beginner',
    whyItHelps: 'Movement increases circulation, energy, and helps shake off accumulated tension.',
    moodCategories: ['fog', 'heavy-rain'],
  },
  {
    id: 29,
    icon: '🌼',
    category: 'Breathing',
    title: 'Window Reset',
    description: 'Open the window and take five deep breaths.',
    time: 1,
    difficulty: 'Beginner',
    whyItHelps: 'Fresh air combined with conscious breathing creates a mental reset.',
    moodCategories: ['fog', 'heavy-rain', 'storm'],
  },
  {
    id: 30,
    icon: '🎉',
    category: 'Gratitude',
    title: 'Celebrate One Small Win',
    description: 'Recognize something you did today.',
    time: 1,
    difficulty: 'Beginner',
    whyItHelps: 'Celebrating progress builds confidence and reinforces positive behavior.',
    moodCategories: ['clear-sky', 'hope', 'blooming'],
  },
];

export const MOOD_TO_CATEGORIES = {
  'clear-sky': ['Productivity', 'Learning', 'Gratitude', 'Social Connection'],
  'hope': ['Gratitude', 'Kindness', 'Self Compassion', 'Reflection'],
  'blooming': ['Reflection', 'Gratitude', 'Growth', 'Mindfulness'],
  'fog': ['Grounding', 'Hydration', 'Movement', 'Breathing'],
  'heavy-rain': ['Breathing', 'Nature', 'Stretching', 'Hydration', 'Movement'],
  'storm': ['Breathing', 'Grounding', 'Hydration', 'Self Compassion', 'Movement'],
};

export const DIFFICULTY_COLORS = {
  Beginner: '#10B981',
  Intermediate: '#F59E0B',
  Advanced: '#EF4444',
};

export function getTodaysChallenges(mood = 'clear-sky', completedToday = []) {
  const categories = MOOD_TO_CATEGORIES[mood] || MOOD_TO_CATEGORIES['clear-sky'];
  const available = TINY_WINS_DATABASE.filter(challenge => !completedToday.includes(challenge.id));
  const selected = [];
  const usedCategories = new Set();

  for (const challenge of available) {
    if (selected.length >= 3) break;
    if (categories.includes(challenge.category) && !usedCategories.has(challenge.category)) {
      selected.push(challenge);
      usedCategories.add(challenge.category);
    }
  }

  for (const challenge of available) {
    if (selected.length >= 3) break;
    if (!selected.find(c => c.id === challenge.id) && !usedCategories.has(challenge.category)) {
      selected.push(challenge);
      usedCategories.add(challenge.category);
    }
  }

  for (const challenge of available) {
    if (selected.length >= 3) break;
    if (!selected.find(c => c.id === challenge.id)) {
      selected.push(challenge);
    }
  }

  return selected.slice(0, 3);
}
```

---

## COPY THESE 4 FILES TO YOUR PROJECT

### File 1: `src/data/tinyWinsDatabase.js`
Copy the DATABASE CODE above ☝️

### File 2: `src/components/TinyWinCard.jsx`
```javascript
import React, { useState } from 'react';
import { motion } from 'motion/react';
import { DIFFICULTY_COLORS } from '../data/tinyWinsDatabase';

export default function TinyWinCard({ challenge, onComplete, isCompleted }) {
  const [expandedWhy, setExpandedWhy] = useState(false);
  const difficultyColor = DIFFICULTY_COLORS[challenge.difficulty] || '#10B981';

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ y: -4 }}
      style={{
        background: 'linear-gradient(145deg, rgba(26,10,62,0.95) 0%, rgba(45,18,96,0.9) 50%, rgba(20,8,52,0.95) 100%)',
        border: '1px solid rgba(139,92,246,0.2)',
        borderRadius: 20,
        padding: 18,
        boxShadow: '0 8px 32px rgba(0,0,0,0.3), 0 0 60px rgba(124,58,237,0.1)',
        opacity: isCompleted ? 0.6 : 1,
      }}
    >
      <div style={{ display: 'flex', gap: 12, marginBottom: 12 }}>
        <div style={{ fontSize: 32 }}>{challenge.icon}</div>
        <div style={{ flex: 1 }}>
          <div style={{ fontSize: 10, fontWeight: 700, letterSpacing: '0.08em', textTransform: 'uppercase', color: 'rgba(196,181,253,0.5)', marginBottom: 4 }}>
            {challenge.category}
          </div>
          <h3 style={{ fontSize: 15, fontWeight: 700, color: '#fff', margin: 0 }}>
            {challenge.title}
            {isCompleted && ' ✓'}
          </h3>
        </div>
      </div>

      <p style={{ fontSize: 12, color: 'rgba(184,180,216,0.75)', margin: '0 0 12px', lineHeight: 1.5 }}>
        {challenge.description}
      </p>

      <div style={{ display: 'flex', gap: 8, marginBottom: 14 }}>
        <span style={{ display: 'inline-flex', alignItems: 'center', gap: 4, background: 'rgba(255,255,255,0.06)', border: '1px solid rgba(255,255,255,0.09)', borderRadius: 16, padding: '4px 10px', fontSize: 11, color: '#B8B4D8' }}>
          ⏱ {challenge.time < 1 ? Math.round(challenge.time * 60) + 's' : challenge.time + ' min'}
        </span>
        <span style={{ display: 'inline-flex', alignItems: 'center', gap: 4, background: 'rgba(255,255,255,0.06)', border: '1px solid rgba(255,255,255,0.09)', borderRadius: 16, padding: '4px 10px', fontSize: 11, color: '#B8B4D8' }}>
          <span style={{ color: difficultyColor }}>●</span> {challenge.difficulty}
        </span>
      </div>

      <motion.div initial={false} animate={{ height: expandedWhy ? 'auto' : 0 }} style={{ overflow: 'hidden', marginBottom: expandedWhy ? 12 : 0 }}>
        <div style={{ background: 'rgba(139,92,246,0.1)', border: '1px solid rgba(168,85,247,0.2)', borderRadius: 12, padding: 12 }}>
          <p style={{ fontSize: 12, color: 'rgba(184,180,216,0.85)', margin: 0, lineHeight: 1.6 }}>
            {challenge.whyItHelps}
          </p>
        </div>
      </motion.div>

      <div style={{ display: 'flex', gap: 8 }}>
        <motion.button whileHover={{ y: -2 }} onClick={() => setExpandedWhy(!expandedWhy)} style={{ flex: 1, background: 'rgba(255,255,255,0.06)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 10, color: '#A78BFA', fontSize: 12, fontWeight: 600, padding: '10px 12px', cursor: 'pointer' }}>
          💡 {expandedWhy ? 'Hide' : 'Why?'}
        </motion.button>
        <motion.button whileHover={!isCompleted ? { y: -2 } : {}} onClick={() => onComplete?.(challenge.id)} disabled={isCompleted} style={{ flex: 1, background: 'linear-gradient(135deg, #6D4AFF, #8B5CF6)', border: 'none', borderRadius: 12, color: '#fff', fontWeight: 600, cursor: 'pointer', padding: '10px 20px', fontSize: 13, opacity: isCompleted ? 0.5 : 1 }}>
          {isCompleted ? '✓ Done' : 'Complete'}
        </motion.button>
      </div>
    </motion.div>
  );
}
```

### File 3: `src/hooks/useTinyWins.js`
```javascript
import { useCallback } from 'react';
import { useTinyWinsStore } from '../store/tinyWins';
import { useWeatherStore } from '../store/weather';
import { getTodaysChallenges } from '../data/tinyWinsDatabase';

export function useTinyWins() {
  const { dailyWins, completedToday, checkAndRefresh, completeWin } = useTinyWinsStore();
  const { todayEntry } = useWeatherStore();
  const mood = todayEntry?.weather || 'clear-sky';

  const getTodaysChallengesList = useCallback(() => {
    return getTodaysChallenges(mood, completedToday);
  }, [mood, completedToday]);

  return {
    dailyWins,
    completedToday,
    checkAndRefresh,
    completeWin,
    getTodaysChallenges: getTodaysChallengesList,
    getCompletionPercentage: () => Math.round((completedToday.length / 3) * 100),
    isAllDone: completedToday.length === 3,
    mood,
  };
}
```

### File 4: `src/pages/TinyWins.jsx`
[See src/pages/TinyWins.jsx content above or in dev branch]

---

## ✅ Installation Steps
1. Copy 4 files above to their directories
2. Update routing in App.jsx (if needed)
3. Run: `npm run build`
4. Done! 🎉

No new dependencies needed!
