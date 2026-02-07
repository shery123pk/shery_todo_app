/**
 * API Type Definitions
 *
 * TypeScript types for API requests and responses.
 * Author: Sharmeen Asif
 */

/**
 * Standard API error response structure
 */
export interface ApiErrorDetail {
  /** Human-readable error message */
  message: string;
  /** HTTP status code */
  status_code: number;
  /** Field-level validation errors (if applicable) */
  errors: Record<string, string> | null;
  /** ISO timestamp of when error occurred */
  timestamp: string;
}

/**
 * Custom API error class
 */
export class ApiError extends Error {
  /** HTTP status code */
  status: number;
  /** Field-level errors */
  errors: Record<string, string> | null;

  constructor(
    message: string,
    status: number = 500,
    errors: Record<string, string> | null = null
  ) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.errors = errors;
  }
}

/**
 * Pagination parameters for list endpoints
 */
export interface PaginationParams {
  /** Number of items to return */
  limit?: number;
  /** Number of items to skip */
  offset?: number;
}

/**
 * Generic paginated response
 */
export interface PaginatedResponse<T> {
  /** Array of items */
  items: T[];
  /** Total count of items (all pages) */
  total: number;
  /** Current limit */
  limit: number;
  /** Current offset */
  offset: number;
  /** Whether there are more pages */
  has_more: boolean;
}

/**
 * Authentication types
 */

export interface SignupData {
  email: string;
  password: string;
  full_name: string;
}

export interface SigninData {
  email: string;
  password: string;
  remember_me?: boolean;
}

export interface UserResponse {
  id: string;
  email: string;
  email_verified: boolean;
  name: string | null;
  full_name: string;
  created_at: string;
  updated_at: string;
}

export interface SigninResponse {
  user: UserResponse;
  access_token: string;
  message: string;
}

/**
 * Task types
 */

export interface TaskResponse {
  id: string;
  user_id: string;
  title: string;
  description: string | null;
  completed: boolean;
  priority: string | null;
  tags: string[];
  category: string | null;
  created_at: string;
  updated_at: string;
}

export interface TaskListResponse {
  tasks: TaskResponse[];
  total: number;
  completed: number;
  incomplete: number;
}

export interface TaskCreateData {
  title: string;
  description?: string;
  priority?: string;
  tags?: string[];
  category?: string;
}

export interface TaskUpdateData {
  title?: string;
  description?: string;
  completed?: boolean;
  priority?: string;
  tags?: string[];
  category?: string;
}

/**
 * Organization types (for future use)
 */

export interface OrganizationResponse {
  id: string;
  name: string;
  slug: string;
  owner_id: string;
  created_at: string;
  updated_at: string;
}

export interface OrganizationCreateData {
  name: string;
  slug?: string;
}

/**
 * Project types (for future use)
 */

export interface ProjectResponse {
  id: string;
  organization_id: string;
  name: string;
  description: string | null;
  status: 'active' | 'archived' | 'completed';
  created_at: string;
  updated_at: string;
}

export interface ProjectCreateData {
  name: string;
  description?: string;
  status?: 'active' | 'archived' | 'completed';
}
