import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { requireAdmin, AuthError } from "@/lib/auth";
import { parseTagsJson } from "@/lib/versioning";

export const dynamic = "force-dynamic";

interface RouteContext {
  params: Promise<{ id: string }>;
}

/**
 * GET /api/notes/[id]/versions (admin only)
 * Lists every saved version snapshot for a note, newest first.
 *
 * Each row is returned with all NoteVersion scalar fields plus a parsed
 * `tags` array (mirroring the parsed shape used by the shared types).
 */
export async function GET(_request: NextRequest, context: RouteContext) {
  try {
    await requireAdmin();
    const { id } = await context.params;

    const versions = await db.noteVersion.findMany({
      where: { noteId: id },
      orderBy: { createdAt: "desc" },
    });

    const formatted = versions.map((v) => ({
      id: v.id,
      noteId: v.noteId,
      title: v.title,
      slug: v.slug,
      description: v.description,
      contentPath: v.contentPath,
      assetsPath: v.assetsPath,
      status: v.status,
      categoryId: v.categoryId,
      tagsJson: v.tagsJson,
      tags: parseTagsJson(v.tagsJson),
      createdById: v.createdById,
      createdByName: v.createdByName,
      createdAt: v.createdAt,
    }));

    return NextResponse.json({ versions: formatted });
  } catch (err) {
    const message =
      err instanceof Error ? err.message : "Failed to fetch versions.";
    const status = err instanceof AuthError ? err.statusCode : 500;
    return NextResponse.json({ error: message }, { status });
  }
}
