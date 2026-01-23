export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-6 sm:p-24">
      <div className="text-center">
        <h1 className="text-4xl sm:text-6xl font-bold mb-4">
          Phase 2 Todo App
        </h1>
        <p className="text-lg sm:text-xl text-gray-600 dark:text-gray-400 mb-8">
          Full-stack todo application with JWT authentication
        </p>

        <div className="space-y-4">
          <p className="text-green-600 dark:text-green-400 font-semibold">
            ✅ Frontend setup complete!
          </p>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Next: Phase 5 - Authentication pages (Login, Register)
          </p>
        </div>

        <div className="mt-12 space-y-3">
          <p className="text-sm font-mono bg-gray-100 dark:bg-gray-800 p-3 rounded">
            API Base URL: {process.env.NEXT_PUBLIC_API_BASE_URL}
          </p>
          <p className="text-xs text-gray-500">
            Backend running on http://localhost:8000
          </p>
        </div>
      </div>
    </main>
  );
}
