import { NextResponse, type NextRequest } from "next/server";

/**
 * Global security middleware.
 *
 * - Adds conservative security headers to every response.
 * - Does NOT interfere with authenticated API routes; only sets headers.
 *
 * Authn/authz remain per-route via `requireAdmin()` in src/lib/auth.ts.
 */
export function middleware(_request: NextRequest) {
  const res = NextResponse.next();
  // Security headers
  res.headers.set("X-Content-Type-Options", "nosniff");
  res.headers.set("X-Frame-Options", "SAMEORIGIN");
  res.headers.set("Referrer-Policy", "strict-origin-when-cross-origin");
  res.headers.set(
    "Permissions-Policy",
    "camera=(), microphone=(), geolocation=()",
  );
  // Cache-control for API responses — never cache auth/session
  if (_request.nextUrl.pathname.startsWith("/api/auth")) {
    res.headers.set(
      "Cache-Control",
      "no-store, no-cache, must-revalidate, max-age=0",
    );
  }
  return res;
}

export const config = {
  // Run on all routes (headers are cheap); API + pages both benefit.
  matcher: ["/((?!_next/static|_next/image|favicon.ico|uploads).*)"],
};
