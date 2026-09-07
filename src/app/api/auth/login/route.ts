import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import {
  createSession,
  verifyPassword,
  AuthError,
} from "@/lib/auth";
import { parseBody, z } from "@/lib/validation";
import { rateLimit } from "@/lib/rate-limit";

export const dynamic = "force-dynamic";

// Rate limit: 10 login attempts per minute per IP. Brute-force protection.
const loginLimiter = rateLimit({ intervalMs: 60_000, max: 10 });

const loginSchema = z.object({
  email: z.string().trim().toLowerCase().email().max(254),
  password: z.string().min(1).max(1024),
});

/**
 * POST /api/auth/login
 * Validates credentials and creates a session. Rate-limited to mitigate
 * brute-force attacks. Returns a generic "Invalid email or password." for
 * both unknown-user and wrong-password cases (no user enumeration).
 */
export async function POST(request: NextRequest) {
  try {
    // Rate limit check — returns 429 if exceeded.
    const { ok, retryAfterMs } = loginLimiter.check(request);
    if (!ok) {
      return NextResponse.json(
        {
          success: false,
          error: "Too many login attempts. Please try again shortly.",
        },
        {
          status: 429,
          headers: { "Retry-After": String(Math.ceil(retryAfterMs / 1000)) },
        },
      );
    }

    const parsed = await parseBody(request, loginSchema);
    if (!parsed.success) return parsed.response;
    const { email, password } = parsed.data;

    const user = await db.user.findUnique({
      where: { email },
    });

    // Always run a password verify against a dummy hash to keep timing
    // roughly constant whether or not the user exists (no timing oracle).
    const DUMMY_HASH =
      "$2a$10$CwTycUXWue0Thq9StjUM0uJ8.6fF2K8mF3n8mZxQ2mO0bYxQK8mO2";
    const hashToCheck = user?.password ?? DUMMY_HASH;
    const passwordValid = await verifyPassword(password, hashToCheck);

    if (!user || !passwordValid) {
      return NextResponse.json(
        { success: false, error: "Invalid email or password." },
        { status: 401 },
      );
    }

    await createSession({
      id: user.id,
      email: user.email,
      role: user.role,
    });

    return NextResponse.json({
      success: true,
      user: {
        id: user.id,
        email: user.email,
        name: user.name,
        role: user.role,
      },
    });
  } catch (err) {
    const message =
      err instanceof Error ? err.message : "An unexpected error occurred.";
    const status = err instanceof AuthError ? err.statusCode : 500;
    return NextResponse.json(
      { success: false, error: message },
      { status },
    );
  }
}
