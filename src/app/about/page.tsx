export default function AboutPage() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-[#faf9f5] via-[#fffbef] to-[#f8f7f3]">
      <div className="container mx-auto px-6 py-24">
        <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-modular text-[#3f403f] mb-8 text-center">
          About Study Spark
        </h1>
        
        <div className="space-y-8">
          <section id="mission" className="bg-[#fffbef] border border-[rgba(63,64,63,0.08)] rounded-2xl p-8">
            <h2 className="text-2xl font-modular text-[#3f403f] mb-4">Our Mission</h2>
            <p className="text-[#575b44] font-norwester leading-relaxed">
              Study Spark is designed to hold you accountable and help you stay focused during study sessions. 
              By using real-time attention tracking and alerts when you're distracted, we help you build 
              consistent study habits. Track your progress and stay motivated to reach your goals.
            </p>
          </section>

          <section id="how-it-works" className="bg-[#fffbef] border border-[rgba(63,64,63,0.08)] rounded-2xl p-8">
            <h2 className="text-2xl font-modular text-[#3f403f] mb-4">How It Works</h2>
            <div className="space-y-4">
              <div className="flex items-start space-x-4">
                <div className="w-8 h-8 bg-[#939f5c] rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                  <span className="text-[#3f403f] font-bold text-sm">1</span>
                </div>
                <div>
                  <h3 className="font-norwester text-[#3f403f] mb-2">Choose Your Method</h3>
                  <p className="text-[#575b44] font-norwester">
                    Select from 4 proven study techniques that match your learning style and schedule.
                  </p>
                </div>
              </div>
              
              <div className="flex items-start space-x-4">
                <div className="w-8 h-8 bg-[#939f5c] rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                  <span className="text-[#3f403f] font-bold text-sm">2</span>
                </div>
                <div>
                  <h3 className="font-norwester text-[#3f403f] mb-2">Start Your Session</h3>
                  <p className="text-[#575b44] font-norwester">
                    Begin a focused study session with real-time attention tracking and alerts when you're distracted.
                  </p>
                </div>
              </div>
              
              <div className="flex items-start space-x-4">
                <div className="w-8 h-8 bg-[#939f5c] rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                  <span className="text-[#3f403f] font-bold text-sm">3</span>
                </div>
                <div>
                  <h3 className="font-norwester text-[#3f403f] mb-2">Stay Accountable</h3>
                  <p className="text-[#575b44] font-norwester">
                    Get instant alerts when you're distracted. Track your progress to stay motivated and reach your goals.
                  </p>
                </div>
              </div>
            </div>
          </section>

          <section className="bg-[#fffbef] border border-[rgba(63,64,63,0.08)] rounded-2xl p-8">
            <h2 className="text-2xl font-modular text-[#3f403f] mb-4">Why Study Spark?</h2>
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <h3 className="font-norwester text-[#3f403f] mb-2">Real-Time Accountability</h3>
                <p className="text-[#575b44] font-norwester text-sm">
                  Get instant alerts when you're distracted. Stay on track and build better study habits.
                </p>
              </div>
              <div>
                <h3 className="font-norwester text-[#3f403f] mb-2">Privacy First</h3>
                <p className="text-[#575b44] font-norwester text-sm">
                  Your study data stays on your device. No tracking, no ads, no distractions.
                </p>
              </div>
              <div>
                <h3 className="font-norwester text-[#3f403f] mb-2">Proven Methods</h3>
                <p className="text-[#575b44] font-norwester text-sm">
                  Based on research-backed study techniques used by top performers.
                </p>
              </div>
              <div>
                <h3 className="font-norwester text-[#3f403f] mb-2">Track Your Progress</h3>
                <p className="text-[#575b44] font-norwester text-sm">
                  Monitor your study time and streaks to stay motivated and reach your goals.
                </p>
              </div>
            </div>
          </section>
        </div>
        </div>
      </div>
    </main>
  );
}