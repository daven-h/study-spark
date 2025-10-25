export type MethodSlug = 
  | "pomodoro" 
  | "52-17" 
  | "deep-work-90-20" 
  | "phone-free-sprint";

export interface User {
  id: string;
  email?: string;
  name?: string;
  avatarUrl?: string;
}

export interface Session {
  id: string;
  title: string;
  method: MethodSlug;
  completed: boolean;
  minutes: number;           // whole minutes focused
  dateISO: string;           // yyyy-mm-dd
  createdAt: number;
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
