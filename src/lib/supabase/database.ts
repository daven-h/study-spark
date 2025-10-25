import { supabase } from './client';
import { Task } from '@/types/task';
import { Session } from '@/types/session';
import { Settings } from '@/types/settings';

export async function getTasks(userId: string) {
  const { data, error } = await supabase
    .from('tasks')
    .select('*')
    .eq('user_id', userId)
    .order('created_at', { ascending: false });

  if (error) throw error;
  return data;
}

export async function upsertTask(task: Task, userId: string) {
  const { data, error } = await supabase
    .from('tasks')
    .upsert({
      id: task.id,
      user_id: userId,
      title: task.title,
      estimate_pomos: task.estimatePomos,
      done: task.done,
      created_at: task.createdAt,
      updated_at: task.updatedAt,
    })
    .select()
    .single();

  if (error) throw error;
  return data;
}

export async function deleteTask(taskId: string) {
  const { error } = await supabase
    .from('tasks')
    .delete()
    .eq('id', taskId);

  if (error) throw error;
}

/**
 * Sessions
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