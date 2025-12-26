/**
 * Tasks Dashboard Page
 * Protected route - requires authentication
 * Author: Sharmeen Asif
 */

import { cookies } from 'next/headers'
import { redirect } from 'next/navigation'
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
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-lg shadow p-6">
          <TaskList />
        </div>
      </main>
    </div>
  )
}
