export default function FAQPage() {
  const faqs = [
    {
      question: "What study methods are available?",
      answer: "Study Spark offers 4 proven study techniques: Pomodoro (25/5), 52/17 (52 min work, 17 min break), Deep Work (90/20), and Phone-Free Sprint (distraction-free sessions with real-time attention tracking)."
    },
    {
      question: "Do I need an account to use Study Spark?",
      answer: "No account required! You can optionally sign in to sync your progress across devices when cloud features are available."
    },
    {
      question: "Is my study data private?",
      answer: "Absolutely. Your study sessions and progress are stored locally on your device. We don't collect, track, or share your personal study data. Your privacy is our priority."
    },
    {
      question: "How do I choose the right study method?",
      answer: "Start with Pomodoro if you're new to structured study techniques. For longer sessions, try 52/17 or Deep Work (90/20). For distraction-free focus sessions with real-time accountability, use Phone-Free Sprint."
    },
    {
      question: "Can I track my progress over time?",
      answer: "Yes! Study Spark tracks your total study time, session count, current streak, and daily goals. You can view detailed statistics and progress charts in the Progress page."
    },
    {
      question: "Is Study Spark free?",
      answer: "Yes, Study Spark is completely free to use. We believe in making effective study tools accessible to all students."
    }
  ];

  return (
    <main className="min-h-screen bg-gradient-to-br from-[#faf9f5] via-[#fffbef] to-[#f8f7f3]">
      <div className="container mx-auto px-6 py-24">
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
        </div>
      </div>
    </main>
  );
}