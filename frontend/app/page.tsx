import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-600 to-purple-700 flex items-center justify-center px-4">
      <div className="text-center">
        <h1 className="text-5xl font-bold text-white mb-4">
          Interactive Study Tool 
        </h1>
        <p className="text-xl text-blue-100 mb-8">
          Learn smarter with AI-powered study assistance
        </p>
        <Link 
          href="/chat"
          className="inline-block bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-blue-50 transition-colors shadow-lg"
        >
          Start Learning →
        </Link>
      </div>
    </main>
  );
}
