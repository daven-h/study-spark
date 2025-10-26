import React from 'react';

interface ProgressBarProps {
  progress: number; // 0-100
  className?: string;
  showPercentage?: boolean;
}

export function ProgressBar({ 
  progress, 
  className = "", 
  showPercentage = false 
}: ProgressBarProps) {
  const clampedProgress = Math.min(100, Math.max(0, progress));
  
  return (
    <div className={`w-full ${className}`}>
      <div className="flex justify-between items-center mb-2">
        <span className="text-sm font-norwester text-[#3f403f]">
          Progress
        </span>
        {showPercentage && (
          <span className="text-sm font-norwester text-[#575b44]">
            {Math.round(clampedProgress)}%
          </span>
        )}
      </div>
      <div className="w-full bg-[rgba(63,64,63,0.08)] rounded-full h-2">
        <div 
          className="bg-[#939f5c] h-2 rounded-full transition-all duration-300 ease-out"
          style={{ width: `${clampedProgress}%` }}
        />
      </div>
    </div>
  );
}
