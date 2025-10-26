import { create } from 'zustand';
import { PomodoroState, TimerPhase, TimerStatus } from '@/types/pomodoro';
import { useSettingsStore } from './settingsStore';
import { useSessionStore } from './sessionStore';

interface PomodoroStore extends PomodoroState {
  // Actions
  startTimer: (taskId?: string) => void;
  pauseTimer: () => void;
  resumeTimer: () => void;
  skipPhase: () => void;
  resetTimer: () => void;
  tick: () => void; // Called every second
  
  // Internal
  intervalId: number | null;
}

export const usePomodoroStore = create<PomodoroStore>((set, get) => ({
  // Initial state
  phase: 'idle',
  status: 'idle',
  timeRemaining: 0,
  cyclesCompleted: 0,
  currentTaskId: null,
  intervalId: null,

  startTimer: (taskId) => {
    const settings = useSettingsStore.getState();
    const { intervalId } = get();
    
    // Clear any existing interval
    if (intervalId) {
      clearInterval(intervalId);
    }

    // Start work phase
    const newIntervalId = window.setInterval(() => {
      get().tick();
    }, 1000);

    set({
      phase: 'work',
      status: 'running',
      timeRemaining: settings.workMin * 60,
      currentTaskId: taskId || null,
      intervalId: newIntervalId,
    });
  },

  pauseTimer: () => {
    const { intervalId } = get();
    if (intervalId) {
      clearInterval(intervalId);
    }
    set({ status: 'paused', intervalId: null });
  },

  resumeTimer: () => {
    const { status } = get();
    if (status !== 'paused') return;

    const newIntervalId = window.setInterval(() => {
      get().tick();
    }, 1000);

    set({ status: 'running', intervalId: newIntervalId });
  },

  skipPhase: () => {
    // Force move to next phase
    set({ timeRemaining: 0 });
    get().tick();
  },

  resetTimer: () => {
    const { intervalId } = get();
    if (intervalId) {
      clearInterval(intervalId);
    }
    
    set({
      phase: 'idle',
      status: 'idle',
      timeRemaining: 0,
      cyclesCompleted: 0,
      currentTaskId: null,
      intervalId: null,
    });
  },

  tick: () => {
    const state = get();
    const settings = useSettingsStore.getState();

    if (state.status !== 'running') return;

    // Countdown
    if (state.timeRemaining > 0) {
      set({ timeRemaining: state.timeRemaining - 1 });
      return;
    }

    // Phase completed - determine next phase
    let nextPhase: TimerPhase;
    let nextDuration: number;
    let newCyclesCompleted = state.cyclesCompleted;

    if (state.phase === 'work') {
      // Work completed

      const sessionStore = useSessionStore.getState();

      sessionStore.addSession({
        taskId: state.currentTaskId,
        date: new Date().toISOString().split('T')[0],
        workMinutes: settings.workMin,
        breakMinutes: 0,
        attentionTimeline: sessionStore.currentAttentionTimeline,
      });

      sessionStore.clearCurrentTimeline();


      newCyclesCompleted += 1;
      
      // Long break after cyclesToLong cycles, otherwise short break
      if (newCyclesCompleted % settings.cyclesToLong === 0) {
        nextPhase = 'longBreak';
        nextDuration = settings.longBreak * 60;
      } else {
        nextPhase = 'shortBreak';
        nextDuration = settings.shortBreak * 60;
      }
    } else {
      // Break completed - back to work
      nextPhase = 'work';
      nextDuration = settings.workMin * 60;
    }

    // TODO: Play sound notification here
    // TODO: Log session to sessionStore here

    set({
      phase: nextPhase,
      timeRemaining: nextDuration,
      cyclesCompleted: newCyclesCompleted,
    });
  },
}));