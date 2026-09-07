/**
 * Lightweight in-memory rate limiter for API routes.
 *
 * Not suitable for multi-instance production deployments (use Redis or
 * Upstash there), but sufficient for a single-instance sandbox and stops
 * brute-force login attempts.
 *
 * Usage in a route handler:
 *   const rl = rateLimit({ intervalMs: 60_000, max: 10 });
 *   const { ok } = rl.check(request);
 *   if (!ok) return NextResponse.json({ error: "Too many requests" }, { status: 429 });
 */

interface RateLimitOpts {
  /** Sliding window length in ms */
  intervalMs: number;
  /** Max hits per window per identity */
  max: number;
}

interface Hit {
  count: number;
  resetAt: number;
}

const buckets = new Map<string, Hit>();

// Periodically evict expired buckets to avoid memory growth.
if (typeof setInterval !== "undefined") {
  setInterval(() => {
    const now = Date.now();
    for (const [key, hit] of buckets) {
      if (hit.resetAt <= now) buckets.delete(key);
    }
  }, 60_000).unref?.();
}

export function rateLimit(opts: RateLimitOpts) {
  return {
    check(request: Request, identity?: string): { ok: boolean; retryAfterMs: number } {
      const ip =
        request.headers.get("x-forwarded-for")?.split(",")[0]?.trim() ||
        request.headers.get("x-real-ip") ||
        "anonymous";
      const key = identity ? `${ip}:${identity}` : ip;
      const now = Date.now();
      const existing = buckets.get(key);
      if (!existing || existing.resetAt <= now) {
        buckets.set(key, { count: 1, resetAt: now + opts.intervalMs });
        return { ok: true, retryAfterMs: opts.intervalMs };
      }
      existing.count += 1;
      if (existing.count > opts.max) {
        return { ok: false, retryAfterMs: existing.resetAt - now };
      }
      return { ok: true, retryAfterMs: existing.resetAt - now };
    },
  };
}
