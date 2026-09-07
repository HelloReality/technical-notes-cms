import { cookies } from "next/headers";

/**
 * Name of the anonymous-viewer cookie. Stores a stable random token (UUID)
 * so we can attribute NoteView rows to a single browser even when the
 * visitor isn't logged in.
 */
export const ANON_COOKIE = "anon_id";

const ANON_COOKIE_MAX_AGE = 60 * 60 * 24 * 365; // 1 year

/**
 * Read or create the anonymous-viewer id for the current request.
 *
 * - If the visitor is signed in, the caller should pass `userId` to the
 *   NoteView row and ignore this value entirely.
 * - Otherwise we look for an `anon_id` cookie. If absent we mint a fresh
 *   UUID (crypto.randomUUID is available in Node 19+ / Edge) and set it on
 *   the response cookie store.
 *
 * Always returns a non-empty string. Safe to call from route handlers and
 * server components (uses next/headers).
 */
export async function getOrCreateAnonId(): Promise<string> {
  const cookieStore = await cookies();
  const existing = cookieStore.get(ANON_COOKIE)?.value;
  if (existing && existing.trim().length > 0) {
    return existing;
  }

  const fresh = generateAnonId();
  cookieStore.set(ANON_COOKIE, fresh, {
    httpOnly: false,
    sameSite: "lax",
    path: "/",
    maxAge: ANON_COOKIE_MAX_AGE,
    secure: process.env.NODE_ENV === "production",
  });
  return fresh;
}

/**
 * Read the anon id without setting a cookie if it's missing. Useful when
 * you only want to query existing views (e.g. GET /recent) but don't want
 * to mint a new identity just from a read. The POST /view endpoint is the
 * one that creates identities.
 *
 * Returns null if the cookie is absent.
 */
export async function readAnonId(): Promise<string | null> {
  const cookieStore = await cookies();
  const value = cookieStore.get(ANON_COOKIE)?.value;
  if (!value || value.trim().length === 0) return null;
  return value;
}

function generateAnonId(): string {
  // crypto.randomUUID is available globally in Node 19+ / Edge runtimes.
  if (typeof crypto !== "undefined" && typeof crypto.randomUUID === "function") {
    return crypto.randomUUID();
  }
  // Fallback — should never run on a supported runtime, but keeps the
  // helper total and avoids a crash if invoked from an exotic context.
  return (
    Date.now().toString(36) +
    Math.random().toString(36).slice(2, 12) +
    Math.random().toString(36).slice(2, 12)
  );
}
