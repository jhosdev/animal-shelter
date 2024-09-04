import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { getAccessToken } from './utils/auth';

export function middleware(request: NextRequest) {
  const token = getAccessToken();
  if (!token && !request.nextUrl.pathname.startsWith('/login')) {
    return NextResponse.redirect(new URL('/', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/animals/:path*', '/adoptions/:path*'],
};