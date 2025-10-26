'use client';

import { useState } from 'react';
import { LoginModal } from '@/components/auth/LoginModal';
import { useAuthStore } from '@/store/authStore';
import { signOut } from '@/lib/supabase/auth';

export default function Header() {
  const [showLoginModal, setShowLoginModal] = useState(false);

  // pull everything we need from Zustand
  const { user, loading, setUser } = useAuthStore();

  const handleSignOut = async () => {
    try {
      await signOut();
      // immediately clear local state so UI updates right away
      setUser(null);
    } catch (error) {
      console.error('Sign out error:', error);
    }
  };

  // helper for avatar letter (handles null/undefined)
  const avatarLetter = (user?.email ?? '?')[0]?.toUpperCase() ?? '?';

  return (
    <>
      <header className="w-full px-6 py-4">
        <div className="flex justify-end items-center space-x-4">
          {loading ? (
            // while AuthProvider is still hydrating from supabase.auth.getSession()
            <div className="text-xs text-gray-500 animate-pulse select-none">
              Loading...
            </div>
          ) : user ? (
            <>
              <div className="flex items-center gap-2 bg-gray-100 px-4 py-2 rounded-xl max-w-[220px]">
                <div className="w-8 h-8 bg-[#939f5c] rounded-full flex items-center justify-center text-white font-bold">
                  {avatarLetter}
                </div>

                <div className="flex flex-col leading-tight">
                  <span className="text-[10px] uppercase tracking-wide text-gray-400 font-semibold">
                    Signed in
                  </span>
                  <span className="text-sm font-medium text-gray-700 truncate max-w-[150px]">
                    {user.email}
                  </span>
                </div>
              </div>

              <button
                onClick={handleSignOut}
                className="rounded-2xl bg-[#939f5c] text-[#3f403f] px-5 py-2 text-xl font-bold tracking-wide shadow-sm hover:bg-[#808b4f] transition font-modular uppercase"
              >
                SIGN OUT
              </button>
            </>
          ) : (
            <button
              onClick={() => setShowLoginModal(true)}
              className="rounded-2xl bg-[#939f5c] text-[#3f403f] px-5 py-2 text-xl font-bold tracking-wide shadow-sm hover:bg-[#808b4f] transition font-modular uppercase"
            >
              LOGIN
            </button>
          )}
        </div>
      </header>

      {/* Login Modal */}
      <LoginModal open={showLoginModal} onOpenChange={setShowLoginModal} />
    </>
  );
}
