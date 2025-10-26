export default function BlogPage() {
  const posts = [
    {
      title: "The Science Behind Effective Study Techniques",
      excerpt: "Research-backed insights into why certain study methods work better than others.",
      date: "December 15, 2024",
      category: "Research"
    },
    {
      title: "How to Build a Sustainable Study Routine",
      excerpt: "Practical tips for creating study habits that stick and don't lead to burnout.",
      date: "December 10, 2024",
      category: "Habits"
    },
    {
      title: "The Pomodoro Technique: A Deep Dive",
      excerpt: "Everything you need to know about the Pomodoro method and how to master it.",
      date: "December 5, 2024",
      category: "Study Methods"
    },
    {
      title: "Digital Minimalism for Students",
      excerpt: "How reducing digital distractions can dramatically improve your study focus.",
      date: "November 28, 2024",
      category: "Focus"
    },
    {
      title: "Success Stories: Students Who Transformed Their Study Habits",
      excerpt: "Real stories from students who improved their grades and reduced stress using Study Spark.",
      date: "November 20, 2024",
      category: "Success Stories"
    },
    {
      title: "The Psychology of Procrastination and How to Overcome It",
      excerpt: "Understanding why we procrastinate and evidence-based strategies to break the cycle.",
      date: "November 15, 2024",
      category: "Psychology"
    }
  ];

  return (
    <main className="min-h-screen bg-gradient-to-br from-[#faf9f5] via-[#fffbef] to-[#f8f7f3]">
      <div className="container mx-auto px-6 py-24">
        <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-modular text-[#3f403f] mb-8 text-center">
          Study Spark Blog
        </h1>
        
        <p className="text-xl font-norwester text-[#575b44] text-center mb-12">
          Latest insights, updates, and success stories from our community
        </p>

        <div className="space-y-8">
          {posts.map((post, index) => (
            <article key={index} className="bg-[#fffbef] border border-[rgba(63,64,63,0.08)] rounded-2xl p-8 hover:shadow-lg transition-shadow">
              <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-4">
                <span className="inline-block bg-[#939f5c] text-[#3f403f] px-3 py-1 rounded-full text-sm font-norwester font-bold mb-2 md:mb-0">
                  {post.category}
                </span>
                <time className="text-[#575b44] font-norwester text-sm">
                  {post.date}
                </time>
              </div>
              
              <h2 className="text-2xl font-norwester text-[#3f403f] mb-4">
                {post.title}
              </h2>
              
              <p className="text-[#575b44] font-norwester leading-relaxed mb-6">
                {post.excerpt}
              </p>
              
              <button className="text-[#939f5c] font-norwester font-bold hover:text-[#808b4f] transition">
                Read Full Article →
              </button>
            </article>
          ))}
        </div>
        </div>
      </div>
    </main>
  );
}