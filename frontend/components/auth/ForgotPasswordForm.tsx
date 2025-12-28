'use client'

/**
 * Forgot Password Form Component
 * Beautiful glassmorphism design for password reset request
 * Author: Sharmeen Asif
 */

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import * as z from 'zod'
import Link from 'next/link'
import { Mail, CheckCircle2, XCircle, Loader2, ArrowLeft, Key } from 'lucide-react'

// Validation schema
const forgotPasswordSchema = z.object({
  email: z.string()
    .email('Please enter a valid email address')
    .toLowerCase(),
})

type ForgotPasswordFormData = z.infer<typeof forgotPasswordSchema>

export default function ForgotPasswordForm() {
  const router = useRouter()
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)
  const [resetToken, setResetToken] = useState<string | null>(null)

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    getValues,
  } = useForm<ForgotPasswordFormData>({
    resolver: zodResolver(forgotPasswordSchema),
  })

  const onSubmit = async (data: ForgotPasswordFormData) => {
    setError(null)
    setResetToken(null)

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/forgot-password`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: data.email }),
      })

      const result = await response.json()

      if (!response.ok) {
        throw new Error(result.detail || 'Failed to send reset email')
      }

      setSuccess(true)

      // In development, show the reset token
      if (result.reset_token) {
        setResetToken(result.reset_token)
      }
    } catch (err: any) {
      setError(err.message || 'Failed to send reset email. Please try again.')
    }
  }

  if (success) {
    return (
      <div className="w-full max-w-md mx-auto space-y-6">
        <div className="bg-gradient-to-br from-green-50 to-emerald-50 border-2 border-green-200 rounded-2xl p-8 text-center animate-in fade-in slide-in-from-bottom-4 duration-500">
          <div className="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-4">
            <CheckCircle2 className="w-10 h-10 text-white" />
          </div>
          <h3 className="text-2xl font-bold text-green-900 mb-2">Check Your Email!</h3>
          <p className="text-green-700 mb-6">
            If an account exists with <strong>{getValues('email')}</strong>, we've sent password reset instructions to your inbox.
          </p>

          <div className="bg-white/50 backdrop-blur-sm rounded-xl p-4 mb-6 text-left">
            <h4 className="font-semibold text-gray-900 text-sm mb-2 flex items-center gap-2">
              <Mail className="w-4 h-4 text-blue-600" />
              What to do next:
            </h4>
            <ul className="space-y-2 text-sm text-gray-700">
              <li className="flex items-start gap-2">
                <span className="text-blue-600 font-bold">1.</span>
                <span>Check your email inbox (and spam folder)</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-blue-600 font-bold">2.</span>
                <span>Click the password reset link</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-blue-600 font-bold">3.</span>
                <span>Create a new secure password</span>
              </li>
            </ul>
          </div>

          {/* Development Mode: Show Reset Token */}
          {resetToken && (
            <div className="bg-yellow-50 border-2 border-yellow-200 rounded-xl p-4 mb-6 text-left">
              <h4 className="font-semibold text-yellow-900 text-sm mb-2 flex items-center gap-2">
                <Key className="w-4 h-4" />
                Development Mode - Reset Token:
              </h4>
              <div className="bg-white rounded-lg p-3 font-mono text-xs break-all text-gray-700">
                {resetToken}
              </div>
              <p className="text-xs text-yellow-700 mt-2">
                This token is only shown in development. Use it to test the reset password page.
              </p>
              <Link
                href={`/auth/reset-password?token=${resetToken}`}
                className="mt-3 inline-flex items-center gap-2 text-sm text-yellow-800 hover:text-yellow-900 font-medium hover:underline transition-colors"
              >
                <ArrowLeft className="w-4 h-4" />
                Go to Reset Password page
              </Link>
            </div>
          )}

          <div className="space-y-3">
            <button
              onClick={() => router.push('/auth/signin')}
              className="w-full py-3 px-6 bg-gradient-to-r from-green-600 to-emerald-600 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl transform hover:scale-[1.02] active:scale-[0.98] transition-all duration-200 flex items-center justify-center gap-2"
            >
              <ArrowLeft className="w-5 h-5" />
              Back to Sign In
            </button>

            <button
              onClick={() => {
                setSuccess(false)
                setResetToken(null)
              }}
              className="w-full py-2.5 text-sm text-gray-600 hover:text-gray-800 transition-colors"
            >
              Didn't receive email? Try again
            </button>
          </div>
        </div>

        {/* Help Text */}
        <div className="bg-blue-50 border border-blue-200 rounded-xl p-4">
          <p className="text-xs text-blue-700">
            <strong>Note:</strong> For security reasons, we don't reveal whether an email address is registered.
            If you don't receive an email within 5 minutes, check your spam folder or try signing up.
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="w-full max-w-md space-y-6">
      {/* Error Alert */}
      {error && (
        <div className="bg-red-50 border-2 border-red-200 rounded-xl p-4 flex items-start gap-3 animate-in fade-in slide-in-from-top-2">
          <XCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
          <div className="flex-1">
            <h4 className="font-semibold text-red-900 text-sm">Request failed</h4>
            <p className="text-red-700 text-sm mt-1">{error}</p>
          </div>
        </div>
      )}

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
        {/* Instructions */}
        <div className="bg-blue-50 border border-blue-200 rounded-xl p-4">
          <p className="text-sm text-blue-700">
            Enter your email address and we'll send you instructions to reset your password.
          </p>
        </div>

        {/* Email Field */}
        <div className="space-y-2">
          <label htmlFor="email" className="block text-sm font-semibold text-gray-700">
            Email Address
          </label>
          <div className="relative">
            <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              {...register('email')}
              id="email"
              type="email"
              placeholder="you@example.com"
              autoComplete="email"
              autoFocus
              className={`w-full pl-11 pr-4 py-3 border-2 rounded-xl bg-white/50 backdrop-blur-sm transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                errors.email ? 'border-red-300' : 'border-gray-200 hover:border-gray-300'
              }`}
            />
          </div>
          {errors.email && (
            <p className="text-sm text-red-600 flex items-center gap-1">
              <XCircle className="w-4 h-4" />
              {errors.email.message}
            </p>
          )}
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isSubmitting}
          className="w-full py-3.5 px-6 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl transform hover:scale-[1.02] active:scale-[0.98] transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center justify-center gap-2"
        >
          {isSubmitting ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Sending reset link...
            </>
          ) : (
            <>
              <Mail className="w-5 h-5" />
              Send Reset Link
            </>
          )}
        </button>

        {/* Back to Sign In Link */}
        <div className="text-center">
          <Link
            href="/auth/signin"
            className="inline-flex items-center gap-2 text-sm text-gray-600 hover:text-gray-800 font-medium hover:underline transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to Sign In
          </Link>
        </div>

        {/* Security Note */}
        <div className="bg-gray-50 border border-gray-200 rounded-xl p-4">
          <p className="text-xs text-gray-600">
            <strong>Security tip:</strong> Make sure you're on the correct website before entering your email.
            We'll never ask for your password via email.
          </p>
        </div>
      </form>
    </div>
  )
}
