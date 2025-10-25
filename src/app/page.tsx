'use client';

import { useState } from 'react';
import Image from 'next/image';
import Link from 'next/link';

const studyMethods = [
  { label: 'Pomodoro', slug: 'pomodoro' },
  { label: 'Flowtime', slug: 'flowtime' },
  { label: '52 / 17', slug: '52-17' },
  { label: 'Deep Work (90 / 20)', slug: 'deep-work-90-20' },
  { label: 'Blurting Sprint', slug: 'blurting-sprint' },
  { label: 'Phone-Free Sprint', slug: 'phone-free-sprint' },
];

export default function Home() {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  const handleMethodSelect = (slug: string) => {
    setIsDropdownOpen(false);
    // Navigation will be handled by the Link component
  };

  return (
    <main className="grid grid-cols-1 md:grid-cols-2 items-center gap-10 px-6 pb-16 pt-6">
      {/* Left block */}
      <div className="space-y-6">
        <h2 className="font-norwester text-[#575b44] text-xl font-semibold">
          Digital Study Tracker
        </h2>
        
        <h1 className="font-modular text-6xl md:text-7xl font-extrabold text-[#3f403f] leading-tight">
          STUDY SPARK
        </h1>
        
        <p className="font-norwester text-[#939f5c] text-lg">
          Turn focus into a habit, one session at a time.
        </p>
        
        {/* STUDY MODE Button with Dropdown */}
        <div className="relative">
          <button
            onClick={() => setIsDropdownOpen(!isDropdownOpen)}
            className="rounded-2xl bg-[#939f5c] text-[#3f403f] px-6 py-3 text-2xl font-norwester tracking-wide shadow-sm hover:bg-[#808b4f] transition"
          >
            STUDY MODE
          </button>
          
          {isDropdownOpen && (
            <div className="absolute top-full left-0 mt-2 w-64 bg-white border border-gray-200 rounded-xl shadow-lg z-10">
              {studyMethods.map((method) => (
                <Link
                  key={method.slug}
                  href={`/methods/${method.slug}`}
                  onClick={() => handleMethodSelect(method.slug)}
                  className="block px-4 py-3 text-[#3f403f] hover:bg-gray-50 transition first:rounded-t-xl last:rounded-b-xl"
                >
                  {method.label}
                </Link>
              ))}
            </div>
          )}
        </div>
      </div>
      
      {/* Right block */}
      <div className="flex justify-center md:justify-end">
        <Image
          src="/brain-mascot.png"
          alt="Study Spark Brain Mascot"
          width={500}
          height={500}
          className="w-full max-w-lg h-auto rounded-3xl shadow-2xl"
          priority
        />
      </div>
    </main>
  );
}
