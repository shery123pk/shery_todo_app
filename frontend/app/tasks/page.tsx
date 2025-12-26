/**
 * Tasks Dashboard Page
 * Protected route - requires authentication
 * Author: Sharmeen Asif
 */

import { cookies } from 'next/headers'
import { redirect } from 'next/navigation'
import Link from 'next/link'
import TaskList from '@/components/tasks/TaskList'

async function getCurrentUser() {
  const cookieStore = await cookies()
  const sessionToken = cookieStore.get('session_token')

  if (!sessionToken) {
    return null
  }

  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

  try {
    const response = await fetch(`${API_URL}/api/auth/me`, {
      headers: {
        Cookie: `session_token=${sessionToken.value}`,
      },
      cache: 'no-store', // Always fetch fresh user data
    })

    if (!response.ok) {
      return null
    }

    return response.json()
  } catch (error) {
    console.error('Failed to fetch user:', error)
    return null
  }
}

async function handleSignout() {
  'use server'

  const cookieStore = await cookies()
  const sessionToken = cookieStore.get('session_token')

  if (sessionToken) {
    const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

    try {
      await fetch(`${API_URL}/api/auth/signout`, {
        method: 'POST',
        headers: {
          Cookie: `session_token=${sessionToken.value}`,
        },
      })
    } catch (error) {
      console.error('Signout error:', error)
    }
  }

  redirect('/auth/signin')
}

export default async function TasksPage() {
  const user = await getCurrentUser()

  if (!user) {
    redirect('/auth/signin')
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">My Tasks</h1>
              <p className="text-sm text-gray-600">
                Welcome back, {user.name || user.email}!
              </p>
            </div>
            <div className="flex items-center gap-3">
              {/* CLI Button */}
              <Link
                href="/cli"
                className="px-4 py-2 text-sm bg-black text-green-400 rounded-md hover:bg-gray-800 flex items-center gap-2 font-mono"
                title="Phase I: CLI Interface"
              >
                <span>$</span>
                <span>CLI</span>
              </Link>

              {/* Chatbot Button */}
              <Link
                href="/chatbot"
                className="px-4 py-2 text-sm bg-indigo-600 text-white rounded-md hover:bg-indigo-700 flex items-center gap-2"
                title="Phase III: AI Chatbot"
              >
                <span>🤖</span>
                <span>AI Chat</span>
              </Link>

              {/* Sign Out */}
              <form action={handleSignout}>
                <button
                  type="submit"
                  className="px-4 py-2 text-sm bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300"
                >
                  Sign Out
                </button>
              </form>
            </div>
          </div>
        </div>
      </header>

      {/* Phase Integration Banner */}
      <div className="bg-gradient-to-r from-purple-600 to-indigo-600 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3">
          <div className="flex items-center justify-between text-sm">
            <div className="flex items-center gap-6">
              <span className="font-semibold">All 5 Phases Available:</span>
              <Link href="/tasks" className="hover:underline opacity-80">
                Phase II: Web GUI (Current)
              </Link>
              <Link href="/cli" className="hover:underline opacity-80">
                Phase I: CLI
              </Link>
              <Link href="/chatbot" className="hover:underline opacity-80">
                Phase III: AI Chat
              </Link>
            </div>
            <span className="text-xs opacity-75">Panaversity Hackathon</span>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-lg shadow p-6">
          <TaskList />
        </div>
      </main>
    </div>
  )
}
