'use client'

/**
 * useAuth Hook
 * Client-side authentication state management
 * Handles session validation, user data, and auth operations
 * Author: Sharmeen Asif
 */

import { useState, useEffect, useCallback } from 'react'
import { useRouter } from 'next/navigation'
import type { User } from '@/types/auth'
import { getStoredToken, clearStoredToken } from '@/lib/api-client'

interface AuthState {
  user: User | null
  isLoading: boolean
  isAuthenticated: boolean
  error: string | null
}

interface UseAuthReturn extends AuthState {
  refreshUser: () => Promise<void>
  logout: () => Promise<void>
  checkAuth: () => Promise<boolean>
}

export function useAuth(): UseAuthReturn {
  const router = useRouter()
  const [state, setState] = useState<AuthState>({
    user: null,
    isLoading: true,
    isAuthenticated: false,
    error: null,
  })

  /**
   * Fetch current user from session
   */
  const fetchUser = useCallback(async (): Promise<User | null> => {
    try {
      const token = getStoredToken()
      if (!token) return null
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/me`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
      })

      if (!response.ok) {
        if (response.status === 401) {
          // Not authenticated
          return null
        }
        throw new Error('Failed to fetch user')
      }

      const userData = await response.json()
      return userData
    } catch (error) {
      console.error('Error fetching user:', error)
      return null
    }
  }, [])

  /**
   * Refresh user data
   */
  const refreshUser = useCallback(async () => {
    setState((prev) => ({ ...prev, isLoading: true, error: null }))

    try {
      const userData = await fetchUser()

      setState({
        user: userData,
        isLoading: false,
        isAuthenticated: !!userData,
        error: null,
      })
    } catch (error: any) {
      setState({
        user: null,
        isLoading: false,
        isAuthenticated: false,
        error: error.message || 'Failed to refresh user',
      })
    }
  }, [fetchUser])

  /**
   * Check authentication status
   * Returns true if user is authenticated
   */
  const checkAuth = useCallback(async (): Promise<boolean> => {
    const userData = await fetchUser()
    const isAuth = !!userData

    setState((prev) => ({
      ...prev,
      user: userData,
      isAuthenticated: isAuth,
      isLoading: false,
    }))

    return isAuth
  }, [fetchUser])

  /**
   * Logout user
   */
  const logout = useCallback(async () => {
    setState((prev) => ({ ...prev, isLoading: true }))

    try {
      const token = getStoredToken()
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/signout`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
      })

      if (!response.ok) {
        throw new Error('Failed to sign out')
      }

      // Clear token and local state
      clearStoredToken()
      setState({
        user: null,
        isLoading: false,
        isAuthenticated: false,
        error: null,
      })

      // Redirect to signin
      router.push('/auth/signin?message=Signed out successfully')
    } catch (error: any) {
      setState((prev) => ({
        ...prev,
        isLoading: false,
        error: error.message || 'Failed to sign out',
      }))
    }
  }, [router])

  /**
   * Initialize auth state on mount
   */
  useEffect(() => {
    refreshUser()
  }, [refreshUser])

  return {
    user: state.user,
    isLoading: state.isLoading,
    isAuthenticated: state.isAuthenticated,
    error: state.error,
    refreshUser,
    logout,
    checkAuth,
  }
}

/**
 * Hook for protecting routes - redirects to signin if not authenticated
 */
export function useRequireAuth(): UseAuthReturn {
  const router = useRouter()
  const auth = useAuth()

  useEffect(() => {
    if (!auth.isLoading && !auth.isAuthenticated) {
      // Store return URL for redirect after signin
      const returnUrl = encodeURIComponent(window.location.pathname + window.location.search)
      router.push(`/auth/signin?returnUrl=${returnUrl}`)
    }
  }, [auth.isLoading, auth.isAuthenticated, router])

  return auth
}

/**
 * Hook for guest-only routes - redirects to dashboard if authenticated
 */
export function useGuestOnly(redirectTo: string = '/tasks'): UseAuthReturn {
  const router = useRouter()
  const auth = useAuth()

  useEffect(() => {
    if (!auth.isLoading && auth.isAuthenticated) {
      router.push(redirectTo)
    }
  }, [auth.isLoading, auth.isAuthenticated, router, redirectTo])

  return auth
}
