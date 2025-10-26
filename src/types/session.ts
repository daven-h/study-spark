export interface Session{
    id: string;
    taskId: string | null;
    date: string;
    workMinutes: number;
    breakMinutes: number;
    attentionTimeline: number[]; // Score per second
    createdAt:string;
    updatedAt:string;
}

export interface SessionStats{
    totalFocusTime: number;
    cyclesCompleted: number;
    attentionScore: number;
    mostDistractedMinute: number | null; // minute with the lowest score

}