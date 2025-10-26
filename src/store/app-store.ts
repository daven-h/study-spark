import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { AppState, User, Session, Stats, MethodSlug } from '@/types';
import { isSameDay, getStartOfDay } from '@/lib/time';
import { signInWithGoogle, signOut as supabaseSignOut, getCurrentUser } from '@/lib/supabase/auth';

interface AppStore extends AppState {
  // Actions
  signInGoogle: () => Promise<User>;
  signOut: () => Promise<void>;
  syncUserFromSupabase: () => Promise<void>;
  addSession: (session: Session) => void;
  endSession: (sessionId: string, endedAt: number) => void;
  setLastMethod: (method: MethodSlug) => void;
  computeStats: () => Stats;
  setUser: (user: User | null) => void;
  setDailyGoal: (minutes: number) => void;
}

export const useAppStore = create<AppStore>()(
  persist(
    (set, get) => ({
      // Initial state
      user: null,
      sessions: [],
      lastMethod: undefined,
      dailyGoalMinutes: 120, // Default: 2 hours = 120 minutes

      // Actions
      signInGoogle: async () => {
        try {
          // Check if we have Supabase env vars
          if (process.env.NEXT_PUBLIC_SUPABASE_URL && process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY) {
            // Use real Google auth
            await signInWithGoogle();
            // The user will be redirected to auth callback, then back to the app
            // The auth state will be handled by the auth provider
            return {
              id: 'pending',
              email: 'pending',
              name: 'pending'
            };
          } else {
            // Fallback to local fake user for development
            const user: User = {
              id: 'local-uid',
              email: 'you@example.com',
              name: 'You',
              avatarUrl: undefined
            };
            
            set({ user });
            return user;
          }
        } catch (error) {
          console.error('Google sign in error:', error);
          throw error;
        }
      },

      signOut: async () => {
        try {
          if (process.env.NEXT_PUBLIC_SUPABASE_URL && process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY) {
            await supabaseSignOut();
          }
          set({ user: null });
        } catch (error) {
          console.error('Sign out error:', error);
          // Still clear local state even if Supabase sign out fails
          set({ user: null });
        }
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

      setDailyGoal: (minutes: number) => {
        set({ dailyGoalMinutes: minutes });
      },

      syncUserFromSupabase: async () => {
        try {
          if (process.env.NEXT_PUBLIC_SUPABASE_URL && process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY) {
            const supabaseUser = await getCurrentUser();
            if (supabaseUser) {
              const user: User = {
                id: supabaseUser.id,
                email: supabaseUser.email,
                name: supabaseUser.user_metadata?.full_name || supabaseUser.user_metadata?.name,
                avatarUrl: supabaseUser.user_metadata?.avatar_url
              };
              set({ user });
            } else {
              set({ user: null });
            }
          }
        } catch (error) {
          console.error('Error syncing user from Supabase:', error);
        }
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
        const completedSessions = sessions.filter(s => s.completed);
        const totalSessions = completedSessions.length;
        const totalSeconds = completedSessions.reduce((sum, s) => sum + (s.minutes * 60), 0);

        // Calculate current streak
        const now = Date.now();
        const today = getStartOfDay(now);
        let currentStreak = 0;
        
        // Get unique study days (sorted by date, most recent first)
        const studyDays = Array.from(
          new Set(
            completedSessions
              .map(s => getStartOfDay(new Date(s.dateISO).getTime()))
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
        lastMethod: state.lastMethod,
        dailyGoalMinutes: state.dailyGoalMinutes
      })
    }
  )
);
