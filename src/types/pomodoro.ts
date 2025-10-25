export type TimerPhase = 'work' | 'shortBreak' | 'longBreak' | 'idle';

export type TimerStatus = 'running' | 'paused' | 'idle';

export interface PomodoroState {
  phase: TimerPhase;
  status: TimerStatus;
  timeRemaining: number; // in seconds
  cyclesCompleted: number;
  currentTaskId: string | null;
}
