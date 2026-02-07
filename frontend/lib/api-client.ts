/**
 * API Client
 * Handles all HTTP requests to the backend API
 * Author: Sharmeen Asif
 */

import {
  ApiError,
  ApiErrorDetail,
  SignupData,
  SigninData,
  UserResponse,
  SigninResponse,
  TaskResponse,
  TaskListResponse,
  TaskCreateData,
  TaskUpdateData,
} from './api-types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Token management - store/retrieve JWT from localStorage
 */
export function getStoredToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('access_token');
}

export function setStoredToken(token: string): void {
  if (typeof window === 'undefined') return;
  localStorage.setItem('access_token', token);
}

export function clearStoredToken(): void {
  if (typeof window === 'undefined') return;
  localStorage.removeItem('access_token');
}

/**
 * Get auth headers with Bearer token
 */
function getAuthHeaders(): Record<string, string> {
  const token = getStoredToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

/**
 * Generic API response wrapper for type-safe error handling
 */
export interface ApiResponse<T> {
  /** Response data (null if error) */
  data: T | null;
  /** Error information (null if success) */
  error: ApiErrorDetail | null;
  /** HTTP status code */
  status: number;
  /** Whether request was successful */
  ok: boolean;
}

/**
 * HTTP request options with authentication
 */
interface RequestOptions extends RequestInit {
  /** Include authentication credentials (cookies) */
  includeCredentials?: boolean;
}

/**
 * Generic API request utility
 *
 * @param endpoint - API endpoint (e.g., '/api/auth/login')
 * @param options - Request options (method, body, headers, etc.)
 * @returns Promise with typed response or error
 */
export async function apiRequest<T>(
  endpoint: string,
  options: RequestOptions = {}
): Promise<ApiResponse<T>> {
  const {
    includeCredentials = true,
    headers = {},
    ...fetchOptions
  } = options;

  try {
    const url = `${API_URL}${endpoint}`;

    const defaultHeaders: HeadersInit = {
      'Content-Type': 'application/json',
      ...getAuthHeaders(),
    };

    const mergedHeaders = {
      ...defaultHeaders,
      ...(headers as Record<string, string>),
    };

    const response = await fetch(url, {
      ...fetchOptions,
      headers: mergedHeaders,
    });

    let data: T | null = null;
    let error: ApiErrorDetail | null = null;

    if (response.ok) {
      try {
        data = await response.json();
      } catch {
        data = null as T;
      }
    } else {
      try {
        error = await response.json();
      } catch {
        error = {
          message: response.statusText || 'An error occurred',
          status_code: response.status,
          errors: null,
          timestamp: new Date().toISOString(),
        };
      }
    }

    return {
      data,
      error,
      status: response.status,
      ok: response.ok,
    };

  } catch (err) {
    return {
      data: null,
      error: {
        message: err instanceof Error ? err.message : 'Network error',
        status_code: 0,
        errors: null,
        timestamp: new Date().toISOString(),
      },
      status: 0,
      ok: false,
    };
  }
}

/**
 * Generic GET request
 */
export async function apiGet<T>(
  endpoint: string,
  options?: RequestOptions
): Promise<ApiResponse<T>> {
  return apiRequest<T>(endpoint, { ...options, method: 'GET' });
}

/**
 * Generic POST request
 */
export async function apiPost<T>(
  endpoint: string,
  body?: any,
  options?: RequestOptions
): Promise<ApiResponse<T>> {
  return apiRequest<T>(endpoint, {
    ...options,
    method: 'POST',
    body: body ? JSON.stringify(body) : undefined,
  });
}

/**
 * Generic PATCH request
 */
export async function apiPatch<T>(
  endpoint: string,
  body?: any,
  options?: RequestOptions
): Promise<ApiResponse<T>> {
  return apiRequest<T>(endpoint, {
    ...options,
    method: 'PATCH',
    body: body ? JSON.stringify(body) : undefined,
  });
}

/**
 * Generic DELETE request
 */
export async function apiDelete<T>(
  endpoint: string,
  options?: RequestOptions
): Promise<ApiResponse<T>> {
  return apiRequest<T>(endpoint, { ...options, method: 'DELETE' });
}

/**
 * Throw an error if API response is not ok
 */
export function throwIfError<T>(
  response: ApiResponse<T>
): asserts response is ApiResponse<T> & { ok: true; data: T } {
  if (!response.ok) {
    throw new ApiError(
      response.error?.message || 'API request failed',
      response.status,
      response.error?.errors || null
    );
  }
}

/**
 * Re-export types for convenience
 */
export type {
  SignupData,
  SigninData,
  UserResponse,
  SigninResponse,
  TaskResponse,
  TaskListResponse,
  TaskCreateData,
  TaskUpdateData,
  ApiErrorDetail,
  PaginationParams,
  PaginatedResponse,
} from './api-types';

/**
 * Authentication API
 */

/**
 * Signup new user
 */
export async function signup(data: SignupData): Promise<UserResponse> {
  const response = await fetch(`${API_URL}/api/auth/signup`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error: ApiErrorDetail = await response.json();
    throw new ApiError(error.message || 'Signup failed', response.status, error.errors);
  }

  return response.json();
}

/**
 * Signin existing user
 */
export async function signin(data: SigninData): Promise<SigninResponse> {
  const response = await fetch(`${API_URL}/api/auth/signin`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error: ApiErrorDetail = await response.json();
    throw new ApiError(error.message || 'Signin failed', response.status, error.errors);
  }

  const result: SigninResponse = await response.json();
  // Store the access token in localStorage for cross-origin auth
  setStoredToken(result.access_token);
  return result;
}

/**
 * Signout current user
 */
export async function signout(): Promise<void> {
  const response = await fetch(`${API_URL}/api/auth/signout`, {
    method: 'POST',
    headers: {
      ...getAuthHeaders(),
    },
  });

  // Clear token regardless of response
  clearStoredToken();

  if (!response.ok) {
    const error: ApiErrorDetail = await response.json().catch(() => ({
      message: 'Signout failed',
      status_code: response.status,
      errors: null,
      timestamp: new Date().toISOString(),
    }));
    throw new ApiError(error.message, response.status, error.errors);
  }
}

/**
 * Get current user profile
 */
export async function getCurrentUser(): Promise<UserResponse> {
  const response = await fetch(`${API_URL}/api/auth/me`, {
    method: 'GET',
    headers: {
      ...getAuthHeaders(),
    },
  });

  if (!response.ok) {
    throw new ApiError('Not authenticated', response.status);
  }

  return response.json();
}

/**
 * Task API
 */

/**
 * Get all tasks for the current user
 */
export async function getTasks(
  completed?: boolean,
  limit: number = 100,
  offset: number = 0
): Promise<TaskListResponse> {
  const params = new URLSearchParams();
  if (completed !== undefined) {
    params.append('completed', String(completed));
  }
  params.append('limit', String(limit));
  params.append('offset', String(offset));

  const response = await fetch(`${API_URL}/api/tasks?${params}`, {
    method: 'GET',
    headers: { ...getAuthHeaders() },
  });

  if (!response.ok) {
    const error: ApiErrorDetail = await response.json();
    throw new ApiError(error.message || 'Failed to fetch tasks', response.status, error.errors);
  }

  return response.json();
}

/**
 * Get a specific task by ID
 */
export async function getTask(taskId: string): Promise<TaskResponse> {
  const response = await fetch(`${API_URL}/api/tasks/${taskId}`, {
    method: 'GET',
    headers: { ...getAuthHeaders() },
  });

  if (!response.ok) {
    const error: ApiErrorDetail = await response.json();
    throw new ApiError(error.message || 'Task not found', response.status, error.errors);
  }

  return response.json();
}

/**
 * Create a new task
 */
export async function createTask(data: TaskCreateData): Promise<TaskResponse> {
  const response = await fetch(`${API_URL}/api/tasks`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders(),
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error: ApiErrorDetail = await response.json();
    throw new ApiError(error.message || 'Failed to create task', response.status, error.errors);
  }

  return response.json();
}

/**
 * Update an existing task
 */
export async function updateTask(
  taskId: string,
  data: TaskUpdateData
): Promise<TaskResponse> {
  const response = await fetch(`${API_URL}/api/tasks/${taskId}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders(),
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error: ApiErrorDetail = await response.json();
    throw new ApiError(error.message || 'Failed to update task', response.status, error.errors);
  }

  return response.json();
}

/**
 * Delete a task
 */
export async function deleteTask(taskId: string): Promise<void> {
  const response = await fetch(`${API_URL}/api/tasks/${taskId}`, {
    method: 'DELETE',
    headers: { ...getAuthHeaders() },
  });

  if (!response.ok) {
    const error: ApiErrorDetail = await response.json();
    throw new ApiError(error.message || 'Failed to delete task', response.status, error.errors);
  }
}
