import React from 'react';

interface StatsCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  className?: string;
}

export function StatsCard({ title, value, subtitle, className = "" }: StatsCardProps) {
  return (
    <div className={`bg-[#fffbef] border border-[rgba(63,64,63,0.08)] rounded-2xl p-6 ${className}`}>
      <div className="text-sm font-norwester text-[#575b44] mb-2">
        {title}
      </div>
      <div className="text-3xl font-modular text-[#939f5c] mb-1">
        {value}
      </div>
      {subtitle && (
        <div className="text-sm font-norwester text-[#575b44]">
          {subtitle}
        </div>
      )}
    </div>
  );
}
