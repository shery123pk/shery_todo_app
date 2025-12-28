/**
 * Global TypeScript Type Definitions
 *
 * Shared types used across the application (UI, utilities, etc.).
 * API-specific types are in lib/api-types.ts.
 *
 * Author: Sharmeen Asif
 */

/**
 * Re-export API types for convenience
 */
export type {
  ApiError,
  ApiErrorDetail,
  PaginationParams,
  PaginatedResponse,
  SignupData,
  SigninData,
  UserResponse,
  SigninResponse,
  TaskResponse,
  TaskListResponse,
  TaskCreateData,
  TaskUpdateData,
  OrganizationResponse,
  OrganizationCreateData,
  ProjectResponse,
  ProjectCreateData,
} from '../lib/api-types';

/**
 * Common UI component props
 */

export interface BaseComponentProps {
  /** CSS class name */
  className?: string;
  /** Children elements */
  children?: React.ReactNode;
}

export interface ButtonProps extends BaseComponentProps {
  /** Button variant */
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost';
  /** Button size */
  size?: 'sm' | 'md' | 'lg';
  /** Whether button is disabled */
  disabled?: boolean;
  /** Whether button is in loading state */
  loading?: boolean;
  /** Click handler */
  onClick?: () => void;
  /** Button type */
  type?: 'button' | 'submit' | 'reset';
}

export interface InputProps extends BaseComponentProps {
  /** Input value */
  value: string;
  /** Change handler */
  onChange: (value: string) => void;
  /** Input type */
  type?: 'text' | 'email' | 'password' | 'number' | 'tel' | 'url';
  /** Placeholder text */
  placeholder?: string;
  /** Whether input is disabled */
  disabled?: boolean;
  /** Whether input has error */
  error?: string;
  /** Input label */
  label?: string;
  /** Input name attribute */
  name?: string;
  /** Whether input is required */
  required?: boolean;
}

/**
 * Form handling types
 */

export interface FormFieldError {
  /** Field name */
  field: string;
  /** Error message */
  message: string;
}

export interface FormState<T> {
  /** Form values */
  values: T;
  /** Form errors */
  errors: Record<keyof T, string>;
  /** Whether form is submitting */
  isSubmitting: boolean;
  /** Whether form is valid */
  isValid: boolean;
  /** Whether form has been touched */
  touched: Record<keyof T, boolean>;
}

/**
 * Route and navigation types
 */

export interface RouteParams {
  /** Route parameters from URL */
  params: Record<string, string>;
  /** Query parameters from URL */
  searchParams: Record<string, string>;
}

/**
 * Status and state types
 */

export type LoadingState = 'idle' | 'loading' | 'success' | 'error';

export type SortDirection = 'asc' | 'desc';

export interface SortConfig<T> {
  /** Field to sort by */
  field: keyof T;
  /** Sort direction */
  direction: SortDirection;
}

export interface FilterConfig<T> {
  /** Filters to apply */
  filters: Partial<T>;
  /** Search query */
  search?: string;
}

/**
 * Data table types
 */

export interface Column<T> {
  /** Column key (must match data key) */
  key: keyof T;
  /** Column header label */
  label: string;
  /** Whether column is sortable */
  sortable?: boolean;
  /** Custom render function */
  render?: (value: T[keyof T], row: T) => React.ReactNode;
  /** Column width (CSS value) */
  width?: string;
}

export interface TableProps<T> {
  /** Table data */
  data: T[];
  /** Table columns */
  columns: Column<T>[];
  /** Loading state */
  loading?: boolean;
  /** Empty state message */
  emptyMessage?: string;
  /** Sort configuration */
  sortConfig?: SortConfig<T>;
  /** Sort change handler */
  onSortChange?: (config: SortConfig<T>) => void;
  /** Row click handler */
  onRowClick?: (row: T) => void;
}

/**
 * Modal and dialog types
 */

export interface ModalProps extends BaseComponentProps {
  /** Whether modal is open */
  isOpen: boolean;
  /** Close handler */
  onClose: () => void;
  /** Modal title */
  title?: string;
  /** Modal size */
  size?: 'sm' | 'md' | 'lg' | 'xl';
  /** Whether to close on overlay click */
  closeOnOverlayClick?: boolean;
}

export interface ConfirmDialogProps {
  /** Whether dialog is open */
  isOpen: boolean;
  /** Close handler */
  onClose: () => void;
  /** Confirm handler */
  onConfirm: () => void;
  /** Dialog title */
  title: string;
  /** Dialog message */
  message: string;
  /** Confirm button text */
  confirmText?: string;
  /** Cancel button text */
  cancelText?: string;
  /** Confirm button variant */
  confirmVariant?: 'primary' | 'danger';
}

/**
 * Toast notification types
 */

export type ToastType = 'success' | 'error' | 'warning' | 'info';

export interface Toast {
  /** Unique toast ID */
  id: string;
  /** Toast type */
  type: ToastType;
  /** Toast message */
  message: string;
  /** Toast duration (ms, 0 = no auto-dismiss) */
  duration?: number;
  /** Whether toast can be dismissed */
  dismissible?: boolean;
}

/**
 * File upload types
 */

export interface FileUpload {
  /** File object */
  file: File;
  /** Upload progress (0-100) */
  progress: number;
  /** Upload status */
  status: 'pending' | 'uploading' | 'success' | 'error';
  /** Error message if failed */
  error?: string;
  /** Uploaded file URL */
  url?: string;
}

/**
 * Utility types
 */

/** Make all properties optional recursively */
export type DeepPartial<T> = T extends object
  ? {
      [P in keyof T]?: DeepPartial<T[P]>;
    }
  : T;

/** Make all properties required recursively */
export type DeepRequired<T> = T extends object
  ? {
      [P in keyof T]-?: DeepRequired<T[P]>;
    }
  : T;

/** Extract keys of type T that have values of type V */
export type KeysOfType<T, V> = {
  [K in keyof T]-?: T[K] extends V ? K : never;
}[keyof T];

/** Make specific properties required */
export type RequireKeys<T, K extends keyof T> = T & Required<Pick<T, K>>;

/** Make specific properties optional */
export type OptionalKeys<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>;

/**
 * Environment variables (for type safety)
 */
export interface ProcessEnv {
  NEXT_PUBLIC_API_URL: string;
  NODE_ENV: 'development' | 'production' | 'test';
}

declare global {
  namespace NodeJS {
    interface ProcessEnv extends ProcessEnv {}
  }
}
