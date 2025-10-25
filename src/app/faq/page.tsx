export default function FAQPage() {
  const faqs = [
    {
      question: "What study methods are available?",
      answer: "Study Spark offers 6 proven study techniques: Pomodoro (25/5), Flowtime (work until energy dips), 52/17 (52 min work, 17 min break), Deep Work (90/20), Blurting Sprint (recall bursts), and Phone-Free Sprint (distraction-free sessions)."
    },
    {
      question: "Do I need an account to use Study Spark?",
      answer: "No account required! Study Spark works completely offline and stores your data locally. You can optionally sign in to sync your progress across devices when cloud features are available."
    },
    {
      question: "Is my study data private?",
      answer: "Absolutely. Your study sessions and progress are stored locally on your device. We don't collect, track, or share your personal study data. Your privacy is our priority."
    },
    {
      question: "Can I use Study Spark offline?",
      answer: "Yes! Study Spark is designed to work completely offline. All core features including timers, progress tracking, and statistics work without an internet connection."
    },
    {
      question: "How do I choose the right study method?",
      answer: "Start with Pomodoro if you're new to structured study techniques. If you prefer flexible timing, try Flowtime. For deep work sessions, use Deep Work (90/20). Experiment with different methods to find what works best for you."
    },
    {
      question: "Can I track my progress over time?",
      answer: "Yes! Study Spark tracks your total study time, session count, current streak, and daily goals. You can view detailed statistics and progress charts in the Progress page."
    },
    {
      question: "Is Study Spark free?",
      answer: "Yes, Study Spark is completely free to use. We believe in making effective study tools accessible to all students."
    },
    {
      question: "Can I use Study Spark on mobile devices?",
      answer: "Yes! Study Spark is fully responsive and works great on phones, tablets, and desktop computers. The interface adapts to your screen size for the best experience."
    }
  ];

  return (
    <main className="container mx-auto px-6 py-12">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-modular text-[#3f403f] mb-8 text-center">
          Frequently Asked Questions
        </h1>
        
        <div className="space-y-6">
          {faqs.map((faq, index) => (
            <div key={index} className="bg-[#fffbef] border border-[rgba(63,64,63,0.08)] rounded-2xl p-6">
              <h2 className="text-xl font-norwester text-[#3f403f] mb-3">
                {faq.question}
              </h2>
              <p className="text-[#575b44] font-norwester leading-relaxed">
                {faq.answer}
              </p>
            </div>
          ))}
        </div>

        <div className="mt-12 text-center">
          <p className="text-[#575b44] font-norwester mb-6">
            Still have questions? We're here to help!
          </p>
          <a
            href="mailto:support@studyspark.app"
            className="inline-block rounded-2xl bg-[#939f5c] text-[#3f403f] px-6 py-3 text-lg font-bold tracking-wide shadow-sm hover:bg-[#808b4f] transition font-modular uppercase"
          >
            Contact Support
          </a>
        </div>
      </div>
    </main>
  );
}