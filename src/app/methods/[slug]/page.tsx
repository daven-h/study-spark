import Link from 'next/link';
import Image from 'next/image';
import StarBorderButton from '@/components/StarBorderButton';

const methodTitles: { [key: string]: string } = {
  "pomodoro": "Pomodoro (25/5)",
  "52-17": "52 / 17",
  "deep-work-90-20": "Deep Work (90 / 20)",
  "phone-free-sprint": "Phone-Free Sprint"
};

const methodDetails: { [key: string]: any } = {
  "pomodoro": {
    title: "Pomodoro (25/5)",
    description: "25 minutes focused work, 5 minutes break. After 4 rounds, take a 15–30 min break.",
    benefits: "Great for beating procrastination and building momentum.",
    icon: "🍅",
    color: "#e74c3c",
    image: "/pomodoro-method.png",
    steps: [
      "Set a timer for 25 minutes",
      "Work on your task with complete focus",
      "Take a 5-minute break when timer rings",
      "Repeat for 4 rounds",
      "Take a longer 15-30 minute break"
    ],
    tips: [
      "Choose tasks that can be completed in 25-minute chunks",
      "Use breaks to stretch, hydrate, or take a quick walk",
      "Track your completed pomodoros for motivation",
      "Eliminate distractions during work periods"
    ]
  },
  "52-17": {
    title: "52 / 17",
    description: "52 minutes focused work, 17 minutes break.",
    benefits: "Great for deep work with planned recovery.",
    icon: "⏰",
    color: "#3498db",
    image: "/52-17-method.png",
    steps: [
      "Work intensely for 52 minutes",
      "Take a 17-minute break",
      "Repeat the cycle",
      "Aim for 2–3 cycles per session"
    ],
    tips: [
      "Use the longer work period for complex tasks",
      "Break time is perfect for a short walk or snack",
      "Monitor your focus levels to optimize timing",
      "Plan your recovery activities during breaks"
    ]
  },
  "deep-work-90-20": {
    title: "Deep Work (90 / 20)",
    description: "One 90-minute block of uninterrupted focus.",
    benefits: "Great for big, cognitively heavy tasks.",
    icon: "🧠",
    color: "#9b59b6",
    image: "/deep-work-method.png",
    steps: [
      "Prepare your workspace for deep focus",
      "Work for 90 minutes without interruption",
      "Take a 20-minute restorative break",
      "Follow with a full 20-minute reset away from screens"
    ],
    tips: [
      "Choose your most challenging tasks for this method",
      "Eliminate all distractions beforehand",
      "Use break time for light physical activity",
      "Avoid screens during the 20-minute reset"
    ]
  },
  "phone-free-sprint": {
    title: "Phone-Free Sprint",
    description: "25–40 minute focus with phone face-down/out of frame.",
    benefits: "Great for eliminating the #1 distraction.",
    icon: "📱",
    color: "#27ae60",
    image: "/phone-free-method.png",
    steps: [
      "Put your phone face-down or out of frame",
      "Set a timer for 25-40 minutes",
      "Work without any digital distractions",
      "Break only after a clean streak"
    ],
    tips: [
      "Start with shorter periods and build up",
      "Use a physical timer instead of your phone",
      "Tell others you're in a focus session",
      "Keep your phone completely out of sight"
    ]
  }
};

interface MethodPageProps {
  params: Promise<{
    slug: string;
  }>;
}

