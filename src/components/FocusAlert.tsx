'use client';

import { useState, useEffect, useRef } from 'react';

interface FocusAlertProps {
  isDistracted: boolean;
}

// Helper function to play a quick alert sound
function playAlertSound() {
  try {
    const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();

    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);

    oscillator.frequency.value = 800; // Higher pitch for alert
    oscillator.type = 'sine';
    
    gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.2);

    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + 0.2);
  } catch (error) {
    console.log('Could not play sound:', error);
  }
}

export default function FocusAlert({ isDistracted }: FocusAlertProps) {
  const [show, setShow] = useState(false);
  const [visible, setVisible] = useState(false);
  const prevDistractedRef = useRef(false);
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    // Detect when isDistracted changes from false to true (new distraction event)
    if (isDistracted && !prevDistractedRef.current) {
      // Show the alert immediately
      setShow(true);
      setVisible(true);
      
      // Play alert sound
      playAlertSound();
      
      // Clear any existing timeout
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
      
      // After 3 seconds, start fading out
      timeoutRef.current = setTimeout(() => {
        setVisible(false);
      }, 3000);
    }
    
    // When distraction ends, reset the component state
    if (!isDistracted && prevDistractedRef.current) {
      setShow(false);
      setVisible(false);
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
        timeoutRef.current = null;
      }
    }
    
    // Update previous value
    prevDistractedRef.current = isDistracted;
    
    // Clean up
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, [isDistracted]);

  // Remove from DOM after fade animation completes
  useEffect(() => {
    if (!visible && show) {
      const removeTimer = setTimeout(() => {
        setShow(false);
      }, 300); // Wait for fade animation to complete
      
      return () => clearTimeout(removeTimer);
    }
  }, [visible, show]);

  if (!show) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center pointer-events-none">
      <div 
        className={`text-8xl md:text-9xl font-bold text-red-500 transition-opacity duration-300 ${
          visible ? 'opacity-100' : 'opacity-0'
        }`}
        style={{
          textShadow: '0 0 20px rgba(239, 68, 68, 0.5), 0 0 40px rgba(239, 68, 68, 0.3), 0 0 60px rgba(239, 68, 68, 0.2)',
          animation: visible ? 'pulse 1s ease-in-out infinite' : 'none'
        }}
      >
        FOCUS
      </div>
      <style jsx>{`
        @keyframes pulse {
          0%, 100% {
            transform: scale(1);
          }
          50% {
            transform: scale(1.05);
          }
        }
      `}</style>
    </div>
  );
}
