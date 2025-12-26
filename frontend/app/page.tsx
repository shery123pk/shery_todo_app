import Link from 'next/link'

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center p-24">
      <main className="text-center">
        <h1 className="text-4xl font-bold mb-6">Todo App - Phase 2</h1>
        <p className="text-xl text-gray-600 mb-8">
          Full-stack web application with authentication
        </p>
        <div className="flex gap-4 justify-center">
          <Link
            href="/auth/signup"
            className="px-6 py-3 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90"
          >
            Sign Up
          </Link>
          <Link
            href="/auth/signin"
            className="px-6 py-3 bg-secondary text-secondary-foreground rounded-lg hover:bg-secondary/90"
          >
            Sign In
          </Link>
        </div>
      </main>
    </div>
  )
}
