import Link from 'next/link';

export default function LoginPage() {
  return (
    <main className="px-6 py-8">
      <div className="max-w-2xl mx-auto text-center">
        <h1 className="font-modular text-5xl font-extrabold text-[#3f403f] mb-6">
          LOGIN
        </h1>
        
        <p className="text-[#3f403f] text-lg mb-8">
          Authentication functionality will be implemented here.
        </p>
        
        <Link
          href="/"
          className="inline-block rounded-2xl bg-[#939f5c] text-[#3f403f] px-6 py-2 text-lg font-norwester tracking-wide shadow-sm hover:bg-[#808b4f] transition"
        >
          Back to Home
        </Link>
      </div>
    </main>
  );
}
