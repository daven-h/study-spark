import Link from 'next/link';

const methodTitles: { [key: string]: string } = {
  "pomodoro": "Pomodoro",
  "flowtime": "Flowtime",
  "52-17": "52 / 17",
  "deep-work-90-20": "Deep Work (90 / 20)",
  "blurting-sprint": "Blurting Sprint",
  "phone-free-sprint": "Phone-Free Sprint"
};

interface MethodPageProps {
  params: Promise<{
    slug: string;
  }>;
}

export default async function MethodPage({ params }: MethodPageProps) {
  const { slug } = await params;
  const title = methodTitles[slug] || "Study Method";

  return (
    <main className="px-6 py-8">
      <div className="max-w-4xl mx-auto">
        <Link
          href="/"
          className="inline-block rounded-2xl bg-[#939f5c] text-[#3f403f] px-6 py-2 text-lg font-norwester tracking-wide shadow-sm hover:bg-[#808b4f] transition mb-8"
        >
          ← Back to Home
        </Link>
        
        <h1 className="font-modular text-5xl font-extrabold text-[#3f403f] mb-6">
          {title}
        </h1>
        
        <div className="bg-white rounded-2xl p-8 shadow-sm">
          <p className="text-[#3f403f] text-lg">
            This is the {title} study method page. Study session functionality will be implemented here.
          </p>
        </div>
      </div>
    </main>
  );
}
