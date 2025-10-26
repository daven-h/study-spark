'use client';

import { useState, useRef, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAppStore } from '@/store/app-store';
import { Button } from '@/components/ui/button';
import FocusAlert from '@/components/FocusAlert';

interface AttentionData {
  attention_score: number;
  eye_ar: number;
  mouth_ar: number;
  head_tilt: number;
  phone_detected: boolean;
  fps: number;
  timestamp: number;
  focus_status: string;
  session_active: boolean;
}

export default function FocusSessionPage() {
  const router = useRouter();
  const { addSession, lastMethod } = useAppStore();
  const [isSessionActive, setIsSessionActive] = useState(false);
  const [sessionDuration, setSessionDuration] = useState(0);
  const [sessionStartTime, setSessionStartTime] = useState<number | null>(null);
  const [isClient, setIsClient] = useState(false);
  const [attentionData, setAttentionData] = useState<AttentionData>({
    attention_score: 0,
    eye_ar: 0,
    mouth_ar: 0,
    head_tilt: 0,
    phone_detected: false,
    fps: 0,
    timestamp: 0,
    focus_status: 'unknown',
    session_active: false
  });
  const [websocketConnected, setWebsocketConnected] = useState(false);
  const [apiConnected, setApiConnected] = useState(false);
  const videoRef = useRef<HTMLVideoElement>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);
  const websocketRef = useRef<WebSocket | null>(null);
  const pollingRef = useRef<NodeJS.Timeout | null>(null);

  // Set client-side flag to prevent hydration issues
  useEffect(() => {
    setIsClient(true);
  }, []);

  // Connect to HTTP API server
  useEffect(() => {
    if (isClient) {
      connectToAPI();
    }
    return () => {
      disconnectFromAPI();
    };
  }, [isClient]);

  // Start camera when component mounts
  useEffect(() => {
    if (isClient) {
      startCamera();
    }
    return () => {
      stopCamera();
    };
  }, [isClient]);

  const connectToAPI = async () => {
    try {
      const response = await fetch('http://localhost:8765/api/ping');
      if (response.ok) {
        setApiConnected(true);
        console.log('API server connected');
      } else {
        setApiConnected(false);
        console.log('API server not responding');
      }
    } catch (error) {
      console.error('Failed to connect to API:', error);
      setApiConnected(false);
    }
  };

  const disconnectFromAPI = () => {
    if (pollingRef.current) {
      clearInterval(pollingRef.current);
      pollingRef.current = null;
    }
    setApiConnected(false);
  };

  const sendAPICommand = async (command: string) => {
    if (!apiConnected) return;
    
    try {
      const endpoint = command === 'start_tracking' ? 'start_tracking' : 
                     command === 'stop_tracking' ? 'stop_tracking' : 'ping';
      
      const response = await fetch(`http://localhost:8765/api/${endpoint}`, {
        method: endpoint === 'ping' ? 'GET' : 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      if (response.ok) {
        const data = await response.json();
        console.log(`API command ${command}:`, data);
        return data;
      }
    } catch (error) {
      console.error(`API command ${command} failed:`, error);
    }
  };

  const pollAttentionData = () => {
    if (!apiConnected) return;
    
    const poll = async () => {
      try {
        const response = await fetch('http://localhost:8765/api/attention_data', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });
        if (response.ok) {
          const data = await response.json();
          if (data.success) {
            setAttentionData(data.data);
          }
        } else {
          console.error('API responded with error:', response.status);
        }
      } catch (error) {
        console.error('Failed to poll attention data:', error);
        // Don't spam the console with errors
        if (Math.random() < 0.1) { // Only log 10% of errors
          console.error('Polling error:', error);
        }
      }
    };
    
    // Poll every 100ms (10 Hz)
    pollingRef.current = setInterval(poll, 100);
  };

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          width: { ideal: 1280 },
          height: { ideal: 720 },
          facingMode: 'user'
        }
      });
      
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        streamRef.current = stream;
      }
    } catch (error) {
      console.error('Error accessing camera:', error);
      // Fallback: show a placeholder or message
    }
  };

  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
  };

  const startSession = async () => {
    setIsSessionActive(true);
    const startTime = Date.now();
    setSessionStartTime(startTime);
    setSessionDuration(0);
    
    // Start attention tracking via API
    await sendAPICommand('start_tracking');
    pollAttentionData();
    
    // Start timer
    intervalRef.current = setInterval(() => {
      setSessionDuration(Math.floor((Date.now() - startTime) / 1000));
    }, 1000);
  };

  const stopSession = async () => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
    }
    
    // Stop attention tracking via API
    await sendAPICommand('stop_tracking');
    disconnectFromAPI();
    
    setIsSessionActive(false);
    
    // Calculate session duration in minutes
    const durationMinutes = Math.floor(sessionDuration / 60);
    
    // Create session record with attention data
    const session = {
      id: `session-${Date.now()}`,
      task: `${lastMethod ? lastMethod.replace('-', ' ') : 'Study'} Session`,
      method: lastMethod || 'pomodoro',
      completed: true,
      minutes: durationMinutes,
      dateISO: new Date().toISOString().split('T')[0],
      createdAt: Date.now(),
      attentionScore: Math.round(attentionData.attention_score * 100),
      avgEyeAR: attentionData.eye_ar,
      avgMouthAR: attentionData.mouth_ar,
      phoneDetected: attentionData.phone_detected
    };
    
    addSession(session);
    
    // Stop camera
    stopCamera();
    
    // Redirect to progress page
    router.push('/progress');
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  // Determine if user is distracted
  const isDistracted = attentionData.phone_detected || attentionData.focus_status === 'distracted';

  return (
    <main className="min-h-screen bg-[#fffbef] flex flex-col">
      {/* Focus Alert Popup */}
      <FocusAlert isDistracted={isDistracted} />
      
      {/* Header */}
      <div className="bg-white border-b border-[rgba(63,64,63,0.08)] px-6 py-4">
        <div className="max-w-6xl mx-auto flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-modular text-[#3f403f]">
              Focus Session
            </h1>
            <p className="text-sm font-norwester text-[#575b44]">
              {lastMethod ? lastMethod.replace('-', ' ').toUpperCase() : 'STUDY'} Method
            </p>
          </div>
          
          {isSessionActive && isClient && (
            <div className="text-right">
              <div className="text-3xl font-modular text-[#939f5c]">
                {formatTime(sessionDuration)}
              </div>
              <div className="text-sm font-norwester text-[#575b44]">
                Session Time
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Camera Section */}
      <div className="flex-1 flex flex-col items-center justify-center p-6">
        <div className="relative w-full max-w-4xl aspect-video bg-black rounded-2xl overflow-hidden shadow-lg">
          {isClient ? (
            <video
              ref={videoRef}
              autoPlay
              playsInline
              muted
              className="w-full h-full object-cover scale-x-[-1]"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center text-white">
              <div className="text-center">
                <div className="text-2xl mb-2">📹</div>
                <div className="text-sm">Loading Camera...</div>
              </div>
            </div>
          )}
          
          {/* Overlay for computer vision indicators */}
          <div className="absolute inset-0 pointer-events-none">
            {/* Connection status */}
            <div className={`absolute top-4 left-4 px-3 py-1 rounded-full text-sm font-norwester ${
              apiConnected ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
            }`}>
              {apiConnected ? '🔗 AI Connected' : '❌ AI Disconnected'}
            </div>
            
            {/* Computer vision tracking area */}
            <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
              {/* Outer focus ring */}
              <div className={`border-2 rounded-full opacity-50 ${
                attentionData.focus_status === 'focused' ? 'border-green-400' : 
                attentionData.focus_status === 'distracted' ? 'border-red-400' : 
                'border-yellow-400'
              }`} style={{
                width: '1260px',
                height: '700px',
                position: 'absolute',
                left: '50%',
                top: '50%',
                transform: 'translate(-50%, -50%)'
              }}></div>
              
              {/* Inner focus area */}
              <div className={`border border-white rounded-full opacity-30 ${
                attentionData.focus_status === 'focused' ? 'border-green-300' : 
                attentionData.focus_status === 'distracted' ? 'border-red-300' : 
                'border-yellow-300'
              }`} style={{
                width: '1252px',
                height: '692px',
                position: 'absolute',
                left: '50%',
                top: '50%',
                transform: 'translate(-50%, -50%)'
              }}></div>
            </div>
            
            {/* Real-time status indicators */}
            <div className="absolute top-4 right-4 space-y-2">
              <div className={`px-2 py-1 rounded text-xs font-norwester ${
                attentionData.focus_status === 'focused' ? 'bg-green-500 text-white' :
                attentionData.focus_status === 'distracted' ? 'bg-red-500 text-white' :
                'bg-yellow-500 text-white'
              }`}>
                {attentionData.focus_status === 'focused' ? '✅ Focused' :
                 attentionData.focus_status === 'distracted' ? '❌ Distracted' :
                 '⏳ Analyzing...'}
              </div>
              
              <div className="bg-blue-500 text-white px-2 py-1 rounded text-xs font-norwester">
                👁️ Eye AR: {attentionData.eye_ar.toFixed(2)}
              </div>
              
              <div className="bg-purple-500 text-white px-2 py-1 rounded text-xs font-norwester">
                🧠 Score: {Math.round(attentionData.attention_score * 100)}%
              </div>
              
              {attentionData.phone_detected && (
                <div className="bg-red-600 text-white px-2 py-1 rounded text-xs font-norwester">
                  📱 Phone Detected!
                </div>
              )}
              
              <div className="bg-gray-600 text-white px-2 py-1 rounded text-xs font-norwester">
                📊 FPS: {Math.round(attentionData.fps)}
              </div>
            </div>
          </div>
        </div>

        {/* Instructions */}
        <div className="mt-8 text-center max-w-2xl">
          <h2 className="text-xl font-modular text-[#3f403f] mb-4">
            {isSessionActive ? 'Stay Focused!' : 'Ready to Start?'}
          </h2>
          <p className="text-[#575b44] font-norwester mb-6">
            {isSessionActive 
              ? 'Keep your eyes on the screen and maintain good posture. AI is tracking your focus, eye movement, and detecting distractions like phones.'
              : apiConnected 
                ? 'Position yourself in front of the camera and click "Start Session" when you\'re ready to begin. AI will track your attention in real-time.'
                : 'AI attention tracking is not connected. Please start the Python server first.'
            }
          </p>
        </div>
      </div>

      {/* Bottom Action Bar */}
      <div className="bg-white border-t border-[rgba(63,64,63,0.08)] px-6 py-6">
        <div className="max-w-6xl mx-auto flex justify-center">
          {!isSessionActive ? (
            <Button
              onClick={startSession}
              disabled={!apiConnected}
              className={`font-modular px-8 py-4 text-lg rounded-2xl shadow-lg ${
                apiConnected 
                  ? 'bg-[#939f5c] text-[#3f403f] hover:bg-[#808b4f]' 
                  : 'bg-gray-400 text-gray-600 cursor-not-allowed'
              }`}
            >
              {apiConnected ? 'Start Session' : 'AI Not Connected'}
            </Button>
          ) : (
            <Button
              onClick={stopSession}
              className="font-modular bg-red-500 text-white hover:bg-red-600 px-8 py-4 text-lg rounded-2xl shadow-lg"
            >
              Stop Session
            </Button>
          )}
        </div>
      </div>
    </main>
  );
}
