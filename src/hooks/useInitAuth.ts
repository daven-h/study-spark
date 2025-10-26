// hooks/useInitAuth.ts
'use client';

import { useEffect } from 'react';
import { supabase } from '@/lib/supabase/client'; // adjust path
import { useAuthStore } from '@/store/authStore';

export function useInitAuth() {
  const { setUser, setLoading } = useAuthStore();

  useEffect(() => {
    let mounted = true;

    async function load() {
      // 1. Get current user from Supabase
      const { data, error } = await supabase.auth.getUser();

      if (mounted) {
        if (error) {
          console.error('Auth init error:', error.message);
          setUser(null);
        } else {
          setUser(data.user ?? null);
        }
        setLoading(false);
      }

      // 2. Subscribe to auth state changes (login/logout)
      const { data: sub } = supabase.auth.onAuthStateChange((_event, session) => {
        // session will be null on signout
        setUser(session?.user ?? null);
      });

      // cleanup
      return () => {
        sub.subscription.unsubscribe();
      };
    }

    load();

    return () => {
      mounted = false;
    };
  }, [setUser, setLoading]);
}
