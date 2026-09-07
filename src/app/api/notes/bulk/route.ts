import { NextRequest, NextResponse } from "next/server";
import { Prisma } from "@prisma/client";
import { db } from "@/lib/db";
import { requireAdmin, AuthError } from "@/lib/auth";
import { parseBody, z } from "@/lib/validation";
import type { BulkResult } from "@/lib/types";

export const dynamic = "force-dynamic";

// Cap the errors array so a batch of 200 all-failing notes does not balloon
// the JSON response. Beyond the cap we append a single "...and N more" line.
const MAX_ERRORS = 20;

const bulkSchema = z.object({
  action: z.enum(["PUBLISH", "UNPUBLISH", "DELETE"]),
  noteIds: z.array(z.string().min(1)).min(1).max(200),
});

/** Prisma throws P2025 when a record required for update/delete is missing. */
function isNotFound(err: unknown): boolean {
  return (
    err instanceof Prisma.PrismaClientKnownRequestError &&
    err.code === "P2025"
  );
}

function describeError(err: unknown, id: string, action: string): string {
  if (isNotFound(err)) return `Note ${id} not found`;
  if (err instanceof Error) return err.message;
  return `Failed to ${action.toLowerCase()} note ${id}`;
}

/**
 * POST /api/notes/bulk (admin only)
 *
 * Apply a single action (PUBLISH / UNPUBLISH / DELETE) to up to 200 notes.
 * Each note is processed independently so one failure does not abort the batch;
 * we collect per-id outcomes and return a { BulkResult } summary.
 */
export async function POST(request: NextRequest) {
  try {
    await requireAdmin();

    const parsed = await parseBody(request, bulkSchema);
    if (!parsed.success) return parsed.response;

    const { action, noteIds } = parsed.data;
    const requested = noteIds.length;

    let succeeded = 0;
    let failed = 0;
    const errors: string[] = [];

    for (const id of noteIds) {
      try {
        if (action === "PUBLISH") {
          // Preserve publishedAt history: only stamp "now" if never published.
          // Matches the PATCH /api/notes/[id] behaviour.
          const existing = await db.note.findUnique({
            where: { id },
            select: { publishedAt: true },
          });
          if (!existing) {
            throw new Error(`Note ${id} not found`);
          }
          await db.note.update({
            where: { id },
            data: {
              status: "PUBLISHED",
              publishedAt: existing.publishedAt ?? new Date(),
            },
          });
        } else if (action === "UNPUBLISH") {
          // Do NOT clear publishedAt — keep the publish history intact.
          await db.note.update({
            where: { id },
            data: { status: "UNPUBLISHED" },
          });
        } else {
          // DELETE
          await db.note.delete({ where: { id } });
        }
        succeeded += 1;
      } catch (err) {
        failed += 1;
        if (errors.length < MAX_ERRORS) {
          errors.push(describeError(err, id, action));
        }
      }
    }

    // If we hit the error cap, summarize the remaining failures so the client
    // still knows the true count without a massive payload.
    if (failed > errors.length) {
      const remaining = failed - errors.length;
      errors.push(`...and ${remaining} more`);
    }

    const result: BulkResult = {
      action,
      requested,
      succeeded,
      failed,
      errors,
    };

    return NextResponse.json({ success: true, result }, { status: 200 });
  } catch (err) {
    const message =
      err instanceof Error
        ? err.message
        : "Failed to perform bulk operation.";
    const status = err instanceof AuthError ? err.statusCode : 500;
    return NextResponse.json(
      { success: false, error: message },
      { status },
    );
  }
}
