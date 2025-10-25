'use client';

import { useState } from 'react';
import { LoginModal } from '@/components/auth/LoginModal';

export default function Header() {
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [showRegisterModal, setShowRegisterModal] = useState(false);

  return (
    <>
      <header className="w-full px-6 py-4">
        <div className="flex justify-end space-x-4">
         
          <button
            onClick={() => setShowLoginModal(true)}
            className="rounded-2xl bg-[#939f5c] text-[#3f403f] px-5 py-2 text-xl font-bold tracking-wide shadow-sm hover:bg-[#808b4f] transition font-modular uppercase"
          >
            LOGIN
          </button>
        </div>
      </header>

      {/* Login Modal */}
      <LoginModal open={showLoginModal} onOpenChange={setShowLoginModal} />
      
      {/* Register Modal - TODO: Create RegisterModal component */}
      <LoginModal open={showRegisterModal} onOpenChange={setShowRegisterModal} />
    </>
  );
}