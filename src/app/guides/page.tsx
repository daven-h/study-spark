export default function GuidesPage() {
  const guides = [
    {
      title: "Getting Started with Study Spark",
      description: "Learn the basics of using Study Spark effectively for your study sessions.",
      category: "Getting Started"
    },
    {
      title: "Choosing the Right Study Method",
      description: "A comprehensive guide to selecting the study technique that works best for you.",
      category: "Study Methods"
    },
    {
      title: "Building Consistent Study Habits",
      description: "Tips and strategies for maintaining a regular study routine and building momentum.",
      category: "Habits & Routine"
    },
    {
      title: "Maximizing Focus During Study Sessions",
      description: "Techniques to minimize distractions and maintain deep focus while studying.",
      category: "Focus & Concentration"
    },
    {
      title: "Understanding Your Study Patterns",
      description: "How to analyze your progress data to optimize your study approach.",
      category: "Progress Tracking"
    },
    {
      title: "Creating the Perfect Study Environment",
      description: "Setting up your physical and digital space for maximum productivity.",
      category: "Environment"
    }
  ];

  return (
    <main className="container mx-auto px-6 py-12">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-modular text-[#3f403f] mb-8 text-center">
          Tips & Guides
        </h1>
        
        <p className="text-xl font-norwester text-[#575b44] text-center mb-12">
          Expert advice and proven strategies for effective studying
        </p>

        <div className="grid md:grid-cols-2 gap-6">
          {guides.map((guide, index) => (
            <div key={index} className="bg-[#fffbef] border border-[rgba(63,64,63,0.08)] rounded-2xl p-6 hover:shadow-lg transition-shadow">
              <div className="mb-4">
                <span className="inline-block bg-[#939f5c] text-[#3f403f] px-3 py-1 rounded-full text-sm font-norwester font-bold">
                  {guide.category}
                </span>
              </div>
              <h2 className="text-xl font-norwester text-[#3f403f] mb-3">
                {guide.title}
              </h2>
              <p className="text-[#575b44] font-norwester leading-relaxed mb-4">
                {guide.description}
              </p>
              <button className="text-[#939f5c] font-norwester font-bold hover:text-[#808b4f] transition">
                Read More →
              </button>
            </div>
          ))}
        </div>

        <div className="mt-12 text-center">
          <div className="bg-[#fffbef] border border-[rgba(63,64,63,0.08)] rounded-2xl p-8">
            <h2 className="text-2xl font-modular text-[#3f403f] mb-4">
              Want More Tips?
            </h2>
            <p className="text-[#575b44] font-norwester mb-6">
              Subscribe to our newsletter for weekly study tips and productivity insights.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 max-w-md mx-auto">
              <input
                type="email"
                placeholder="Enter your email"
                className="flex-1 px-4 py-3 rounded-xl border border-[rgba(63,64,63,0.08)] focus:outline-none focus:ring-2 focus:ring-[#939f5c]/50"
              />
              <button className="rounded-xl bg-[#939f5c] text-[#3f403f] px-6 py-3 font-norwester font-bold hover:bg-[#808b4f] transition">
                Subscribe
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}