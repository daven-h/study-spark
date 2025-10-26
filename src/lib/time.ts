/**
 * Format seconds to human-readable time string
 * @param totalSec - Total seconds to format
 * @returns Formatted string like "2h 30m" or "45m" or "30s"
 */
export function formatSecondsToHms(totalSec: number): string {
  if (totalSec < 60) {
    return `${totalSec}s`;
  }

  const hours = Math.floor(totalSec / 3600);
  const minutes = Math.floor((totalSec % 3600) / 60);
  const seconds = totalSec % 60;

  if (hours > 0) {
    if (minutes > 0) {
      return `${hours}h ${minutes}m`;
    }
    return `${hours}h`;
  }

  if (minutes > 0) {
    if (seconds > 0) {
      return `${minutes}m ${seconds}s`;
    }
    return `${minutes}m`;
  }

  return `${seconds}s`;
}

/**
 * Format timestamp to readable date
 * @param timestamp - Unix timestamp in milliseconds
 * @returns Formatted date like "Oct 25" or "Dec 1"
 */
export function formatDate(timestamp: number): string {
  const date = new Date(timestamp);
  const months = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
  ];

  const month = months[date.getMonth()];
  const day = date.getDate();

  return `${month} ${day}`;
}

/**
 * Format timestamp to full date string
 * @param timestamp - Unix timestamp in milliseconds
 * @returns Formatted date like "October 25, 2024"
 */
export function formatFullDate(timestamp: number): string {
  const date = new Date(timestamp);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
}

/**
 * Get start of day timestamp for a given date
 * @param timestamp - Unix timestamp in milliseconds
 * @returns Start of day timestamp
 */
export function getStartOfDay(timestamp: number): number {
  const date = new Date(timestamp);
  date.setHours(0, 0, 0, 0);
  return date.getTime();
}

/**
 * Check if two timestamps are on the same day
 * @param timestamp1 - First timestamp
 * @param timestamp2 - Second timestamp
 * @returns True if same day
 */
export function isSameDay(timestamp1: number, timestamp2: number): boolean {
  const date1 = new Date(timestamp1);
  const date2 = new Date(timestamp2);

  return date1.getFullYear() === date2.getFullYear() &&
         date1.getMonth() === date2.getMonth() &&
         date1.getDate() === date2.getDate();
}
