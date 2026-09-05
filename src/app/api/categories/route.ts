import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { requireAdmin, AuthError } from "@/lib/auth";
import { slugify } from "@/lib/utils";

export const dynamic = "force-dynamic";

/**
 * GET /api/categories
 * Returns all categories with their nested children.
 */
export async function GET() {
  try {
    // Top-level categories with their immediate children
    const categories = await db.category.findMany({
      where: { parentId: null },
      orderBy: { name: "asc" },
      include: {
        children: {
          orderBy: { name: "asc" },
        },
        _count: { select: { notes: true } },
      },
    });

    return NextResponse.json({ categories });
  } catch (err) {
    const message =
      err instanceof Error ? err.message : "Failed to fetch categories.";
    return NextResponse.json(
      { error: message, categories: [] },
      { status: 500 }
    );
  }
}

interface CreateCategoryBody {
  name?: string;
  slug?: string;
  description?: string;
  parentId?: string;
}

/**
 * POST /api/categories (admin only)
 * Creates a new category.
 */
export async function POST(request: NextRequest) {
  try {
    await requireAdmin();

    const body = (await request.json()) as CreateCategoryBody;
    const name = body.name?.trim();
    if (!name) {
      return NextResponse.json(
        { success: false, error: "Name is required." },
        { status: 400 }
      );
    }

    const slug = body.slug?.trim() ? slugify(body.slug) : slugify(name);

    // Validate parentId if provided
    if (body.parentId) {
      const parent = await db.category.findUnique({
        where: { id: body.parentId },
      });
      if (!parent) {
        return NextResponse.json(
          { success: false, error: "Parent category not found." },
          { status: 404 }
        );
      }
    }

    const existing = await db.category.findFirst({
      where: {
        OR: [{ name }, { slug }],
      },
    });
    if (existing) {
      return NextResponse.json(
        {
          success: false,
          error: "A category with that name or slug already exists.",
        },
        { status: 409 }
      );
    }

    const category = await db.category.create({
      data: {
        name,
        slug,
        description: body.description?.trim() || null,
        parentId: body.parentId || null,
      },
    });

    return NextResponse.json({ success: true, category }, { status: 201 });
  } catch (err) {
    const message =
      err instanceof Error ? err.message : "Failed to create category.";
    const status = err instanceof AuthError ? err.statusCode : 500;
    return NextResponse.json(
      { success: false, error: message },
      { status }
    );
  }
}
