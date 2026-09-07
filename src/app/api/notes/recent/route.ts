import { NextResponse, type NextRequest } from "next/server";
import { db } from "@/lib/db";
import { getSessionUser } from "@/lib/auth";
import { getOrCreateAnonId, readAnonId } from "@/lib/anon";

export const dynamic = "force-dynamic";

const DEFAULT_LIMIT = 8;
const MAX_LIMIT = 50;

/**
 * GET /api/notes/recent?limit=8
 *
 * Lists the most-recently-viewed notes for the current visitor (user OR
 * anonymous). Includes the related note (with category + tags) so the
 * "Continue reading" drawer can render titles without another round-trip.
 *
 * Notes:
 *  - Identity resolution: if signed in → userId; else → anon_id cookie
 *    (minted on the fly via getOrCreateAnonId so future views stick).
 *  - Filters out views whose note no longer exists or is not published
 *    (for non-admins). Deleted notes cascade-delete the NoteView row, so
 *    this is mostly defensive — but a note can also be moved to DRAFT/
 *    UNPUBLISHED after a visitor viewed it, in which case we hide it.
 */
export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const rawLimit = Number.parseInt(searchParams.get("limit") ?? "", 10);
    const limit = Number.isFinite(rawLimit) && rawLimit > 0
      ? Math.min(Math.max(rawLimit, 1), MAX_LIMIT)
      : DEFAULT_LIMIT;

    // 1) Resolve identity
    const user = await getSessionUser();
    const isAdmin = user?.role === "ADMIN";

    let userId: string | null = null;
    let anonId: string | null = null;
    if (user) {
      userId = user.id;
    } else {
      // GET is read-mostly: prefer the existing cookie so we don't mint
      // identities for visitors who haven't recorded any views. If they
      // have no cookie, return an empty list — they'll get one on next
      // POST /view.
      anonId = await readAnonId();
    }

    if (!userId && !anonId) {
      return NextResponse.json({ views: [] });
    }

    const views = await db.noteView.findMany({
      where: {
        OR: [
          ...(userId ? [{ userId }] : []),
          ...(anonId ? [{ anonId }] : []),
        ],
      },
      include: {
        note: {
          include: {
            category: { select: { id: true, name: true, slug: true } },
            tags: { select: { id: true, name: true, slug: true } },
          },
        },
      },
      orderBy: { viewedAt: "desc" },
      take: limit,
    });

    // Drop views whose note was deleted or moved out of PUBLISHED for
    // non-admins. Cascade deletes already handle the "note vanished"
    // case, but this also covers the "drafted after viewing" case.
    const visible = views.filter((v) => {
      if (!v.note) return false;
      if (!isAdmin && v.note.status !== "PUBLISHED") return false;
      return true;
    });

    return NextResponse.json({ views: visible });
  } catch (err) {
    const message =
      err instanceof Error ? err.message : "Failed to fetch recent views.";
    return NextResponse.json(
      { error: message, views: [] },
      { status: 500 },
    );
  }
}

/**
 * DELETE /api/notes/recent
 *
 * Clears every NoteView row owned by the current visitor (user OR anon).
 * No admin required — a visitor can clear their own history.
 */
export async function DELETE() {
  try {
    const user = await getSessionUser();

    let userId: string | null = null;
    let anonId: string | null = null;
    if (user) {
      userId = user.id;
    } else {
      // For DELETE we want to clear whichever identity the visitor has.
      // Mint an anon cookie only if missing so the visitor's local state
      // (which assumed an anon identity) is consistent.
      anonId = await getOrCreateAnonId();
    }

    if (!userId && !anonId) {
      // Should be unreachable given the above, but be defensive.
      return NextResponse.json({ success: true });
    }

    await db.noteView.deleteMany({
      where: {
        OR: [
          ...(userId ? [{ userId }] : []),
          ...(anonId ? [{ anonId }] : []),
        ],
      },
    });

    return NextResponse.json({ success: true });
  } catch (err) {
    const message =
      err instanceof Error ? err.message : "Failed to clear recent views.";
    return NextResponse.json(
      { success: false, error: message },
      { status: 500 },
    );
  }
}
