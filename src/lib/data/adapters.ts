import { DataAdapter, User, Session } from '@/types';
import { useAppStore } from '@/store/app-store';

// Local adapter that wraps the Zustand store
class LocalAdapter implements DataAdapter {
  async signInGoogle(): Promise<User> {
    return useAppStore.getState().signInGoogle();
  }

  async signOut(): Promise<void> {
    useAppStore.getState().signOut();
  }

  async addSession(session: Session): Promise<void> {
    useAppStore.getState().addSession(session);
  }

  async endSession(sessionId: string, endedAt: number): Promise<void> {
    useAppStore.getState().endSession(sessionId, endedAt);
  }

  async getSessions(): Promise<Session[]> {
    return useAppStore.getState().sessions;
  }

  async getUser(): Promise<User | null> {
    return useAppStore.getState().user;
  }
}

// Supabase adapter (stubs for now)
class SupabaseAdapter implements DataAdapter {
  async signInGoogle(): Promise<User> {
    // TODO: Implement Supabase OAuth
    throw new Error('Supabase auth not implemented yet');
  }

  async signOut(): Promise<void> {
    // TODO: Implement Supabase sign out
    throw new Error('Supabase sign out not implemented yet');
  }

  async addSession(session: Session): Promise<void> {
    // TODO: Implement Supabase session creation
    throw new Error('Supabase session creation not implemented yet');
  }

  async endSession(sessionId: string, endedAt: number): Promise<void> {
    // TODO: Implement Supabase session update
    throw new Error('Supabase session update not implemented yet');
  }

  async getSessions(): Promise<Session[]> {
    // TODO: Implement Supabase session fetching
    throw new Error('Supabase session fetching not implemented yet');
  }

  async getUser(): Promise<User | null> {
    // TODO: Implement Supabase user fetching
    throw new Error('Supabase user fetching not implemented yet');
  }
}

/**
 * Get the appropriate data adapter based on environment variables
 * @returns LocalAdapter if no Supabase env vars, SupabaseAdapter if present
 */
export function getDataAdapter(): DataAdapter {
  const hasSupabaseConfig = 
    process.env.NEXT_PUBLIC_SUPABASE_URL && 
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

  if (hasSupabaseConfig) {
    return new SupabaseAdapter();
  }

  return new LocalAdapter();
}

// Export adapters for testing
export { LocalAdapter, SupabaseAdapter };
