'use client'

/**
 * Email Verification Component
 * Beautiful glassmorphism design for email verification
 * Author: Sharmeen Asif
 */

import { useState, useEffect } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import Link from 'next/link'
import { CheckCircle2, XCircle, Loader2, Mail, AlertCircle, ArrowLeft } from 'lucide-react'

type VerificationState = 'verifying' | 'success' | 'error' | 'missing_token'

export default function VerifyEmailForm() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const [state, setState] = useState<VerificationState>('verifying')
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const token = searchParams.get('token')

    if (!token) {
      setState('missing_token')
      return
    }

    // Auto-verify on mount
    verifyEmail(token)
  }, [searchParams])

  const verifyEmail = async (token: string) => {
    setState('verifying')
    setError(null)

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/verify-email`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ token }),
      })

      const result = await response.json()

      if (!response.ok) {
        if (response.status === 401) {
          throw new Error('Verification link has expired or is invalid. Please request a new one.')
        }
        throw new Error(result.detail || 'Failed to verify email')
      }

      setState('success')

      // Redirect to signin after 3 seconds
      setTimeout(() => {
        router.push('/auth/signin?message=Email verified successfully! Please sign in.')
      }, 3000)
    } catch (err: any) {
      setState('error')
      setError(err.message || 'Failed to verify email. Please try again.')
    }
  }

  // Missing Token State
  if (state === 'missing_token') {
    return (
      <div className="w-full max-w-md mx-auto">
        <div className="bg-yellow-50 border-2 border-yellow-200 rounded-2xl p-8 text-center">
          <div className="w-16 h-16 bg-yellow-500 rounded-full flex items-center justify-center mx-auto mb-4">
            <AlertCircle className="w-10 h-10 text-white" />
          </div>
          <h3 className="text-2xl font-bold text-yellow-900 mb-2">Verification Link Missing</h3>
          <p className="text-yellow-700 mb-6">
            No verification token found. Please use the link from your verification email.
          </p>

          <div className="space-y-3">
            <div className="bg-white/50 backdrop-blur-sm rounded-xl p-4 text-left">
              <h4 className="font-semibold text-gray-900 text-sm mb-2 flex items-center gap-2">
                <Mail className="w-4 h-4 text-blue-600" />
                How to verify your email:
              </h4>
              <ul className="space-y-2 text-sm text-gray-700">
                <li className="flex items-start gap-2">
                  <span className="text-blue-600 font-bold">1.</span>
                  <span>Check your email inbox for a message from us</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-blue-600 font-bold">2.</span>
                  <span>Click the verification link in the email</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-blue-600 font-bold">3.</span>
                  <span>You'll be redirected here automatically</span>
                </li>
              </ul>
            </div>

            <Link
              href="/auth/signin"
              className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-yellow-600 to-orange-600 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl transform hover:scale-[1.02] active:scale-[0.98] transition-all duration-200"
            >
              <ArrowLeft className="w-5 h-5" />
              Go to Sign In
            </Link>
          </div>
        </div>
      </div>
    )
  }

  // Verifying State
  if (state === 'verifying') {
    return (
      <div className="w-full max-w-md mx-auto">
        <div className="bg-blue-50 border-2 border-blue-200 rounded-2xl p-8 text-center">
          <div className="w-16 h-16 bg-blue-500 rounded-full flex items-center justify-center mx-auto mb-4">
            <Loader2 className="w-10 h-10 text-white animate-spin" />
          </div>
          <h3 className="text-2xl font-bold text-blue-900 mb-2">Verifying Your Email</h3>
          <p className="text-blue-700 mb-4">
            Please wait while we verify your email address...
          </p>
          <div className="flex justify-center">
            <div className="flex gap-1">
              <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
              <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
              <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  // Error State
  if (state === 'error') {
    return (
      <div className="w-full max-w-md mx-auto space-y-6">
        <div className="bg-red-50 border-2 border-red-200 rounded-2xl p-8 text-center">
          <div className="w-16 h-16 bg-red-500 rounded-full flex items-center justify-center mx-auto mb-4">
            <XCircle className="w-10 h-10 text-white" />
          </div>
          <h3 className="text-2xl font-bold text-red-900 mb-2">Verification Failed</h3>
          <p className="text-red-700 mb-6">
            {error || 'We couldn\'t verify your email address. The link may have expired or is invalid.'}
          </p>

          <div className="space-y-3">
            <Link
              href="/auth/signup"
              className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-red-600 to-pink-600 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl transform hover:scale-[1.02] active:scale-[0.98] transition-all duration-200"
            >
              Request New Verification Email
            </Link>

            <div>
              <Link
                href="/auth/signin"
                className="inline-flex items-center gap-2 text-sm text-gray-600 hover:text-gray-800 font-medium hover:underline transition-colors"
              >
                <ArrowLeft className="w-4 h-4" />
                Back to Sign In
              </Link>
            </div>
          </div>
        </div>

        <div className="bg-blue-50 border border-blue-200 rounded-xl p-4">
          <h4 className="font-semibold text-blue-900 text-sm mb-2 flex items-center gap-2">
            <AlertCircle className="w-4 h-4" />
            Common issues:
          </h4>
          <ul className="space-y-1 text-xs text-blue-700">
            <li>• Verification links expire after 24 hours</li>
            <li>• Each link can only be used once</li>
            <li>• Make sure you're using the latest email we sent</li>
          </ul>
        </div>
      </div>
    )
  }

  // Success State
  return (
    <div className="w-full max-w-md mx-auto">
      <div className="bg-gradient-to-br from-green-50 to-emerald-50 border-2 border-green-200 rounded-2xl p-8 text-center animate-in fade-in slide-in-from-bottom-4 duration-500">
        <div className="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-4">
          <CheckCircle2 className="w-10 h-10 text-white" />
        </div>
        <h3 className="text-2xl font-bold text-green-900 mb-2">Email Verified!</h3>
        <p className="text-green-700 mb-6">
          Your email address has been successfully verified. You can now sign in to your account.
        </p>

        <div className="bg-white/50 backdrop-blur-sm rounded-xl p-4 mb-6">
          <div className="flex items-center justify-center gap-2 text-green-700">
            <CheckCircle2 className="w-5 h-5" />
            <span className="font-medium">Account activated</span>
          </div>
        </div>

        <div className="flex justify-center mb-4">
          <Loader2 className="w-6 h-6 animate-spin text-green-600" />
        </div>
        <p className="text-sm text-green-600">Redirecting to sign in...</p>

        <div className="mt-6">
          <Link
            href="/auth/signin"
            className="inline-flex items-center gap-2 text-sm text-green-700 hover:text-green-800 font-medium hover:underline transition-colors"
          >
            Or click here to sign in now
            <ArrowLeft className="w-4 h-4 rotate-180" />
          </Link>
        </div>
      </div>
    </div>
  )
}
