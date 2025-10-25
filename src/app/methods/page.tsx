import Link from 'next/link';
import { MethodSlug } from '@/types';

interface Method {
  slug: MethodSlug;
  title: string;
  description: string;
  icon: string;
}

const methods: Method[] = [
  {
    slug: 'pomodoro',
    title: 'Pomodoro',
    description: '25 min focus, 5 min break. Longer break every 4 rounds.',
    icon: '🍅'
  },
  {
    slug: 'flowtime',
    title: 'Flowtime',
    description: 'Work until energy dips, then rest. No fixed timer.',
    icon: '🌊'
  },
  {
    slug: '52-17',
    title: '52 / 17',
    description: '52 min work, 17 min break.',
    icon: '⏰'
  },
  {
    slug: 'deep-work-90-20',
    title: 'Deep Work (90 / 20)',
    description: '90 min deep focus, 20 min rest.',
    icon: '🧠'
  },
  {
    slug: 'blurting-sprint',
    title: 'Blurting Sprint',
    description: 'Short recall bursts, then review.',
    icon: '⚡'
  },
  {
    slug: 'phone-free-sprint',
    title: 'Phone-Free Sprint',
    description: 'Lock your phone away and sprint.',
    icon: '📱'
  }
];

export default function MethodsPage() {
  return (
    <main className="container mx-auto px-6 py-12">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 id="methods" className="text-5xl font-modular text-[#3f403f] mb-4">
            Study Methods
          </h1>
          <p className="text-xl font-norwester text-[#575b44]">
            Choose the study technique that works best for you
          </p>
        </div>

        {/* Methods Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {methods.map((method) => (
            <div
              key={method.slug}
              className="bg-[#fffbef] border border-[rgba(63,64,63,0.08)] rounded-2xl p-6 hover:shadow-lg transition-shadow"
            >
              <div className="text-center">
                <div className="text-4xl mb-4">{method.icon}</div>
                <h3 className="text-2xl font-modular text-[#3f403f] mb-3">
                  {method.title}
                </h3>
                <p className="text-[#575b44] font-norwester mb-6 leading-relaxed">
                  {method.description}
                </p>
                <Link
                  href={`/methods/${method.slug}`}
                  className="inline-block rounded-2xl bg-[#939f5c] text-[#3f403f] px-6 py-3 text-lg font-bold tracking-wide shadow-sm hover:bg-[#808b4f] transition font-modular uppercase"
                >
                  Start
                </Link>
              </div>
            </div>
          ))}
        </div>

        {/* Call to Action */}
        <div className="text-center mt-12">
          <p className="text-[#575b44] font-norwester mb-6">
            Not sure which method to try? Start with Pomodoro for a proven approach to focused work.
          </p>
          <Link
            href="/methods/pomodoro"
            className="inline-block rounded-2xl bg-[#939f5c] text-[#3f403f] px-8 py-4 text-xl font-bold tracking-wide shadow-sm hover:bg-[#808b4f] transition font-modular uppercase"
          >
            Try Pomodoro First
          </Link>
        </div>
      </div>
    </main>
  );
}
