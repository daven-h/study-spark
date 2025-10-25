import Header from '@/components/layout/Header';
import Image from 'next/image';

export default function Home() {
  return (
    <>
      <Header />
      <main className="container mx-auto px-6 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          {/* Left side - Text content */}
          <div>
            <p className="text-sm text-gray-600 mb-2">Digital Study Tracker</p>
            <h1 className="text-6xl font-bold mb-4 font-modular">STUDY SPARK</h1>
            <p className="text-xl text-[#939f5c] mb-8">
              Turn focus into a habit, one session at a time.
            </p>
            <button className="rounded-2xl bg-[#939f5c] text-[#3f403f] px-8 py-4 text-xl font-bold tracking-wide shadow-sm hover:bg-[#808b4f] transition font-modular uppercase">
              STUDY MODE
            </button>
          </div>

          {/* Right side - Brain mascot image */}
          <div className="flex justify-center">
            {/* Add your brain mascot image here */}
            <div className="w-full max-w-md aspect-square bg-gray-100 rounded-lg flex items-center justify-center">
              <Image src='/brain-mascot.png' alt='Brain Mascot' width={500} height={500} priority />
            </div>
          </div>
        </div>
      </main>
    </>
  );
}