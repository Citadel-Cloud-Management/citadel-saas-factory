import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const PUBLIC_PATHS = ["/", "/login", "/signup", "/privacy", "/terms"];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Allow public paths
  if (PUBLIC_PATHS.some((p) => pathname === p || pathname.startsWith("/api"))) {
    return NextResponse.next();
  }

  // Allow static assets
  if (pathname.startsWith("/_next") || pathname.includes(".")) {
    return NextResponse.next();
  }

  // Check for auth token in cookies (set by client-side after login)
  const token = request.cookies.get("access_token")?.value;

  // For dashboard routes, redirect to login if no token
  if (pathname.startsWith("/dashboard") && !token) {
    const loginUrl = new URL("/login", request.url);
    loginUrl.searchParams.set("redirect", pathname);
    return NextResponse.redirect(loginUrl);
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"],
};
