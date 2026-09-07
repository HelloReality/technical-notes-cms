import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";

export const dynamic = "force-dynamic";
export const revalidate = 0;

interface PublishedItem {
  scheduleId: string;
  noteId: string;
}

/**
 * GET /api/cron/publish?secret=XXX
 * (or via `x-cron-secret` header)
 *
 * Promotes any PENDING ScheduledPublish whose publishAt has passed:
 *  - sets the corresponding Note to status=PUBLISHED (with publishedAt if unset),
 *  - marks the schedule status=DONE with completedAt=now.
 *
 * Authenticated by a shared secret compared against process.env.CRON_SECRET.
 * Each schedule+note update runs in its own transaction so one failure
 * does not abort the batch.
 */
export async function GET(request: NextRequest) {
  try {
    const expected = process.env.CRON_SECRET;
    if (!expected) {
      // Server misconfiguration — refuse to run.
      return NextResponse.json(
        { success: false, error: "CRON_SECRET is not configured." },
        { status: 500 },
      );
    }

    const provided =
      request.nextUrl.searchParams.get("secret") ||
      request.headers.get("x-cron-secret");

    if (!provided || provided !== expected) {
      return NextResponse.json(
        { success: false, error: "Unauthorized." },
        { status: 401 },
      );
    }

    const now = new Date();

    const due = await db.scheduledPublish.findMany({
      where: {
        status: "PENDING",
        publishAt: { lte: now },
      },
      select: { id: true, noteId: true },
    });

    const items: PublishedItem[] = [];
    let failed = 0;

    for (const schedule of due) {
      try {
        await db.$transaction([
          db.note.update({
            where: { id: schedule.noteId },
            data: {
              status: "PUBLISHED",
              publishedAt: now,
            },
          }),
          db.scheduledPublish.update({
            where: { id: schedule.id },
            data: {
              status: "DONE",
              completedAt: now,
            },
          }),
        ]);

        items.push({ scheduleId: schedule.id, noteId: schedule.noteId });
      } catch (err) {
        failed += 1;
        console.error(
          `[cron/publish] Failed to publish schedule ${schedule.id} (note ${schedule.noteId}):`,
          err instanceof Error ? err.message : err,
        );
      }
    }

    return NextResponse.json({
      success: true,
      published: items.length,
      failed,
      items,
    });
  } catch (err) {
    console.error("[cron/publish] Unexpected error:", err);
    const message =
      err instanceof Error ? err.message : "Failed to run scheduled publish.";
    return NextResponse.json(
      { success: false, error: message },
      { status: 500 },
    );
  }
}
