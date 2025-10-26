import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { AppState, User, Session, Stats, MethodSlug } from '@/types';
import { isSameDay, getStartOfDay } from '@/lib/time';
import { signInWithGoogle, signOut as supabaseSignOut, getCurrentUser } from '@/lib/supabase/auth';
import { upsertAppSession, getAppSessions } from '@/lib/supabase/database';

interface AppStore extends AppState {
  // Actions
  signInGoogle: () => Promise<User>;
  signOut: () => Promise<void>;
  syncUserFromSupabase: () => Promise<void>;
  loadUserSessions: (userId: string) => Promise<void>;
  addSession: (session: Session) => Promise<void>;
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
          // Clear all user data on sign out
          set({
            user: null,
            sessions: [],
            lastMethod: undefined
          });
        } catch (error) {
          console.error('Sign out error:', error);
          // Still clear local state even if Supabase sign out fails
          set({
            user: null,
            sessions: [],
            lastMethod: undefined
          });
        }
      },

      addSession: async (session: Session) => {
        // Update local state first
        set((state) => ({
          sessions: [...state.sessions, session],
          lastMethod: session.method
        }));

        // Sync to Supabase if user is logged in
        const { user } = get();
        if (user) {
          try {
            console.log('Syncing session to Supabase:', session);
            await upsertAppSession(session, user.id);
            console.log('Session synced successfully to Supabase');
          } catch (error) {
            console.error('Error syncing session to Supabase:', error);
          }
        } else {
          console.log('No user logged in, skipping Supabase sync');
        }
      },

      setLastMethod: (method: MethodSlug) => {
        set({ lastMethod: method });
      },

      setUser: (user: User | null) => {
        set({ user });
      },

      loadUserSessions: async (userId: string) => {
        try {
          console.log('Loading sessions from Supabase for user:', userId);
          const sessions = await getAppSessions(userId);
          console.log('Loaded sessions:', sessions);
          set({ sessions });
        } catch (error) {
          console.error('Error loading sessions from Supabase:', error);
        }
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
        const yesterday = today - 24 * 60 * 60 * 1000;
        let currentStreak = 0;

        // Get unique study days (sorted by date, most recent first)
        const studyDays = Array.from(
          new Set(
            completedSessions
              .map(s => getStartOfDay(new Date(s.dateISO).getTime()))
          )
        ).sort((a, b) => b - a);

        if (studyDays.length > 0) {
          const mostRecentStudyDay = studyDays[0];

          // Only count streak if most recent study is today or yesterday
          // This keeps the streak alive if you studied yesterday but not yet today
          if (mostRecentStudyDay >= yesterday) {
            // Start counting from the most recent study day
            let checkDate = mostRecentStudyDay;

            for (const studyDay of studyDays) {
              if (isSameDay(checkDate, studyDay)) {
                currentStreak++;
                checkDate -= 24 * 60 * 60 * 1000; // Move to previous day
              } else if (studyDay < checkDate) {
                // Gap found, streak ends
                break;
              }
            }
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
      // Only persist lastMethod
      // User and sessions come from Supabase, not localStorage
      partialize: (state) => ({
        lastMethod: state.lastMethod
      })
    }
  )
);
