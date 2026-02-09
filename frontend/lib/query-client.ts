/**
 * TanStack Query Client Configuration
 *
 * Centralized configuration for React Query (TanStack Query).
 * Handles caching, retry logic, and default query/mutation options.
 *
 * Author: Sharmeen Asif
 */

import { QueryClient, DefaultOptions } from '@tanstack/react-query';

/**
 * Default options for all queries and mutations
 */
const queryConfig: DefaultOptions = {
  queries: {
    /**
     * Stale time: How long data is considered fresh (5 minutes)
     * Fresh data won't refetch on window focus/reconnect
     */
    staleTime: 1000 * 60 * 5,

    /**
     * Cache time: How long inactive data stays in cache (10 minutes)
     * After this, garbage collection removes it
     */
    gcTime: 1000 * 60 * 10,

    /**
     * Retry failed queries 1 time
     * Prevents excessive retries on permanent errors (401, 404, etc.)
     */
    retry: 1,

    /**
     * Retry delay: exponential backoff (1s, 2s, 4s...)
     */
    retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),

    /**
     * Refetch on window focus: disabled by default
     * Enable per-query if needed (e.g., real-time data)
     */
    refetchOnWindowFocus: false,

    /**
     * Refetch on reconnect: enabled
     * Ensures fresh data after network recovery
     */
    refetchOnReconnect: true,

    /**
     * Refetch on mount: only if data is stale
     */
    refetchOnMount: true,
  },

  mutations: {
    /**
     * Retry failed mutations 0 times
     * Mutations should not auto-retry (user action required)
     */
    retry: 0,

    /**
     * Network mode: online only
     * Mutations won't execute if offline
     */
    networkMode: 'online',
  },
};

/**
 * Create Query Client instance
 *
 * Use this function to create a new query client with default config.
 * Useful for server-side rendering where you need per-request clients.
 *
 * @example
 * ```typescript
 * const queryClient = createQueryClient();
 * ```
 */
export function createQueryClient(): QueryClient {
  return new QueryClient({
    defaultOptions: queryConfig,
  });
}

/**
 * Global Query Client instance (for client-side only)
 *
 * Do not use this on the server (Next.js RSC/SSR).
 * Create a new client per request instead.
 */
export const queryClient = createQueryClient();

/**
 * Query keys for consistent cache management
 *
 * Organize query keys by resource type.
 * Use factories to generate type-safe query keys.
 */
export const queryKeys = {
  /**
   * Authentication query keys
   */
  auth: {
    /** Current user profile */
    me: ['auth', 'me'] as const,
    /** User by ID */
    user: (id: string) => ['auth', 'user', id] as const,
  },

  /**
   * Task query keys
   */
  tasks: {
    /** All tasks list */
    all: ['tasks'] as const,
    /** Tasks list with filters */
    list: (filters?: { completed?: boolean; limit?: number; offset?: number }) =>
      ['tasks', 'list', filters] as const,
    /** Single task by ID */
    detail: (id: string) => ['tasks', 'detail', id] as const,
  },

  /**
   * Organization query keys
   */
  organizations: {
    /** All organizations for current user */
    all: ['organizations'] as const,
    /** Organization by ID */
    detail: (id: string) => ['organizations', 'detail', id] as const,
    /** Organization members */
    members: (id: string) => ['organizations', id, 'members'] as const,
  },

  /**
   * Project query keys
   */
  projects: {
    /** All projects in an organization */
    all: (orgId: string) => ['organizations', orgId, 'projects'] as const,
    /** Project by ID */
    detail: (orgId: string, projectId: string) =>
      ['organizations', orgId, 'projects', projectId] as const,
    /** Project tasks */
    tasks: (orgId: string, projectId: string) =>
      ['organizations', orgId, 'projects', projectId, 'tasks'] as const,
  },
} as const;

/**
 * Helper to invalidate related queries after a mutation
 *
 * @example
 * ```typescript
 * // After creating a task, invalidate tasks list
 * await invalidateQueries(queryClient, queryKeys.tasks.all);
 * ```
 */
export async function invalidateQueries(
  client: QueryClient,
  queryKey: readonly unknown[]
): Promise<void> {
  await client.invalidateQueries({ queryKey });
}

/**
 * Helper to prefetch a query
 *
 * Useful for preloading data before navigation.
 *
 * @example
 * ```typescript
 * // Prefetch user profile before rendering protected page
 * await prefetchQuery(queryClient, queryKeys.auth.me, getCurrentUser);
 * ```
 */
export async function prefetchQuery<T>(
  client: QueryClient,
  queryKey: readonly unknown[],
  queryFn: () => Promise<T>
): Promise<void> {
  await client.prefetchQuery({
    queryKey,
    queryFn,
  });
}
