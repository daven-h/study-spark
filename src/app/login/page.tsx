'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAppStore } from '@/store/app-store';

export default function LoginPage() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { signInGoogle } = useAppStore();
  const router = useRouter();

  const handleGoogleSignIn = async () => {
    try {
      setLoading(true);
      setError(null);
      await signInGoogle();
      router.push('/progress');
    } catch (err) {
      setError('Failed to sign in. Please try again.');
      console.error('Sign in error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="container mx-auto px-6 py-12">
      <div className="max-w-md mx-auto">
        <div className="bg-[#fffbef] border border-[rgba(63,64,63,0.08)] rounded-2xl p-8">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-modular text-[#3f403f] mb-2">
              Welcome back
            </h1>
            <p className="text-[#575b44] font-norwester">
              Sign in to track your study progress
            </p>
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 rounded-xl p-4 mb-6">
              <p className="text-red-600 font-norwester text-sm">{error}</p>
            </div>
          )}

          <button
            onClick={handleGoogleSignIn}
            disabled={loading}
            className="w-full rounded-2xl bg-[#939f5c] text-[#3f403f] px-6 py-4 text-lg font-bold tracking-wide shadow-sm hover:bg-[#808b4f] transition font-modular uppercase disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Signing in...' : 'Continue with Google'}
          </button>

          <div className="mt-6 text-center">
            <p className="text-sm font-norwester text-[#575b44]">
              We'll save your sessions to the cloud when available. Works offline too.
            </p>
          </div>
        </div>
      </div>
    </main>
  );
}