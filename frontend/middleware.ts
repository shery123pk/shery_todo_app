/**
 * Next.js Middleware for Route Protection
 * With Bearer token auth, middleware can't validate tokens (no access to localStorage).
 * Auth is handled client-side by AuthContext. Middleware is kept minimal.
 * Author: Sharmeen Asif
 */

import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

/**
 * Middleware function - passes through all requests.
 * Auth protection is handled client-side via AuthContext.
 */
export function middleware(request: NextRequest) {
  return NextResponse.next()
}

export const config = {
  matcher: [
    '/((?!api|_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
}