export default async function MethodPage({ params }: MethodPageProps) {
  const { slug } = await params;
  const method = methodDetails[slug];
  
  if (!method) {
    return (
      <main className="px-6 py-8">
        <div className="max-w-4xl mx-auto">
          <h1 className="font-modular text-5xl font-extrabold text-[#3f403f] mb-6">
            Method Not Found
          </h1>
          <Link
            href="/methods"
            className="inline-block rounded-2xl bg-[#939f5c] text-[#3f403f] px-6 py-2 text-lg font-norwester tracking-wide shadow-sm hover:bg-[#808b4f] transition"
          >
            ← Back to Methods
          </Link>
        </div>
      </main>
    );
  }

  return (
    <main className="px-6 py-8 bg-[#fffbef] min-h-screen">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <Link
            href="/methods"
            className="inline-flex items-center gap-2 text-[#575b44] hover:text-[#3f403f] transition font-norwester mb-4"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Back to Study Methods
          </Link>
          
          <div className="flex items-center gap-4 mb-6">
            <div className="text-6xl">{method.icon}</div>
            <div>
              <h1 className="font-modular text-5xl font-extrabold text-[#3f403f] mb-2">
                {method.title}
              </h1>
              <p className="text-xl font-norwester text-[#575b44]">
                {method.description}
              </p>
            </div>
          </div>
          
          <div className="bg-[#939f5c]/10 border border-[#939f5c]/20 rounded-2xl p-6">
            <p className="text-lg font-norwester text-[#3f403f] italic">
              "{method.benefits}"
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column - Steps */}
          <div className="space-y-6">
            <div className="bg-white rounded-2xl p-6 shadow-sm border border-[rgba(63,64,63,0.08)]">
              <h2 className="text-2xl font-modular text-[#3f403f] mb-4 flex items-center gap-2">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
                How to Use
              </h2>
              <ol className="space-y-3">
                {method.steps.map((step: string, index: number) => (
                  <li key={index} className="flex items-start gap-3">
                    <div className="w-6 h-6 bg-[#939f5c] text-white rounded-full flex items-center justify-center text-sm font-bold font-modular flex-shrink-0 mt-0.5">
                      {index + 1}
                    </div>
                    <span className="text-[#575b44] font-norwester">{step}</span>
                  </li>
                ))}
              </ol>
            </div>

            <div className="bg-white rounded-2xl p-6 shadow-sm border border-[rgba(63,64,63,0.08)]">
              <h2 className="text-2xl font-modular text-[#3f403f] mb-4 flex items-center gap-2">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
                Pro Tips
              </h2>
              <ul className="space-y-3">
                {method.tips.map((tip: string, index: number) => (
                  <li key={index} className="flex items-start gap-3">
                    <div className="w-2 h-2 bg-[#939f5c] rounded-full flex-shrink-0 mt-2"></div>
                    <span className="text-[#575b44] font-norwester">{tip}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Right Column - Image and Start Button */}
          <div className="space-y-6">
            <div className="bg-white rounded-2xl p-6 shadow-sm border border-[rgba(63,64,63,0.08)]">
              <div className="aspect-square bg-gray-100 rounded-xl overflow-hidden mb-6">
                <Image 
                  src={method.image}
                  alt={`${method.title} Study Method`}
                  width={400}
                  height={400}
                  className="w-full h-full object-cover"
                />
              </div>
              
              <div className="text-center">
                <h3 className="text-xl font-modular text-[#3f403f] mb-4">
                  Ready to Focus?
                </h3>
                <p className="text-[#575b44] font-norwester mb-6">
                  Start your {method.title.toLowerCase()} session and build your study momentum.
                </p>
                
                <StarBorderButton 
                  href="/focus" 
                  ariaLabel={`Start ${method.title} session`}
                  className="w-full justify-center"
                >
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.828 14.828a4 4 0 01-5.656 0M9 10h1m4 0h1m-6 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Start Session
                </StarBorderButton>
              </div>
            </div>

            {/* Quick Stats */}
            <div className="bg-gradient-to-br from-[#939f5c]/10 to-[#939f5c]/5 rounded-2xl p-6 border border-[#939f5c]/20">
              <h3 className="text-lg font-modular text-[#3f403f] mb-4">
                Method Stats
              </h3>
              <div className="grid grid-cols-2 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-modular text-[#939f5c] mb-1">
                    {slug === 'pomodoro' ? '25' : slug === '52-17' ? '52' : slug === 'deep-work-90-20' ? '90' : '30'}
                  </div>
                  <div className="text-sm font-norwester text-[#575b44]">Work Minutes</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-modular text-[#939f5c] mb-1">
                    {slug === 'pomodoro' ? '5' : slug === '52-17' ? '17' : slug === 'deep-work-90-20' ? '20' : '10'}
                  </div>
                  <div className="text-sm font-norwester text-[#575b44]">Break Minutes</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
