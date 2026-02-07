/**
 * Authentication Context
 *
 * Provides auth state and methods throughout the app.
 * Uses React Context API for state management.
 *
 * Author: Sharmeen Asif
 */

'use client';

import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { UserResponse } from '@/lib/api-types';
import { getCurrentUser, clearStoredToken, getStoredToken } from '@/lib/api-client';

/**
 * Authentication context state
 */
interface AuthContextType {
  /** Currently authenticated user (null if not logged in) */
  user: UserResponse | null;
  /** Whether auth state is being loaded */
  loading: boolean;
  /** Whether user is authenticated */
  isAuthenticated: boolean;
  /** Update the user state after login/signup */
  setUser: (user: UserResponse | null) => void;
  /** Refresh user data from API */
  refreshUser: () => Promise<void>;
  /** Clear user state (for logout) */
  clearUser: () => void;
  /** Logout user and clear session */
  logout: () => Promise<void>;
}

/**
 * Create the auth context
 */
const AuthContext = createContext<AuthContextType | undefined>(undefined);

/**
 * Auth Provider Props
 */
interface AuthProviderProps {
  children: React.ReactNode;
}

/**
 * Authentication Provider Component
 *
 * Wraps the app to provide authentication state.
 * Automatically fetches user on mount if cookie exists.
 *
 * @example
 * ```tsx
 * <AuthProvider>
 *   <App />
 * </AuthProvider>
 * ```
 */
export function AuthProvider({ children }: AuthProviderProps) {
  const router = useRouter();
  const [user, setUser] = useState<UserResponse | null>(null);
  const [loading, setLoading] = useState(true);

  /**
   * Fetch current user from API
   */
  const refreshUser = useCallback(async () => {
    try {
      setLoading(true);
      // Only try to fetch user if we have a stored token
      const token = getStoredToken();
      if (!token) {
        setUser(null);
        return;
      }
      const userData = await getCurrentUser();
      setUser(userData);
    } catch (error) {
      // User not authenticated or session expired
      setUser(null);
      clearStoredToken();
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * Clear user state (used during logout)
   */
  const clearUser = useCallback(() => {
    setUser(null);
  }, []);

  /**
   * Logout user - calls backend signout and clears state
   */
  const logout = useCallback(async () => {
    try {
      const { signout } = await import('@/lib/api-client');
      await signout();
    } catch (error) {
      console.error('Logout error:', error);
    }
    // Always clear state and redirect
    clearStoredToken();
    setUser(null);
    router.push('/auth/signin?message=Signed out successfully');
  }, [router]);

  /**
   * Fetch user on component mount
   */
  useEffect(() => {
    refreshUser();
  }, [refreshUser]);

  const value: AuthContextType = {
    user,
    loading,
    isAuthenticated: user !== null,
    setUser,
    refreshUser,
    clearUser,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

/**
 * Hook to access auth context
 *
 * @throws {Error} If used outside AuthProvider
 *
 * @example
 * ```tsx
 * function MyComponent() {
 *   const { user, isAuthenticated, loading } = useAuth();
 *
 *   if (loading) return <div>Loading...</div>;
 *   if (!isAuthenticated) return <div>Please log in</div>;
 *
 *   return <div>Hello, {user.name}!</div>;
 * }
 * ```
 */
export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);

  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }

  return context;
}

/**
 * Hook to require authentication
 *
 * Returns full auth context for protected components.
 * Use this when you want to enforce authentication.
 *
 * @example
 * ```tsx
 * function ProtectedComponent() {
 *   const { user, loading } = useRequireAuth();
 *
 *   if (loading) {
 *     return <div>Loading...</div>;
 *   }
 *
 *   if (!user) {
 *     // Show loading or redirect
 *     return <div>Please log in...</div>;
 *   }
 *
 *   // User is guaranteed to be authenticated here
 *   return <div>Welcome, {user.full_name}!</div>;
 * }
 * ```
 */
export function useRequireAuth(): AuthContextType {
  return useAuth();
}

/**
 * Hook for optional authentication
 *
 * Returns user if authenticated, null otherwise.
 * Use this when authentication is optional.
 *
 * @example
 * ```tsx
 * function OptionalAuthComponent() {
 *   const user = useOptionalAuth();
 *
 *   return (
 *     <div>
 *       {user ? `Hello, ${user.name}!` : 'Hello, guest!'}
 *     </div>
 *   );
 * }
 * ```
 */
export function useOptionalAuth(): UserResponse | null {
  const { user } = useAuth();
  return user;
}
