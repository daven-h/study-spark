import { redirect } from 'next/navigation';

export default function RegisterPage() {
  // Redirect to login page for now
  redirect('/login');
}