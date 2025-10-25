'use client';

import Link from 'next/link';

export default function Header() {
  return (
    <header className="w-full px-6 py-4">
      <div className="flex justify-end space-x-4">
        <Link
          href="/register"
          className="rounded-2xl bg-[#939f5c] text-[#3f403f] px-5 py-2 text-xl font-bold tracking-wide shadow-sm hover:bg-[#808b4f] transition font-modular uppercase"
        >
          REGISTER
        </Link>
        <Link
          href="/login"
          className="rounded-2xl bg-[#939f5c] text-[#3f403f] px-5 py-2 text-xl font-bold tracking-wide shadow-sm hover:bg-[#808b4f] transition font-modular uppercase"
        >
          LOGIN
        </Link>
      </div>
    </header>
  );
}
