import { NextResponse } from 'next/server';
import { Client, Account } from 'appwrite';

const client = new Client()
  .setEndpoint(process.env.NEXT_PUBLIC_APPWRITE_ENDPOINT)
  .setProject(process.env.NEXT_PUBLIC_APPWRITE_PROJECT_ID);

const account = new Account(client);

export async function middleware(request) {
  const { pathname } = request.nextUrl;
  const protectedPaths = ['/auth/dashboard'];
  const publicPaths = ['/login', '/verify'];

  // Read Appwrite session cookie
  const sessionCookie = request.cookies.get('a_session'); // Appwrite default cookie

  let isAuthenticated = false;

  if (sessionCookie) {
    try {
      // Attempt to get current session using cookie
      await account.get();
      isAuthenticated = true;
    } catch {
      isAuthenticated = false;
    }
  }

  // Redirect logic
  if (isAuthenticated && publicPaths.some(path => pathname.startsWith(path))) {
    // Authenticated users cannot access login/verify
    return NextResponse.redirect(new URL('/auth/dashboard', request.url));
  }

  if (!isAuthenticated && protectedPaths.some(path => pathname.startsWith(path))) {
    // Unauthenticated users cannot access dashboard
    return NextResponse.redirect(new URL('/login', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/auth/:path*', '/login', '/verify'],
};
