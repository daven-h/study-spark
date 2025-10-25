import { useTaskStore } from '@/store/taskStore';
import { useSessionStore } from '@/store/sessionStore';
import { useSettingsStore } from '@/store/settingsStore';
import { getTasks, upsertTask, getSessions, upsertSession, getSettings, upsertSettings } from './database';

/**
 * Sync local data to Supabase (on first login)
 */
export async function syncLocalToSupabase(userId: string) {
  console.log('Syncing local data to Supabase...');

  try {
    // Get local data
    const { tasks } = useTaskStore.getState();
    const { sessions } = useSessionStore.getState();
    const settings = useSettingsStore.getState();

    // Upload tasks
    for (const task of tasks) {
      await upsertTask(task, userId);
    }

    // Upload sessions
    for (const session of sessions) {
      await upsertSession(session, userId);
    }

    // Upload settings
    await upsertSettings({
      workMin: settings.workMin,
      shortBreak: settings.shortBreak,
      longBreak: settings.longBreak,
      cyclesToLong: settings.cyclesToLong,
      attentionThresholdSec: settings.attentionThresholdSec,
      yawMax: settings.yawMax,
      pitchMax: settings.pitchMax,
      adaptiveEnabled: settings.adaptiveEnabled,
      blockedSites: settings.blockedSites,
    }, userId);

    console.log('Local data synced to Supabase successfully');
  } catch (error) {
    console.error('Error syncing local data to Supabase:', error);
    throw error;
  }
}

/**
 * Sync Supabase data to local (on login)
 */
export async function syncSupabaseToLocal(userId: string) {
  console.log('Syncing Supabase data to local...');

  try {
    // Fetch data from Supabase
    const [tasks, sessions, settings] = await Promise.all([
      getTasks(userId),
      getSessions(userId),
      getSettings(userId),
    ]);

    // Update local stores
    const taskStore = useTaskStore.getState();
    const sessionStore = useSessionStore.getState();
    const settingsStore = useSettingsStore.getState();

    // Merge tasks (newer updated_at wins)
    if (tasks) {
      const localTasks = taskStore.tasks;
      const mergedTasks = mergeTasks(localTasks, tasks.map(t => ({
        id: t.id,
        title: t.title,
        estimatePomos: t.estimate_pomos,
        done: t.done,
        createdAt: t.created_at,
        updatedAt: t.updated_at,
      })));
      
      // Replace local tasks with merged
      taskStore.tasks = mergedTasks;
    }

    // Merge sessions
    if (sessions) {
      const localSessions = sessionStore.sessions;
      const mergedSessions = mergeSessions(localSessions, sessions.map(s => ({
        id: s.id,
        taskId: s.task_id,
        date: s.date,
        workMinutes: s.work_minutes,
        breakMinutes: s.break_minutes,
        attentionTimeline: s.attention_timeline,
        createdAt: s.created_at,
        updatedAt: s.updated_at,
      })));
      
      sessionStore.sessions = mergedSessions;
    }

    // Update settings (cloud wins)
    if (settings) {
      settingsStore.updateSettings({
        workMin: settings.work_min,
        shortBreak: settings.short_break,
        longBreak: settings.long_break,
        cyclesToLong: settings.cycles_to_long,
        attentionThresholdSec: settings.attention_threshold_sec,
        yawMax: settings.yaw_max,
        pitchMax: settings.pitch_max,
        adaptiveEnabled: settings.adaptive_enabled,
        blockedSites: settings.blocked_sites,
      });
    }

    console.log('Supabase data synced to local successfully');
  } catch (error) {
    console.error('Error syncing Supabase data to local:', error);
    throw error;
  }
}

/**
 * Helper: Merge tasks (newer updated_at wins)
 */
function mergeTasks(local: any[], remote: any[]) {
  const merged = new Map();

  // Add all local tasks
  local.forEach(task => merged.set(task.id, task));

  // Add/overwrite with remote tasks if newer
  remote.forEach(task => {
    const existing = merged.get(task.id);
    if (!existing || new Date(task.updatedAt) > new Date(existing.updatedAt)) {
      merged.set(task.id, task);
    }
  });

  return Array.from(merged.values());
}

/**
 * Helper: Merge sessions (newer updated_at wins)
 */
function mergeSessions(local: any[], remote: any[]) {
  const merged = new Map();

  // Add all local sessions
  local.forEach(session => merged.set(session.id, session));

  // Add/overwrite with remote sessions if newer
  remote.forEach(session => {
    const existing = merged.get(session.id);
    if (!existing || new Date(session.updatedAt) > new Date(existing.updatedAt)) {
      merged.set(session.id, session);
    }
  });

  return Array.from(merged.values());
}