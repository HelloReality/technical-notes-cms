import { NextResponse, type NextRequest } from "next/server";
import { z, type ZodSchema } from "zod";

/**
 * Safely parse + validate a JSON request body against a zod schema.
 * Returns `{ success: true, data }` on success or
 * `{ success: false, response }` with a 400 response on failure.
 *
 * Usage:
 *   const parsed = await parseBody(request, loginSchema);
 *   if (!parsed.success) return parsed.response;
 *   const data = parsed.data;
 */
export async function parseBody<T>(
  request: NextRequest,
  schema: ZodSchema<T>,
): Promise<
  | { success: true; data: T }
  | { success: false; response: NextResponse }
> {
  try {
    const json = await request.json();
    const result = schema.safeParse(json);
    if (!result.success) {
      const first = result.error.issues[0];
      const message = first
        ? `${first.path.join(".") || "value"}: ${first.message}`
        : "Invalid request body.";
      return {
        success: false,
        response: NextResponse.json(
          { success: false, error: message },
          { status: 400 },
        ),
      };
    }
    return { success: true, data: result.data };
  } catch {
    return {
      success: false,
      response: NextResponse.json(
        { success: false, error: "Invalid JSON body." },
        { status: 400 },
      ),
    };
  }
}

// Re-export z for convenience in route files.
export { z };
