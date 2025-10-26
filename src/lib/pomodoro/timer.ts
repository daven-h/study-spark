export function formatTime(seconds: number): string {
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}

export function secondsToMinutes(seconds: number): number {
  return Math.floor(seconds / 60);
}

export function minutesToSeconds(minutes: number): number {
  return minutes * 60;
}
