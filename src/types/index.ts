export type MethodSlug = 
  | "pomodoro" 
  | "flowtime" 
  | "52-17" 
  | "deep-work-90-20" 
  | "blurting-sprint" 
  | "phone-free-sprint";

export interface User {
  id: string;
  name?: string;
  avatarUrl?: string;
}

export interface Session {
  id: string;
  method: MethodSlug;
  startedAt: number;
  endedAt?: number;
  durationSec?: number;
  notes?: string;
}

export interface Stats {
  totalSessions: number;
  totalSeconds: number;
  currentStreak: number;
  lastStudyDate?: string;
}

export interface AppState {
  user: User | null;
  sessions: Session[];
  lastMethod?: MethodSlug;
}

export interface DataAdapter {
  signInGoogle(): Promise<User>;
  signOut(): Promise<void>;
  addSession(session: Session): Promise<void>;
  endSession(sessionId: string, endedAt: number): Promise<void>;
  getSessions(): Promise<Session[]>;
  getUser(): Promise<User | null>;
}
