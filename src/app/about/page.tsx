export default function AboutPage() {
  return (
    <main className="container mx-auto px-6 py-12">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-modular text-[#3f403f] mb-8 text-center">
          About Study Spark
        </h1>
        
        <div className="space-y-8">
          <section id="mission" className="bg-[#fffbef] border border-[rgba(63,64,63,0.08)] rounded-2xl p-8">
            <h2 className="text-2xl font-modular text-[#3f403f] mb-4">Our Mission</h2>
            <p className="text-[#575b44] font-norwester leading-relaxed">
              Study Spark is designed to help students build better study habits through proven techniques 
              and progress tracking. We believe that focused, intentional study sessions lead to better 
              learning outcomes and reduced stress.
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
                    Select from 6 proven study techniques that match your learning style and schedule.
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
                    Begin a focused study session with built-in timers and distraction-free environment.
                  </p>
                </div>
              </div>
              
              <div className="flex items-start space-x-4">
                <div className="w-8 h-8 bg-[#939f5c] rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                  <span className="text-[#3f403f] font-bold text-sm">3</span>
                </div>
                <div>
                  <h3 className="font-norwester text-[#3f403f] mb-2">Track Progress</h3>
                  <p className="text-[#575b44] font-norwester">
                    Monitor your study streaks, total time, and build momentum with detailed analytics.
                  </p>
                </div>
              </div>
            </div>
          </section>

          <section className="bg-[#fffbef] border border-[rgba(63,64,63,0.08)] rounded-2xl p-8">
            <h2 className="text-2xl font-modular text-[#3f403f] mb-4">Why Study Spark?</h2>
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <h3 className="font-norwester text-[#3f403f] mb-2">Privacy First</h3>
                <p className="text-[#575b44] font-norwester text-sm">
                  Your study data stays on your device. No tracking, no ads, no distractions.
                </p>
              </div>
              <div>
                <h3 className="font-norwester text-[#3f403f] mb-2">Works Offline</h3>
                <p className="text-[#575b44] font-norwester text-sm">
                  Study anywhere, anytime. No internet connection required for core features.
                </p>
              </div>
              <div>
                <h3 className="font-norwester text-[#3f403f] mb-2">Proven Methods</h3>
                <p className="text-[#575b44] font-norwester text-sm">
                  Based on research-backed study techniques used by top performers.
                </p>
              </div>
              <div>
                <h3 className="font-norwester text-[#3f403f] mb-2">Simple & Clean</h3>
                <p className="text-[#575b44] font-norwester text-sm">
                  Focus on what matters: studying. No complex features or overwhelming interfaces.
                </p>
              </div>
            </div>
          </section>
        </div>
      </div>
    </main>
  );
}