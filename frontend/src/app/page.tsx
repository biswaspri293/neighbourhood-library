"use client";

export default function Home() {
  return (
    <div className="flex min-h-screen bg-black text-white">
      <main className="flex flex-col justify-center px-20 py-32 max-w-4xl">

        <h1 className="text-4xl font-bold mb-6">
          Neighbourhood Library System
        </h1>

        <p className="text-lg text-zinc-400 mb-6 max-w-xl">
          A lightweight system for managing books, members, and borrowing
          operations for a small neighborhood library.
        </p>

        <p className="text-sm text-zinc-500 mb-8">
          To begin managing records, navigate to <span className="font-semibold text-white">Books</span> from the top menu.
        </p>

        <div className="flex gap-4">
          <a
            href="/books"
            className="px-6 py-3 rounded-full bg-white text-black font-medium hover:bg-zinc-300 transition"
          >
            Go to Books
          </a>

          <a
            href="/members"
            className="px-6 py-3 rounded-full border border-zinc-600 hover:bg-zinc-900 transition"
          >
            View Members
          </a>
        </div>

      </main>
    </div>
  );
}