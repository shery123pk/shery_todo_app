/**
 * Next.js Middleware for Route Protection
 * Validates authentication for protected routes
 * Author: Sharmeen Asif
 */

import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

/**
 * Middleware function that runs on every request
 * Protects /tasks routes by checking authentication
 */
export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl

  // Only protect /tasks routes
  if (pathname.startsWith('/tasks')) {
    const sessionToken = request.cookies.get('session_token')

    // No session token - redirect to signin
    if (!sessionToken) {
      const signinUrl = new URL('/auth/signin', request.url)
      signinUrl.searchParams.set('returnUrl', pathname)
      return NextResponse.redirect(signinUrl)
    }

    // Verify session with backend
    try {
      const response = await fetch(`${API_URL}/api/auth/me`, {
        method: 'GET',
        headers: {
          Cookie: `session_token=${sessionToken.value}`,
        },
      })

      // Session invalid or expired - redirect to signin
      if (!response.ok) {
        const signinUrl = new URL('/auth/signin', request.url)
        signinUrl.searchParams.set('error', 'session_expired')
        signinUrl.searchParams.set('returnUrl', pathname)
        return NextResponse.redirect(signinUrl)
      }

      // Session valid - allow access
      return NextResponse.next()
    } catch (error) {
      // Network error or backend unavailable - redirect to signin
      const signinUrl = new URL('/auth/signin', request.url)
      signinUrl.searchParams.set('error', 'service_unavailable')
      return NextResponse.redirect(signinUrl)
    }
  }

  // All other routes - allow access
  return NextResponse.next()
}

/**
 * Configure which routes the middleware runs on
 */
export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public files (e.g., images in /public)
     */
    '/((?!api|_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
}
