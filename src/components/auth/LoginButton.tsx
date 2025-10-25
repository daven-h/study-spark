'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { LoginModal } from './LoginModal';

export function LoginButton() {
  const [showModal, setShowModal] = useState(false);

  return (
    <>
      <Button onClick={() => setShowModal(true)} variant="outline">
        Sign In
      </Button>
      <LoginModal open={showModal} onOpenChange={setShowModal} />
    </>
  );
}