
'use client';

import { usePomodoroTest } from '@/hooks/usePomodoroTest';
import { Button } from '@/components/ui/button';
import { formatTime } from '@/lib/pomodoro/timer';

export default function TestPage() {
  const {
    // Controls
    startTimer,
    pauseTimer,
    resumeTimer,
    skipPhase,
    resetTimer,
    
    // State
    phase,
    status,
    timeRemaining,
    cyclesCompleted,
    
    // Data
    sessions,
    todayStats,
    settings,
  } = usePomodoroTest();

  return (
    <main className="container max-w-4xl mx-auto py-8 px-4">
      <h1 className="text-3xl font-bold mb-8">Pomodoro Test Page</h1>

      {/* Timer Display */}
      <div className="bg-gray-100 p-8 rounded-lg mb-6">
        <div className="text-center">
          <p className="text-sm text-gray-600 mb-2">Phase</p>
          <p className="text-2xl font-bold mb-4 capitalize">{phase}</p>
          
          <p className="text-sm text-gray-600 mb-2">Time Remaining</p>
          <p className="text-6xl font-bold mb-4 font-mono">{formatTime(timeRemaining)}</p>
          
          <p className="text-sm text-gray-600 mb-2">Status</p>
          <p className="text-xl font-semibold capitalize mb-4">{status}</p>
          
          <p className="text-sm text-gray-600 mb-2">Cycles Completed</p>
          <p className="text-xl font-semibold">{cyclesCompleted}</p>
        </div>
      </div>

      {/* Controls */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
        <Button onClick={() => startTimer('test-task')} disabled={status === 'running'}>
          Start Timer
        </Button>
        <Button onClick={pauseTimer} disabled={status !== 'running'}>
          Pause
        </Button>
        <Button onClick={resumeTimer} disabled={status !== 'paused'}>
          Resume
        </Button>
        <Button onClick={skipPhase} disabled={status === 'idle'}>
          Skip Phase
        </Button>
      </div>

      <div className="mb-6">
        <Button onClick={resetTimer} variant="destructive" className="w-full">
          Reset Timer
        </Button>
      </div>

      {/* Today's Stats */}
      <div className="bg-blue-50 p-6 rounded-lg mb-6">
        <h2 className="text-xl font-bold mb-4">Today&apos;s Stats</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div>
            <p className="text-sm text-gray-600">Total Focus Time</p>
            <p className="text-2xl font-bold">{todayStats.totalFocusTime}m</p>
          </div>
          <div>
            <p className="text-sm text-gray-600">Cycles Completed</p>
            <p className="text-2xl font-bold">{todayStats.cyclesCompleted}</p>
          </div>
          <div>
            <p className="text-sm text-gray-600">Attention Score</p>
            <p className="text-2xl font-bold">{todayStats.attentionScore}%</p>
          </div>
          <div>
            <p className="text-sm text-gray-600">Most Distracted</p>
            <p className="text-2xl font-bold">
              {todayStats.mostDistractedMinute !== null 
                ? `Min ${todayStats.mostDistractedMinute}` 
                : 'N/A'}
            </p>
          </div>
        </div>
      </div>

      {/* Current Settings */}
      <div className="bg-gray-50 p-6 rounded-lg mb-6">
        <h2 className="text-xl font-bold mb-4">Current Settings</h2>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4 text-sm">
          <div>
            <p className="text-gray-600">Work Duration</p>
            <p className="font-semibold">{settings.workMin} min</p>
          </div>
          <div>
            <p className="text-gray-600">Short Break</p>
            <p className="font-semibold">{settings.shortBreak} min</p>
          </div>
          <div>
            <p className="text-gray-600">Long Break</p>
            <p className="font-semibold">{settings.longBreak} min</p>
          </div>
          <div>
            <p className="text-gray-600">Cycles to Long</p>
            <p className="font-semibold">{settings.cyclesToLong}</p>
          </div>
          <div>
            <p className="text-gray-600">Adaptive</p>
            <p className="font-semibold">{settings.adaptiveEnabled ? 'On' : 'Off'}</p>
          </div>
        </div>
      </div>

      {/* Session History */}
      <div className="bg-white border rounded-lg p-6">
        <h2 className="text-xl font-bold mb-4">Session History ({sessions.length})</h2>
        {sessions.length === 0 ? (
          <p className="text-gray-500">No sessions yet. Complete a work session to see data here.</p>
        ) : (
          <div className="space-y-3">
            {sessions.slice(-10).reverse().map((session) => (
              <div key={session.id} className="border-l-4 border-blue-500 pl-4 py-2">
                <div className="flex justify-between items-start">
                  <div>
                    <p className="font-semibold">
                      {new Date(session.date).toLocaleString()}
                    </p>
                    <p className="text-sm text-gray-600">
                      Work: {session.workMinutes}m | 
                      Task ID: {session.taskId || 'None'}
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm text-gray-600">Attention Data</p>
                    <p className="font-semibold">
                      {session.attentionTimeline.length} samples
                    </p>
                    <p className="text-sm">
                      Avg: {Math.round(
                        (session.attentionTimeline.reduce((a, b) => a + b, 0) / 
                        session.attentionTimeline.length) * 100
                      )}%
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Instructions */}
      <div className="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded">
        <h3 className="font-bold mb-2">Testing Instructions:</h3>
        <ol className="list-decimal list-inside space-y-1 text-sm">
          <li>Click &quot;Start Timer&quot; to begin a work session</li>
          <li>Use &quot;Skip Phase&quot; to fast-forward through phases</li>
          <li>Check &quot;Session History&quot; after completing work sessions</li>
          <li>Verify attention data is being recorded automatically</li>
          <li>Test Pause/Resume functionality</li>
        </ol>
      </div>
    </main>
  );
}