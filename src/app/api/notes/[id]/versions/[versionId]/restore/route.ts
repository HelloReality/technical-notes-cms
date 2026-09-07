import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { requireAdmin, AuthError } from "@/lib/auth";
import { slugify } from "@/lib/utils";
import {
  createNoteVersionSnapshot,
  parseTagsJson,
} from "@/lib/versioning";

export const dynamic = "force-dynamic";

interface RouteContext {
  params: Promise<{ id: string; versionId: string }>;
}

/**
 * POST /api/notes/[id]/versions/[versionId]/restore (admin only)
 *
 * Restores a note to a previous version's content/metadata.
 *
 * Flow:
 *  1. Look up the target NoteVersion (must belong to the note).
 *  2. Snapshot the CURRENT note state as a new NoteVersion so the restore
 *     itself is reversible.
 *  3. Update the note with the version's fields. Slug collisions are
 *     resolved by appending a short random suffix. Tags are re-resolved by
 *     name (creating missing ones) and reconnected.
 *
 * Returns the updated note including category + tags.
 */
export async function POST(_request: NextRequest, context: RouteContext) {
  try {
    const admin = await requireAdmin();
    const { id, versionId } = await context.params;

    const version = await db.noteVersion.findUnique({
      where: { id: versionId },
    });
    if (!version || version.noteId !== id) {
      return NextResponse.json(
        { success: false, error: "Version not found." },
        { status: 404 },
      );
    }

    const existing = await db.note.findUnique({
      where: { id },
      include: {
        tags: { select: { id: true, name: true, slug: true } },
      },
    });
    if (!existing) {
      return NextResponse.json(
        { success: false, error: "Note not found." },
        { status: 404 },
      );
    }

    // Best-effort snapshot of the CURRENT state so the restore is reversible.
    try {
      await createNoteVersionSnapshot({
        noteId: existing.id,
        title: existing.title,
        slug: existing.slug,
        description: existing.description,
        contentPath: existing.contentPath,
        assetsPath: existing.assetsPath,
        status: existing.status,
        categoryId: existing.categoryId,
        tags: existing.tags.map((t) => t.name),
        user: admin,
      });
    } catch (snapErr) {
      console.error(
        "[versioning] snapshot-before-restore failed:",
        snapErr instanceof Error ? snapErr.message : snapErr,
      );
    }

    // Determine slug — only munge if it changed AND collides with another note.
    let nextSlug = version.slug;
    if (version.slug !== existing.slug) {
      const collision = await db.note.findUnique({
        where: { slug: version.slug },
      });
      if (collision && collision.id !== id) {
        const suffix = Math.random().toString(36).slice(2, 6);
        nextSlug = `${version.slug}-${suffix}`;
      }
    }

    // Re-resolve tags from the version's tagsJson (create missing ones).
    const tagNames = parseTagsJson(version.tagsJson);
    const resolved = await db.tag.findMany({
      where: {
        OR: [
          { name: { in: tagNames } },
          { slug: { in: tagNames.map(slugify) } },
        ],
      },
    });
    const missing = tagNames.filter(
      (name) =>
        !resolved.some(
          (tag) => tag.name === name || tag.slug === slugify(name),
        ),
    );
    const created = await Promise.all(
      missing.map((name) =>
        db.tag.create({ data: { name, slug: slugify(name) } }),
      ),
    );
    const allTags = [...resolved, ...created];

    const note = await db.note.update({
      where: { id },
      data: {
        title: version.title,
        slug: nextSlug,
        description: version.description,
        contentPath: version.contentPath,
        assetsPath: version.assetsPath,
        status: version.status,
        categoryId: version.categoryId,
        tags: { set: allTags.map((t) => ({ id: t.id })) },
      },
      include: {
        category: { select: { id: true, name: true, slug: true } },
        tags: { select: { id: true, name: true, slug: true } },
      },
    });

    return NextResponse.json({ success: true, note });
  } catch (err) {
    const message =
      err instanceof Error ? err.message : "Failed to restore version.";
    const status = err instanceof AuthError ? err.statusCode : 500;
    return NextResponse.json(
      { success: false, error: message },
      { status },
    );
  }
}
