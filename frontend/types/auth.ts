/**
 * Authentication Type Definitions
 * TypeScript types for auth-related data structures
 * Author: Sharmeen Asif
 */

export interface User {
  id: string
  email: string
  full_name: string
  email_verified: boolean
  created_at: string
  updated_at: string
}

export interface Session {
  id: string
  user_id: string
  expires_at: string
  ip_address?: string
  user_agent?: string
  created_at: string
}

export interface AuthTokens {
  access_token: string
  refresh_token?: string
  token_type: string
}

export interface SignupData {
  email: string
  password: string
  full_name: string
}

export interface SigninData {
  email: string
  password: string
  remember_me?: boolean
}

export interface VerifyEmailData {
  token: string
}

export interface ForgotPasswordData {
  email: string
}

export interface ResetPasswordData {
  token: string
  new_password: string
}

export interface ChangePasswordData {
  current_password: string
  new_password: string
}

export interface UpdateProfileData {
  full_name?: string
  email?: string
}
