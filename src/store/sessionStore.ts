import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { Session, SessionStats } from '@/types/session';

interface SessionState {
  sessions: Session[];
  currentAttentionTimeline: number[]; // Build this during active session
  
  // Actions
  addSession: (session: Omit<Session, 'id' | 'createdAt' | 'updatedAt'>) => void;
  recordAttention: (score: number) => void; // Called every second during work
  clearCurrentTimeline: () => void;
  getSessionsByDate: (date: string) => Session[];
  getSessionStats: (sessionId: string) => SessionStats | null;
  getTodayStats: () => SessionStats;
}

export const useSessionStore = create<SessionState>()(
  persist(
    (set, get) => ({
      sessions: [],
      currentAttentionTimeline: [],

      addSession: (sessionData) => {
        const newSession: Session = {
          ...sessionData,
          id: crypto.randomUUID(),
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
        };

        set((state) => ({
          sessions: [...state.sessions, newSession],
        }));
      },

      recordAttention: (score) => {
        set((state) => ({
          currentAttentionTimeline: [...state.currentAttentionTimeline, score],
        }));
      },

      clearCurrentTimeline: () => {
        set({ currentAttentionTimeline: [] });
      },

      getSessionsByDate: (date) => {
        const { sessions } = get();
        return sessions.filter((session) => session.date.startsWith(date));
      },

      getSessionStats: (sessionId) => {
        const { sessions } = get();
        const session = sessions.find((s) => s.id === sessionId);
        
        if (!session || session.attentionTimeline.length === 0) {
          return null;
        }

        return calculateSessionStats(session);
      },

      getTodayStats: () => {
        const { sessions } = get();
        const today = new Date().toISOString().split('T')[0];
        const todaySessions = sessions.filter((s) => s.date.startsWith(today));

        if (todaySessions.length === 0) {
          return {
            totalFocusTime: 0,
            cyclesCompleted: 0,
            attentionScore: 0,
            mostDistractedMinute: null,
          };
        }

        // Aggregate stats from all today's sessions
        const totalFocusTime = todaySessions.reduce(
          (sum, s) => sum + s.workMinutes,
          0
        );
        const cyclesCompleted = todaySessions.length;

        // Calculate average attention across all sessions
        const allScores = todaySessions.flatMap((s) => s.attentionTimeline);
        const avgAttention =
          allScores.length > 0
            ? allScores.reduce((sum, score) => sum + score, 0) / allScores.length
            : 0;

        return {
          totalFocusTime,
          cyclesCompleted,
          attentionScore: Math.round(avgAttention * 100),
          mostDistractedMinute: null, // Can implement later
        };
      },
    }),
    {
      name: 'session-storage',
    }
  )
);

/**
 * Calculate stats for a single session
 */
function calculateSessionStats(session: Session): SessionStats {
  const { attentionTimeline, workMinutes } = session;

  // Average attention score
  const avgAttention =
    attentionTimeline.reduce((sum, score) => sum + score, 0) /
    attentionTimeline.length;

  // Find most distracted minute
  let mostDistractedMinute: number | null = null;
  let lowestAvg = 1;

  // Group by minute and find lowest
  for (let min = 0; min < workMinutes; min++) {
    const startIdx = min * 60;
    const endIdx = Math.min(startIdx + 60, attentionTimeline.length);
    const minuteScores = attentionTimeline.slice(startIdx, endIdx);

    if (minuteScores.length > 0) {
      const minuteAvg =
        minuteScores.reduce((sum, score) => sum + score, 0) / minuteScores.length;

      if (minuteAvg < lowestAvg) {
        lowestAvg = minuteAvg;
        mostDistractedMinute = min;
      }
    }
  }

  return {
    totalFocusTime: workMinutes,
    cyclesCompleted: 1,
    attentionScore: Math.round(avgAttention * 100),
    mostDistractedMinute,
  };
}