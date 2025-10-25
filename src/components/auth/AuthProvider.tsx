'use client';

import { useEffect } from 'react';
import { supabase } from '@/lib/supabase/client';
import { useAppStore } from '@/store/app-store';

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const { setUser, syncUserFromSupabase } = useAppStore();

  useEffect(() => {
    let mounted = true;

    // Get initial session
    supabase.auth.getSession().then(({ data: { session }, error }) => {
      if (!mounted) return;

      if (error) {
        console.error('Error getting initial session:', error.message);
        setUser(null);
      } else if (session?.user) {
        // Convert Supabase user to our User type
        const user = {
          id: session.user.id,
          email: session.user.email,
          name: session.user.user_metadata?.full_name || session.user.user_metadata?.name,
          avatarUrl: session.user.user_metadata?.avatar_url
        };
        setUser(user);
      } else {
        setUser(null);
      }
    });

    // Listen for auth changes (login, logout, token refresh)
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      if (!mounted) return;
      
      if (session?.user) {
        // Convert Supabase user to our User type
        const user = {
          id: session.user.id,
          email: session.user.email,
          name: session.user.user_metadata?.full_name || session.user.user_metadata?.name,
          avatarUrl: session.user.user_metadata?.avatar_url
        };
        setUser(user);
      } else {
        setUser(null);
      }
    });

    // cleanup on unmount
    return () => {
      mounted = false;
      subscription.unsubscribe();
    };
  }, [setUser]);

  return <>{children}</>;
}
