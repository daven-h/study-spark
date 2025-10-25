/**
 * Convert seconds to MM:SS format
 */
export function formatTime(seconds: number): string {
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}

/**
 * Get progress percentage (0-100)
 */
export function getProgress(timeRemaining: number, totalTime: number): number {
  if (totalTime === 0) return 0;
  return ((totalTime - timeRemaining) / totalTime) * 100;
}

/**
 * Get phase display name
 */
export function getPhaseLabel(phase: string): string {
  switch (phase) {
    case 'work':
      return 'Focus Time';
    case 'shortBreak':
      return 'Short Break';
    case 'longBreak':
      return 'Long Break';
    default:
      return 'Ready';
  }
}

/**
 * Calculate total duration for a phase in seconds
 */
export function getPhaseDuration(
  phase: string,
  settings: { workMin: number; shortBreak: number; longBreak: number }
): number {
  switch (phase) {
    case 'work':
      return settings.workMin * 60;
    case 'shortBreak':
      return settings.shortBreak * 60;
    case 'longBreak':
      return settings.longBreak * 60;
    default:
      return 0;
  }
}