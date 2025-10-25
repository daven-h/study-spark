import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import Header from '@/components/Header';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Study Spark',
  description: 'Digital Study Tracker',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} min-h-dvh bg-[#fffbef] text-[#3f403f] antialiased`}>
        <div className="max-w-7xl mx-auto">
          <Header />
          {children}
        </div>
      </body>
    </html>
  );
}
