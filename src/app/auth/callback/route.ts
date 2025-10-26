import { createClient } from '@/lib/supabase/server';
import { NextResponse } from 'next/server';

export async function GET(request: Request) {
  const requestUrl = new URL(request.url);
  const code = requestUrl.searchParams.get('code');

  if (code) {
    const supabase = await createClient();

    // Complete the OAuth flow by exchanging the code for a session
    const { error } = await supabase.auth.exchangeCodeForSession(code);

    if (error) {
      console.error('Error exchanging OAuth code for session:', error.message);
      // You can choose to redirect somewhere else or add a query param here if you want
    }
  }

  // Redirect to progress page after auth attempt
  return NextResponse.redirect(new URL('/progress', requestUrl.origin));
}
