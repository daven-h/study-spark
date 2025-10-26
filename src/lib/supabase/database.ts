import { supabase } from './client';
import { Session } from '@/types/session';
import { Settings } from '@/types/settings';
import { Session as AppSession } from '@/types';

/**
 * Sessions (old pomodoro sessions - kept for backward compatibility)
 */
export async function getSessions(userId: string) {
  const { data, error } = await supabase
    .from('sessions')
    .select('*')
    .eq('user_id', userId)
    .order('date', { ascending: false });

  if (error) throw error;
  return data;
}

export async function upsertSession(session: Session, userId: string) {
  const { data, error } = await supabase
    .from('sessions')
    .upsert({
      id: session.id,
      user_id: userId,
      task_id: session.taskId,
      date: session.date,
      work_minutes: session.workMinutes,
      break_minutes: session.breakMinutes,
      attention_timeline: session.attentionTimeline,
      created_at: session.createdAt,
      updated_at: session.updatedAt,
    })
    .select()
    .single();

  if (error) throw error;
  return data;
}

/**
 * Get AppSessions (from app-store) from Supabase
 */
export async function getAppSessions(userId: string) {
  const { data, error } = await supabase
    .from('app_sessions')
    .select('*')
    .eq('user_id', userId)
    .order('created_at', { ascending: false });

  if (error) throw error;

  // Transform database format to app format
  return data?.map(row => ({
    id: row.id,
    task: row.task,
    method: row.method,
    completed: row.completed,
    minutes: row.minutes,
    dateISO: row.date_iso,
    createdAt: new Date(row.created_at).getTime(),
  })) || [];
}

/**
 * Upsert AppSession (from app-store) to Supabase
 */
export async function upsertAppSession(session: AppSession, userId: string) {
  const { data, error } = await supabase
    .from('app_sessions')
    .upsert({
      id: session.id,
      user_id: userId,
      task: session.task,
      method: session.method,
      completed: session.completed,
      minutes: session.minutes,
      date_iso: session.dateISO,
      created_at: new Date(session.createdAt).toISOString(),
    })
    .select()
    .single();

  if (error) throw error;
  return data;
}

/**
 * Settings
 */
export async function getSettings(userId: string) {
  const { data, error } = await supabase
    .from('settings')
    .select('*')
    .eq('user_id', userId)
    .single();

  if (error && error.code !== 'PGRST116') throw error; // PGRST116 = no rows
  return data;
}

export async function upsertSettings(settings: Settings, userId: string) {
  const { data, error } = await supabase
    .from('settings')
    .upsert({
      user_id: userId,
      work_min: settings.workMin,
      short_break: settings.shortBreak,
      long_break: settings.longBreak,
      cycles_to_long: settings.cyclesToLong,
      attention_threshold_sec: settings.attentionThresholdSec,
      yaw_max: settings.yawMax,
      pitch_max: settings.pitchMax,
      adaptive_enabled: settings.adaptiveEnabled,
      blocked_sites: settings.blockedSites,
    })
    .select()
    .single();

  if (error) throw error;
  return data;
}