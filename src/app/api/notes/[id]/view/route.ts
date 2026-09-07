import { NextResponse, type NextRequest } from "next/server";
import { db } from "@/lib/db";
import { getSessionUser } from "@/lib/auth";
import { getOrCreateAnonId } from "@/lib/anon";

export const dynamic = "force-dynamic";

interface RouteContext {
  params: Promise<{ id: string }>;
}

/**
 * POST /api/notes/[id]/view
 *
 * Records a view on a note for the current visitor (authenticated OR
 * anonymous). No auth required — anonymous visitors get an `anon_id`
 * cookie minted on first call so future reads can list their history.
 *
 * Behaviour:
 *  - If the note doesn't exist OR isn't PUBLISHED (and visitor isn't
 *    admin) → 404 silently. We never record views on drafts for visitors.
 *  - To avoid duplicate rows when a viewer re-opens a note, we look for
 *    the most recent NoteView for this (userId OR anonId) + noteId and
 *    update its viewedAt = now. Otherwise we create a new row.
 *  - Always returns `{ success: true }` so the client fire-and-forgets.
 */
export async function POST(_request: NextRequest, context: RouteContext) {
  try {
    const { id } = await context.params;

    // 1) Resolve the note. We do this before touching identities so an
    //    invalid note id never mints an anon_id cookie.
    const note = await db.note.findUnique({
      where: { id },
      select: { id: true, status: true },
    });

    if (!note) {
      // Silent 404 — don't leak existence.
      return NextResponse.json(
        { success: false, error: "Note not found." },
        { status: 404 },
      );
    }

    // 2) Resolve identity — prefer a signed-in user, fall back to anon.
    const user = await getSessionUser();
    const isAdmin = user?.role === "ADMIN";

    // Visitors (non-admins) can only record views on PUBLISHED notes.
    if (note.status !== "PUBLISHED" && !isAdmin) {
      return NextResponse.json(
        { success: false, error: "Note not found." },
        { status: 404 },
      );
    }

    let userId: string | null = null;
    let anonId: string | null = null;
    if (user) {
      userId = user.id;
    } else {
      anonId = await getOrCreateAnonId();
    }

    // 3) Upsert-by-hand: find the latest existing view for this
    //    (userId OR anonId) + noteId; update its viewedAt, else create.
    //    Prisma SQLite doesn't have a composite unique constraint here,
    //    so we do a findFirst + update/create pair instead of upsert.
    const existing = await db.noteView.findFirst({
      where: {
        noteId: id,
        OR: [
          ...(userId ? [{ userId }] : []),
          ...(anonId ? [{ anonId }] : []),
        ],
      },
      orderBy: { viewedAt: "desc" },
      select: { id: true },
    });

    if (existing) {
      await db.noteView.update({
        where: { id: existing.id },
        data: { viewedAt: new Date(), userId, anonId },
      });
    } else {
      await db.noteView.create({
        data: {
          noteId: id,
          userId,
          anonId,
          viewedAt: new Date(),
        },
      });
    }

    return NextResponse.json({ success: true });
  } catch (err) {
    const message =
      err instanceof Error ? err.message : "Failed to record view.";
    return NextResponse.json(
      { success: false, error: message },
      { status: 500 },
    );
  }
}
