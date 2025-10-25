import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { AppState, User, Session, Stats, MethodSlug } from '@/types';
import { isSameDay, getStartOfDay } from '@/lib/time';

interface AppStore extends AppState {
  // Actions
  signInGoogle: () => Promise<User>;
  signOut: () => void;
  addSession: (session: Session) => void;
  endSession: (sessionId: string, endedAt: number) => void;
  setLastMethod: (method: MethodSlug) => void;
  computeStats: () => Stats;
  setUser: (user: User | null) => void;
}

export const useAppStore = create<AppStore>()(
  persist(
    (set, get) => ({
      // Initial state
      user: null,
      sessions: [],
      lastMethod: undefined,

      // Actions
      signInGoogle: async () => {
        // For now, create a local fake user
        // TODO: Integrate with Supabase when env vars are present
        const user: User = {
          id: 'local-uid',
          name: 'You',
          avatarUrl: undefined
        };
        
        set({ user });
        return user;
      },

      signOut: () => {
        set({ user: null });
      },

      addSession: (session: Session) => {
        set((state) => ({
          sessions: [...state.sessions, session],
          lastMethod: session.method
        }));
      },

      endSession: (sessionId: string, endedAt: number) => {
        set((state) => ({
          sessions: state.sessions.map((session) =>
            session.id === sessionId
              ? {
                  ...session,
                  endedAt,
                  durationSec: endedAt - session.startedAt
                }
              : session
          )
        }));
      },

      setLastMethod: (method: MethodSlug) => {
        set({ lastMethod: method });
      },

      setUser: (user: User | null) => {
        set({ user });
      },

      computeStats: () => {
        const { sessions } = get();
        
        if (sessions.length === 0) {
          return {
            totalSessions: 0,
            totalSeconds: 0,
            currentStreak: 0
          };
        }

        // Calculate total sessions and time
        const completedSessions = sessions.filter(s => s.endedAt && s.durationSec);
        const totalSessions = completedSessions.length;
        const totalSeconds = completedSessions.reduce((sum, s) => sum + (s.durationSec || 0), 0);

        // Calculate current streak
        const now = Date.now();
        const today = getStartOfDay(now);
        let currentStreak = 0;
        
        // Get unique study days (sorted by date, most recent first)
        const studyDays = Array.from(
          new Set(
            completedSessions
              .map(s => getStartOfDay(s.startedAt))
              .sort((a, b) => b - a)
          )
        );

        // Count consecutive days from today backwards
        let checkDate = today;
        for (const studyDay of studyDays) {
          if (isSameDay(checkDate, studyDay)) {
            currentStreak++;
            checkDate -= 24 * 60 * 60 * 1000; // Subtract one day
          } else if (studyDay < checkDate) {
            // Gap found, streak ends
            break;
          }
        }

        // Get last study date
        const lastStudyDate = studyDays.length > 0 
          ? new Date(studyDays[0]).toISOString().split('T')[0]
          : undefined;

        return {
          totalSessions,
          totalSeconds,
          currentStreak,
          lastStudyDate
        };
      }
    }),
    {
      name: 'study-spark/v1',
      // Only persist user and sessions, not computed values
      partialize: (state) => ({
        user: state.user,
        sessions: state.sessions,
        lastMethod: state.lastMethod
      })
    }
  )
);
