'use client';

import Link from 'next/link';
import { useAppStore } from '@/store/app-store';
import { StatsCard } from '@/components/ui/StatsCard';
import { ProgressBar } from '@/components/ui/ProgressBar';
import { formatSecondsToHms, formatDate } from '@/lib/time';
import { useEffect, useState } from 'react';
import AddSessionSheet from '@/components/AddSessionSheet';
import { DailyGoalSheet } from '@/components/DailyGoalSheet';

export default function ProgressPage() {
  const { user, sessions, computeStats, dailyGoalMinutes } = useAppStore();
  const [stats, setStats] = useState(computeStats());
  const [todayProgress, setTodayProgress] = useState(0);

  // Update stats when sessions change
  useEffect(() => {
    setStats(computeStats());
    
    // Calculate today's progress (default goal: 2 hours = 7200 seconds)
    const today = new Date().toISOString().slice(0, 10);
    
    const todaySessions = sessions.filter(s => 
      s.completed && s.dateISO === today
    );
    
    const todaySeconds = todaySessions.reduce((sum, s) => sum + (s.minutes * 60), 0);
    const goalSeconds = dailyGoalMinutes * 60; // Convert minutes to seconds
    const progress = Math.min(100, (todaySeconds / goalSeconds) * 100);
    
    setTodayProgress(progress);
  }, [sessions, computeStats, dailyGoalMinutes]);

  const recentSessions = sessions
    .filter(s => s.completed)
    .sort((a, b) => new Date(b.dateISO).getTime() - new Date(a.dateISO).getTime())
    .slice(0, 5);

  const formatGoal = (minutes: number) => {
    if (minutes < 60) {
      return `${minutes} minutes`;
    } else if (minutes === 60) {
      return '1 hour';
    } else if (minutes % 60 === 0) {
      return `${minutes / 60} hours`;
    } else {
      const hours = Math.floor(minutes / 60);
      const remainingMinutes = minutes % 60;
      return `${hours}h ${remainingMinutes}m`;
    }
  };

  return (
    <main className="container mx-auto px-6 py-12">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-4xl font-modular text-[#3f403f]">
            Your Progress
          </h1>
          <AddSessionSheet />
        </div>

        {/* Welcome message */}
        {user && (
          <div className="text-center mb-8">
            <p className="text-lg font-norwester text-[#575b44]">
              Welcome back, {user.name}!
            </p>
          </div>
        )}

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <StatsCard
            title="Total Sessions"
            value={stats.totalSessions}
            subtitle="completed"
          />
          <StatsCard
            title="Study Time"
            value={formatSecondsToHms(stats.totalSeconds)}
            subtitle="total"
          />
          <StatsCard
            title="Current Streak"
            value={stats.currentStreak}
            subtitle="days"
          />
        </div>

        {/* Study Goals */}
        <div className="bg-[#fffbef] border border-[rgba(63,64,63,0.08)] rounded-2xl p-6 mb-8">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-2xl font-modular text-[#3f403f]">Daily Study Goal</h2>
            <DailyGoalSheet currentGoal={dailyGoalMinutes} />
          </div>
          <p className="text-[#575b44] font-norwester mb-4">
            Goal: {formatGoal(dailyGoalMinutes)} per day
          </p>
          <ProgressBar 
            progress={todayProgress} 
            showPercentage={true}
            className="mb-2"
          />
          <p className="text-sm font-norwester text-[#575b44]">
            {todayProgress >= 100 ? "Goal achieved! 🎉" : "Keep going!"}
          </p>
        </div>

        {/* Recent Activity */}
        <div className="bg-[#fffbef] border border-[rgba(63,64,63,0.08)] rounded-2xl p-6">
          <h2 className="text-2xl font-modular text-[#3f403f] mb-6">Recent Activity</h2>
          
          {recentSessions.length === 0 ? (
            <div className="text-center py-12">
              <div className="text-6xl mb-4">📚</div>
              <h3 className="text-xl font-norwester text-[#3f403f] mb-4">
                No study sessions yet
              </h3>
              <p className="text-[#575b44] font-norwester mb-6">
                Start your first study session to see your progress here.
              </p>
              <Link
                href="/methods"
                className="inline-block rounded-2xl bg-[#939f5c] text-[#3f403f] px-6 py-3 text-lg font-bold tracking-wide shadow-sm hover:bg-[#808b4f] transition font-modular uppercase"
              >
                Start Studying
              </Link>
            </div>
          ) : (
            <div className="space-y-4">
              {recentSessions.map((session) => (
                <div
                  key={session.id}
                  className="flex items-center justify-between p-4 bg-white rounded-xl border border-[rgba(63,64,63,0.08)]"
                >
                  <div className="flex items-center space-x-4">
                    <div className="w-12 h-12 bg-[#939f5c] rounded-full flex items-center justify-center">
                      <span className="text-[#3f403f] font-bold text-lg">
                        {session.method.charAt(0).toUpperCase()}
                      </span>
                    </div>
                    <div>
                      <h4 className="font-norwester text-[#3f403f]">
                        {session.title}
                      </h4>
                      <p className="text-sm font-norwester text-[#575b44] capitalize">
                        {session.method.replace('-', ' ')} • {formatDate(new Date(session.dateISO).getTime())}
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="font-modular text-[#939f5c] text-lg">
                      {session.minutes}m
                    </p>
                    <p className="text-sm font-norwester text-[#575b44]">
                      Duration
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </main>
  );
}