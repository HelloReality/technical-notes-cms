import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { requireAdmin, AuthError } from "@/lib/auth";
import { parseBody, z } from "@/lib/validation";

export const dynamic = "force-dynamic";

// 5 minutes of tolerance for slightly-past publishAt values (clock drift, etc.)
const PAST_TOLERANCE_MS = 5 * 60 * 1000;

const createScheduleSchema = z.object({
  noteId: z.string().trim().min(1, "noteId is required"),
  publishAt: z.string().trim().min(1, "publishAt is required"),
});

/**
 * GET /api/scheduled-publish (admin only)
 * Returns all PENDING scheduled publishes, sorted by publishAt ascending.
 */
export async function GET(_request: NextRequest) {
  try {
    await requireAdmin();

    const schedules = await db.scheduledPublish.findMany({
      where: { status: "PENDING" },
      orderBy: { publishAt: "asc" },
    });

    return NextResponse.json({ schedules });
  } catch (err) {
    const message =
      err instanceof Error ? err.message : "Failed to list schedules.";
    const status = err instanceof AuthError ? err.statusCode : 500;
    return NextResponse.json(
      { success: false, error: message },
      { status },
    );
  }
}

/**
 * POST /api/scheduled-publish (admin only)
 * Creates or replaces a pending scheduled publish for a note.
 * Because `noteId` is unique, we upsert so any existing schedule is replaced.
 */
export async function POST(request: NextRequest) {
  try {
    const admin = await requireAdmin();

    const parsed = await parseBody(request, createScheduleSchema);
    if (!parsed.success) return parsed.response;
    const { noteId, publishAt } = parsed.data;

    const publishDate = new Date(publishAt);
    if (isNaN(publishDate.getTime())) {
      return NextResponse.json(
        { success: false, error: "publishAt must be a valid ISO date string." },
        { status: 400 },
      );
    }

    const now = Date.now();
    if (publishDate.getTime() < now - PAST_TOLERANCE_MS) {
      return NextResponse.json(
        { success: false, error: "publishAt must be in the future." },
        { status: 400 },
      );
    }

    const note = await db.note.findUnique({
      where: { id: noteId },
      select: { id: true },
    });
    if (!note) {
      return NextResponse.json(
        { success: false, error: "Note not found." },
        { status: 404 },
      );
    }

    // noteId is @unique → upsert replaces any existing schedule for this note,
    // resetting it to PENDING (cleared completedAt) with the new publishAt.
    const schedule = await db.scheduledPublish.upsert({
      where: { noteId },
      create: {
        noteId,
        publishAt: publishDate,
        status: "PENDING",
        createdById: admin.id,
        createdByName: admin.name,
      },
      update: {
        publishAt: publishDate,
        status: "PENDING",
        completedAt: null,
        createdById: admin.id,
        createdByName: admin.name,
      },
    });

    return NextResponse.json(
      { success: true, schedule },
      { status: 201 },
    );
  } catch (err) {
    const message =
      err instanceof Error ? err.message : "Failed to create schedule.";
    const status = err instanceof AuthError ? err.statusCode : 500;
    return NextResponse.json(
      { success: false, error: message },
      { status },
    );
  }
}

/**
 * DELETE /api/scheduled-publish?noteId=xxx (admin only)
 * Cancels the pending schedule for a note (sets status=CANCELLED, keeps the row for history).
 * Idempotent: returns success even if no schedule exists.
 */
export async function DELETE(request: NextRequest) {
  try {
    await requireAdmin();

    const noteId = request.nextUrl.searchParams.get("noteId");
    if (!noteId || !noteId.trim()) {
      return NextResponse.json(
        { success: false, error: "noteId query parameter is required." },
        { status: 400 },
      );
    }

    const existing = await db.scheduledPublish.findUnique({
      where: { noteId },
      select: { id: true },
    });

    if (existing) {
      await db.scheduledPublish.update({
        where: { noteId },
        data: { status: "CANCELLED" },
      });
    }

    return NextResponse.json({ success: true });
  } catch (err) {
    const message =
      err instanceof Error ? err.message : "Failed to cancel schedule.";
    const status = err instanceof AuthError ? err.statusCode : 500;
    return NextResponse.json(
      { success: false, error: message },
      { status },
    );
  }
}
