import Image from 'next/image';
import StarBorderButton from '@/components/StarBorderButton';
import GradientText from '@/components/GradientText';

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-[#faf9f5] via-[#fffbef] to-[#f8f7f3]">
      <div className="container mx-auto px-6 py-24">
      {/* Hero Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center mb-24 min-h-[600px]">
        {/* Left side - Text content */}
        <div className="flex flex-col justify-center">
          <p className="text-base font-norwester text-[#575b44] mb-4">Digital Study Tracker</p>
          <h1 className="text-8xl font-bold mb-6 font-modular">
            <GradientText 
              colors={['#3f403f', '#939f5c', '#575b44', '#939f5c', '#3f403f']}
              animationSpeed={3}
            >
              STUDY SPARK
            </GradientText>
          </h1>
          <p className="text-2xl font-norwester text-[#939f5c] mb-10">
            Turn focus into a habit, one session at a time.
          </p>
          <div className="flex flex-col sm:flex-row gap-4">
            <StarBorderButton href="/methods" ariaLabel="Choose a method">
              Choose a Method
            </StarBorderButton>

            <StarBorderButton href="/progress" ariaLabel="Track your progress" className="ml-1" size="md" variant="secondary">
              Track Your Progress
            </StarBorderButton>
          </div>
        </div>

        {/* Right side - Brain mascot image */}
        <div className="flex justify-center items-center">
          <div className="w-full max-w-md aspect-square bg-gray-100 rounded-lg flex items-center justify-center ml-4">
            <Image src='/brain-mascot.png' alt='Brain Mascot' width={500} height={500} priority />
          </div>
        </div>
      </div>

      {/* Why Study Spark Section */}
      <div id="methods" className="mb-16">
        <h2 className="text-4xl font-modular text-[#3f403f] text-center mb-12">
          Why Study Spark?
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Stay Focused Card */}
          <div className="bg-[#fffbef] border border-[rgba(63,64,63,0.08)] rounded-2xl p-8 text-center">
            <div className="w-16 h-16 bg-[#939f5c] rounded-full flex items-center justify-center mx-auto mb-6">
              <svg className="w-8 h-8 text-[#3f403f]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="text-xl font-norwester text-[#3f403f] mb-4">Stay Focused</h3>
            <p className="text-[#575b44] font-norwester">
              Timers that fit your style. Choose from 4 proven study methods designed to maximize your concentration.
            </p>
          </div>

          {/* See Progress Card */}
          <div className="bg-[#fffbef] border border-[rgba(63,64,63,0.08)] rounded-2xl p-8 text-center">
            <div className="w-16 h-16 bg-[#939f5c] rounded-full flex items-center justify-center mx-auto mb-6">
              <svg className="w-8 h-8 text-[#3f403f]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <h3 className="text-xl font-norwester text-[#3f403f] mb-4">See Progress</h3>
            <p className="text-[#575b44] font-norwester">
              Track your study streaks, total time, and build momentum with detailed progress analytics.
            </p>
          </div>

          {/* On Any Device Card */}
          <div className="bg-[#fffbef] border border-[rgba(63,64,63,0.08)] rounded-2xl p-8 text-center">
            <div className="w-16 h-16 bg-[#939f5c] rounded-full flex items-center justify-center mx-auto mb-6">
              <svg className="w-8 h-8 text-[#3f403f]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
              </svg>
            </div>
            <h3 className="text-xl font-norwester text-[#3f403f] mb-4">On Any Device</h3>
            <p className="text-[#575b44] font-norwester">
              Lightweight and private. Study anywhere with our responsive web app.
            </p>
          </div>
        </div>
      </div>
    </div>
    </main>
  );
}