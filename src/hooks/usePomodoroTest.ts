'use client';

import { useEffect } from 'react';
import { usePomodoroStore } from '@/store/pomodoroStore';
import { useSessionStore } from '@/store/sessionStore';
import { useSettingsStore } from '@/store/settingsStore';

/**
 * Test hook to simulate a full Pomodoro cycle with fake attention data
 * This helps test the timer + session logging without needing face detection
 */
export function usePomodoroTest() {
  const pomodoro = usePomodoroStore();
  const session = useSessionStore();
  const settings = useSettingsStore();

  // Simulate attention tracking during work phases
  useEffect(() => {
    if (pomodoro.status !== 'running' || pomodoro.phase !== 'work') {
      return;
    }

    // Record fake attention score every second
    const interval = setInterval(() => {
      // Generate random attention score between 0.7 and 1.0
      const fakeAttentionScore = 0.7 + Math.random() * 0.3;
      session.recordAttention(fakeAttentionScore);
    }, 1000);

    return () => clearInterval(interval);
  }, [pomodoro.status, pomodoro.phase, session]);

  return {
    // Pomodoro controls
    startTimer: pomodoro.startTimer,
    pauseTimer: pomodoro.pauseTimer,
    resumeTimer: pomodoro.resumeTimer,
    skipPhase: pomodoro.skipPhase,
    resetTimer: pomodoro.resetTimer,

    // Current state
    phase: pomodoro.phase,
    status: pomodoro.status,
    timeRemaining: pomodoro.timeRemaining,
    cyclesCompleted: pomodoro.cyclesCompleted,

    // Session data
    sessions: session.sessions,
    todayStats: session.getTodayStats(),

    // Settings
    settings: settings,
    updateSettings: settings.updateSettings,

    // Helpers for testing
    simulateFullCycle: () => {
      // Speed up timer for testing (5 second work, 2 second break)
      settings.updateSettings({
        workMin: 0.083, // 5 seconds
        shortBreak: 0.033, // 2 seconds
        longBreak: 0.05, // 3 seconds
      });
      pomodoro.startTimer('test-task-123');
    },

    resetToDefaults: () => {
      pomodoro.resetTimer();
      settings.resetSettings();
    },
  };
}