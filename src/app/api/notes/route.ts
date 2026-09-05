import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { requireAdmin, getSessionUser, AuthError } from "@/lib/auth";
import { slugify } from "@/lib/utils";

export const dynamic = "force-dynamic";

const VALID_STATUSES = ["DRAFT", "PUBLISHED", "UNPUBLISHED"] as const;
type NoteStatus = (typeof VALID_STATUSES)[number];

function isValidStatus(value: string | null): value is NoteStatus {
  return value !== null && (VALID_STATUSES as readonly string[]).includes(value);
}

/**
 * GET /api/notes
 * Query params:
 *   - status: "published" | "draft" | "unpublished" (admin only sees non-published)
 *   - category: category slug
 *   - search: free text search on title/description
 *   - tag: tag slug filter
 */
export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const statusParam = searchParams.get("status");
    const categorySlug = searchParams.get("category");
    const search = searchParams.get("search");
    const tagSlug = searchParams.get("tag");

    // Determine if the visitor is an admin (can see drafts/unpublished)
    const currentUser = await getSessionUser();
    const isAdmin = currentUser?.role === "ADMIN";

    // Build the where clause
    const where: Record<string, unknown> = {};

    if (statusParam) {
      // e.g. ?status=published -> status: "PUBLISHED"
      const normalized = statusParam.toUpperCase();
      if (isValidStatus(normalized)) {
        where.status = normalized;
      } else if (statusParam.toLowerCase() === "all" && isAdmin) {
        // admin can request everything
      } else {
        // unknown status filter -> default to published for visitors
        where.status = "PUBLISHED";
      }
    } else if (!isAdmin) {
      // Non-admins without a status filter only see published notes
      where.status = "PUBLISHED";
    }

    if (categorySlug) {
      where.category = { slug: categorySlug };
    }

    if (tagSlug) {
      where.tags = { some: { slug: tagSlug } };
    }

    if (search) {
      where.OR = [
        { title: { contains: search } },
        { description: { contains: search } },
      ];
    }

    const notes = await db.note.findMany({
      where,
      orderBy: [
        { publishedAt: "desc" },
        { createdAt: "desc" },
      ],
      include: {
        category: { select: { id: true, name: true, slug: true } },
        tags: { select: { id: true, name: true, slug: true } },
      },
    });

    return NextResponse.json({ notes });
  } catch (err) {
    const message =
      err instanceof Error ? err.message : "Failed to fetch notes.";
    return NextResponse.json(
      { error: message, notes: [] },
      { status: 500 }
    );
  }
}

interface CreateNoteBody {
  title?: string;
  slug?: string;
  description?: string;
  contentPath?: string;
  assetsPath?: string;
  status?: string;
  categoryId?: string;
  tags?: string[]; // tag names or slugs
  publishedAt?: string;
}

/**
 * POST /api/notes (admin only)
 * Creates a new note with metadata.
 */
export async function POST(request: NextRequest) {
  try {
    await requireAdmin();

    const body = (await request.json()) as CreateNoteBody;
    const title = body.title?.trim();
    if (!title) {
      return NextResponse.json(
        { success: false, error: "Title is required." },
        { status: 400 }
      );
    }
    if (!body.contentPath) {
      return NextResponse.json(
        { success: false, error: "contentPath is required." },
        { status: 400 }
      );
    }
    if (!body.categoryId) {
      return NextResponse.json(
        { success: false, error: "categoryId is required." },
        { status: 400 }
      );
    }

    const category = await db.category.findUnique({
      where: { id: body.categoryId },
    });
    if (!category) {
      return NextResponse.json(
        { success: false, error: "Category not found." },
        { status: 404 }
      );
    }

    const slug = body.slug?.trim() ? slugify(body.slug) : slugify(title);

    // Make sure slug is unique
    const existing = await db.note.findUnique({ where: { slug } });
    if (existing) {
      return NextResponse.json(
        { success: false, error: "A note with that slug already exists." },
        { status: 409 }
      );
    }

    let status: NoteStatus = "DRAFT";
    if (body.status && isValidStatus(body.status.toUpperCase())) {
      status = body.status.toUpperCase();
    }

    let publishedAt: Date | null = null;
    if (body.publishedAt) {
      const parsed = new Date(body.publishedAt);
      if (!isNaN(parsed.getTime())) publishedAt = parsed;
    }
    if (status === "PUBLISHED" && !publishedAt) {
      publishedAt = new Date();
    }

    // Resolve tags (by name or slug)
    const tagNames = (body.tags ?? []).map((t) => t.trim()).filter(Boolean);
    const tags = tagNames.length
      ? await db.tag.findMany({
          where: { OR: [{ name: { in: tagNames } }, { slug: { in: tagNames.map(slugify) } }] },
        })
      : [];

    // Create any tags that don't yet exist
    const missingTagInputs = tagNames.filter(
      (t) =>
        !tags.some(
          (existingTag) =>
            existingTag.name === t || existingTag.slug === slugify(t)
        )
    );

    const newTags = await Promise.all(
      missingTagInputs.map((name) =>
        db.tag.create({ data: { name, slug: slugify(name) } })
      )
    );
    const allTags = [...tags, ...newTags];

    const note = await db.note.create({
      data: {
        title,
        slug,
        description: body.description?.trim() || null,
        contentPath: body.contentPath.trim(),
        assetsPath: body.assetsPath?.trim() || null,
        status,
        categoryId: body.categoryId,
        publishedAt,
        tags: { connect: allTags.map((t) => ({ id: t.id })) },
      },
      include: {
        category: { select: { id: true, name: true, slug: true } },
        tags: { select: { id: true, name: true, slug: true } },
      },
    });

    return NextResponse.json({ success: true, note }, { status: 201 });
  } catch (err) {
    const message =
      err instanceof Error ? err.message : "Failed to create note.";
    const status = err instanceof AuthError ? err.statusCode : 500;
    return NextResponse.json(
      { success: false, error: message },
      { status }
    );
  }
}
