import { useSettingsStore } from '@/store/settingsStore';

/**
 * Calculate average attention score from timeline
 * @param attentionTimeline - Array of attention scores (0-1) per second
 */
export function calculateAverageAttention(attentionTimeline: number[]): number {
  if (attentionTimeline.length === 0) return 1;
  
  const sum = attentionTimeline.reduce((acc, score) => acc + score, 0);
  return sum / attentionTimeline.length;
}

/**
 * Adjust work duration based on attention performance
 * @param averageAttention - Average attention score (0-1)
 * @returns New work duration in minutes
 */
export function adjustWorkDuration(averageAttention: number): number {
  const settings = useSettingsStore.getState();
  
  if (!settings.adaptiveEnabled) {
    return settings.workMin; // No adjustment if disabled
  }

  let newWorkMin = settings.workMin;

  // Poor attention (<60%) - decrease work time
  if (averageAttention < 0.6) {
    newWorkMin = Math.max(20, settings.workMin - 5);
  }
  // Excellent attention (>90%) - increase work time
  else if (averageAttention > 0.9) {
    newWorkMin = Math.min(35, settings.workMin + 5);
  }
  // 60-90% attention - keep current duration

  return newWorkMin;
}

/**
 * Get recommendation message for user
 */
export function getAdaptiveMessage(
  averageAttention: number,
  newDuration: number,
  oldDuration: number
): string | null {
  if (newDuration === oldDuration) return null;

  if (newDuration < oldDuration) {
    return `Your attention was ${(averageAttention * 100).toFixed(0)}%. Next session shortened to ${newDuration} minutes.`;
  } else {
    return `Great focus! (${(averageAttention * 100).toFixed(0)}%) Next session extended to ${newDuration} minutes.`;
  }
}
