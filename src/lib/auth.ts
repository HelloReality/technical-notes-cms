import { SignJWT, jwtVerify } from "jose";
import { cookies } from "next/headers";
import bcrypt from "bcryptjs";
import { db } from "@/lib/db";

// Cookie name for the session token
export const SESSION_COOKIE = "cms_session";

// Session expiration (7 days in seconds)
const SESSION_MAX_AGE_SECONDS = 60 * 60 * 24 * 7;

// Helper to get the secret as Uint8Array for jose
function getSecret(): Uint8Array {
  const secret =
    process.env.NEXTAUTH_SECRET || "fallback-dev-secret-change-in-production";
  return new TextEncoder().encode(secret);
}

// Public payload of the JWT
export interface SessionPayload {
  userId: string;
  email: string;
  role: string;
}

// Full session user info (without sensitive fields)
export interface SessionUser {
  id: string;
  email: string;
  name: string | null;
  role: string;
}

/**
 * Hash a plaintext password using bcryptjs.
 */
export async function hashPassword(password: string): Promise<string> {
  const salt = await bcrypt.genSalt(10);
  return bcrypt.hash(password, salt);
}

/**
 * Verify a plaintext password against a bcrypt hash.
 */
export async function verifyPassword(
  password: string,
  hash: string
): Promise<boolean> {
  return bcrypt.compare(password, hash);
}

/**
 * Create a new session for the given user and set the httpOnly cookie.
 * Returns the signed JWT token.
 */
export async function createSession(user: {
  id: string;
  email: string;
  role: string;
}): Promise<string> {
  const payload: SessionPayload = {
    userId: user.id,
    email: user.email,
    role: user.role,
  };

  const token = await new SignJWT(payload)
    .setProtectedHeader({ alg: "HS256" })
    .setIssuedAt()
    .setExpirationTime(`${SESSION_MAX_AGE_SECONDS}s`)
    .sign(getSecret());

  const cookieStore = await cookies();
  cookieStore.set(SESSION_COOKIE, token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax",
    path: "/",
    maxAge: SESSION_MAX_AGE_SECONDS,
  });

  return token;
}

/**
 * Read and verify the JWT from the cookie. Returns the payload or null.
 */
export async function getSession(): Promise<SessionPayload | null> {
  try {
    const cookieStore = await cookies();
    const token = cookieStore.get(SESSION_COOKIE)?.value;
    if (!token) return null;

    const { payload } = await jwtVerify(token, getSecret(), {
      algorithms: ["HS256"],
    });

    return {
      userId: payload.userId as string,
      email: payload.email as string,
      role: payload.role as string,
    };
  } catch {
    return null;
  }
}

/**
 * Get the authenticated user object from the current session, or null.
 */
export async function getSessionUser(): Promise<SessionUser | null> {
  const session = await getSession();
  if (!session) return null;

  const user = await db.user.findUnique({
    where: { id: session.userId },
    select: { id: true, email: true, name: true, role: true },
  });

  return user;
}

/**
 * Destroy the session by clearing the cookie.
 */
export async function destroySession(): Promise<void> {
  const cookieStore = await cookies();
  cookieStore.delete(SESSION_COOKIE);
}

/**
 * Require that the current user is an admin. Returns the user object or
 * throws a structured error that can be handled by the API route.
 */
export async function requireAdmin(): Promise<SessionUser> {
  const user = await getSessionUser();
  if (!user) {
    throw new AuthError("Unauthorized: authentication required", 401);
  }
  if (user.role !== "ADMIN") {
    throw new AuthError("Forbidden: admin role required", 403);
  }
  return user;
}

/**
 * Custom auth error with status code for API handlers.
 */
export class AuthError extends Error {
  statusCode: number;
  constructor(message: string, statusCode: number = 401) {
    super(message);
    this.name = "AuthError";
    this.statusCode = statusCode;
  }
}
