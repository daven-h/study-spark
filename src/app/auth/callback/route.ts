import { createClient } from '@/lib/supabase/server';
import { NextResponse } from 'next/server';

export async function GET(request: Request) {
  const requestUrl = new URL(request.url);
  const code = requestUrl.searchParams.get('code');
  const error = requestUrl.searchParams.get('error');
  const error_description = requestUrl.searchParams.get('error_description');

  console.log('[OAuth Callback] Started processing callback');
  console.log('[OAuth Callback] Code present:', !!code);
  console.log('[OAuth Callback] Error:', error);

  // Handle OAuth errors from Google
  if (error) {
    console.error('[OAuth Callback] OAuth error:', error, error_description);
    return NextResponse.redirect(new URL('/?error=oauth_failed', requestUrl.origin));
  }

  if (code) {
    try {
      const supabase = await createClient();
      console.log('[OAuth Callback] Exchanging code for session...');

      const { data, error } = await supabase.auth.exchangeCodeForSession(code);

      if (error) {
        console.error('[OAuth Callback] Error exchanging code:', error.message);
        return NextResponse.redirect(new URL('/?error=auth_failed', requestUrl.origin));
      }

      console.log('[OAuth Callback] Successfully exchanged code for session');
      console.log('[OAuth Callback] User:', data.user?.email);
    } catch (err) {
      console.error('[OAuth Callback] Exception during code exchange:', err);
      return NextResponse.redirect(new URL('/?error=server_error', requestUrl.origin));
    }
  } else {
    console.error('[OAuth Callback] No code parameter in callback URL');
    return NextResponse.redirect(new URL('/?error=no_code', requestUrl.origin));
  }

  // Redirect to homepage after successful auth
  console.log('[OAuth Callback] Redirecting to homepage');
  return NextResponse.redirect(new URL('/', requestUrl.origin));
}
