import { Session } from '@/types/session';

/**
 * Format session date for display
 */
export function formatSessionDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  });
}

/**
 * Get time of day label
 */
export function getTimeOfDay(dateString: string): string {
  const hour = new Date(dateString).getHours();
  
  if (hour < 12) return 'Morning';
  if (hour < 17) return 'Afternoon';
  if (hour < 21) return 'Evening';
  return 'Night';
}

/**
 * Group sessions by date
 */
export function groupSessionsByDate(sessions: Session[]): Record<string, Session[]> {
  return sessions.reduce((groups, session) => {
    const date = session.date.split('T')[0];
    if (!groups[date]) {
      groups[date] = [];
    }
    groups[date].push(session);
    return groups;
  }, {} as Record<string, Session[]>);
}

/**
 * Calculate total focus time for sessions (in minutes)
 */
export function getTotalFocusTime(sessions: Session[]): number {
  return sessions.reduce((total, session) => total + session.workMinutes, 0);
}

/**
 * Format minutes to readable string
 */
export function formatDuration(minutes: number): string {
  const hours = Math.floor(minutes / 60);
  const mins = minutes % 60;
  
  if (hours === 0) return `${mins}m`;
  if (mins === 0) return `${hours}h`;
  return `${hours}h ${mins}m`;
}