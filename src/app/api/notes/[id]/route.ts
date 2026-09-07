import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { requireAdmin, getSessionUser, AuthError } from "@/lib/auth";
import { slugify } from "@/lib/utils";
import { createNoteVersionSnapshot } from "@/lib/versioning";

export const dynamic = "force-dynamic";

const VALID_STATUSES = ["DRAFT", "PUBLISHED", "UNPUBLISHED"] as const;
type NoteStatus = (typeof VALID_STATUSES)[number];

function isValidStatus(value: string): value is NoteStatus {
  return (VALID_STATUSES as readonly string[]).includes(value);
}

interface RouteContext {
  params: Promise<{ id: string }>;
}

/**
 * GET /api/notes/[id]
 * Returns a single note. Non-admins can only view PUBLISHED notes.
 */
export async function GET(_request: NextRequest, context: RouteContext) {
  try {
    const { id } = await context.params;
    const note = await db.note.findUnique({
      where: { id },
      include: {
        category: { select: { id: true, name: true, slug: true } },
        tags: { select: { id: true, name: true, slug: true } },
      },
    });

    if (!note) {
      return NextResponse.json(
        { error: "Note not found." },
        { status: 404 }
      );
    }

    const currentUser = await getSessionUser();
    const isAdmin = currentUser?.role === "ADMIN";
    if (note.status !== "PUBLISHED" && !isAdmin) {
      return NextResponse.json(
        { error: "Note not found." },
        { status: 404 }
      );
    }

    return NextResponse.json({ note });
  } catch (err) {
    const message =
      err instanceof Error ? err.message : "Failed to fetch note.";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}

interface UpdateNoteBody {
  title?: string;
  slug?: string;
  description?: string;
  contentPath?: string;
  assetsPath?: string;
  status?: string;
  categoryId?: string;
  tags?: string[]; // tag names/slugs to sync (replaces)
  publishedAt?: string;
}

/**
 * PATCH /api/notes/[id] (admin only)
 * Updates note metadata, status, tags, etc.
 */
export async function PATCH(request: NextRequest, context: RouteContext) {
  try {
    const admin = await requireAdmin();

    const { id } = await context.params;
    const body = (await request.json()) as UpdateNoteBody;

    const existing = await db.note.findUnique({
      where: { id },
      include: { tags: { select: { name: true } } },
    });
    if (!existing) {
      return NextResponse.json(
        { success: false, error: "Note not found." },
        { status: 404 }
      );
    }

    // Best-effort snapshot of the CURRENT state so this edit is reversible.
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
        "[versioning] snapshot-before-update failed:",
        snapErr instanceof Error ? snapErr.message : snapErr
      );
    }

    const data: Record<string, unknown> = {};

    if (body.title !== undefined) {
      const title = body.title.trim();
      if (!title) {
        return NextResponse.json(
          { success: false, error: "Title cannot be empty." },
          { status: 400 }
        );
      }
      data.title = title;
    }

    if (body.slug !== undefined) {
      const slug = body.slug.trim() ? slugify(body.slug) : slugify(body.title ?? existing.title);
      // Ensure unique slug if changed
      if (slug !== existing.slug) {
        const collision = await db.note.findUnique({ where: { slug } });
        if (collision && collision.id !== id) {
          return NextResponse.json(
            { success: false, error: "Slug already in use." },
            { status: 409 }
          );
        }
      }
      data.slug = slug;
    }

    if (body.description !== undefined) {
      data.description = body.description.trim() || null;
    }

    if (body.contentPath !== undefined) {
      data.contentPath = body.contentPath.trim();
    }

    if (body.assetsPath !== undefined) {
      data.assetsPath = body.assetsPath.trim() || null;
    }

    if (body.categoryId !== undefined) {
      const category = await db.category.findUnique({
        where: { id: body.categoryId },
      });
      if (!category) {
        return NextResponse.json(
          { success: false, error: "Category not found." },
          { status: 404 }
        );
      }
      data.categoryId = body.categoryId;
    }

    let nextStatus: NoteStatus | undefined;
    if (body.status !== undefined) {
      const normalized = body.status.toUpperCase();
      if (!isValidStatus(normalized)) {
        return NextResponse.json(
          { success: false, error: `Invalid status: ${body.status}` },
          { status: 400 }
        );
      }
      nextStatus = normalized;
      data.status = nextStatus;

      // If we're moving to published and there's no publishedAt, set it
      if (nextStatus === "PUBLISHED" && !existing.publishedAt && body.publishedAt === undefined) {
        data.publishedAt = new Date();
      }
    }

    if (body.publishedAt !== undefined) {
      if (body.publishedAt === null || body.publishedAt === "") {
        data.publishedAt = null;
      } else {
        const parsed = new Date(body.publishedAt);
        if (isNaN(parsed.getTime())) {
          return NextResponse.json(
            { success: false, error: "Invalid publishedAt date." },
            { status: 400 }
          );
        }
        data.publishedAt = parsed;
      }
    }

    // Sync tags if provided
    if (body.tags !== undefined) {
      const tagNames = body.tags.map((t) => t.trim()).filter(Boolean);
      const resolved = await db.tag.findMany({
        where: {
          OR: [
            { name: { in: tagNames } },
            { slug: { in: tagNames.map(slugify) } },
          ],
        },
      });
      const missing = tagNames.filter(
        (t) =>
          !resolved.some(
            (tag) => tag.name === t || tag.slug === slugify(t)
          )
      );
      const created = await Promise.all(
        missing.map((name) => db.tag.create({ data: { name, slug: slugify(name) } }))
      );
      const allTags = [...resolved, ...created];
      data.tags = { set: allTags.map((t) => ({ id: t.id })) };
    }

    const note = await db.note.update({
      where: { id },
      data,
      include: {
        category: { select: { id: true, name: true, slug: true } },
        tags: { select: { id: true, name: true, slug: true } },
      },
    });

    return NextResponse.json({ success: true, note });
  } catch (err) {
    const message =
      err instanceof Error ? err.message : "Failed to update note.";
    const status = err instanceof AuthError ? err.statusCode : 500;
    return NextResponse.json(
      { success: false, error: message },
      { status }
    );
  }
}

/**
 * DELETE /api/notes/[id] (admin only)
 * Deletes a note.
 */
export async function DELETE(_request: NextRequest, context: RouteContext) {
  try {
    await requireAdmin();

    const { id } = await context.params;
    const existing = await db.note.findUnique({ where: { id } });
    if (!existing) {
      return NextResponse.json(
        { success: false, error: "Note not found." },
        { status: 404 }
      );
    }

    await db.note.delete({ where: { id } });
    return NextResponse.json({ success: true });
  } catch (err) {
    const message =
      err instanceof Error ? err.message : "Failed to delete note.";
    const status = err instanceof AuthError ? err.statusCode : 500;
    return NextResponse.json(
      { success: false, error: message },
      { status }
    );
  }
}
