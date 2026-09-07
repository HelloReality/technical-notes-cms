import { db } from "@/lib/db";
import type { SessionUser } from "@/lib/auth";

/**
 * Input for {@link createNoteVersionSnapshot}.
 * Mirrors the scalar fields of a Note plus its tag names.
 */
export interface NoteVersionSnapshotInput {
  noteId: string;
  title: string;
  slug: string;
  description: string | null;
  contentPath: string;
  assetsPath: string | null;
  status: string;
  categoryId: string;
  /** Tag names currently attached to the note. */
  tags: string[];
  /** Admin user who triggered the snapshot, if any. */
  user?: SessionUser | null;
}

/**
 * Persist a snapshot of a note's current state as a {@link NoteVersion} row.
 *
 * Used before every note update (PATCH) and before every version restore so
 * changes are reversible. SQLite has no native array type, so tags are
 * serialised to a JSON string in `tagsJson`.
 *
 * Callers are expected to wrap this in try/catch for best-effort semantics —
 * versioning should never block the underlying mutation.
 */
export async function createNoteVersionSnapshot(
  input: NoteVersionSnapshotInput,
) {
  return db.noteVersion.create({
    data: {
      noteId: input.noteId,
      title: input.title,
      slug: input.slug,
      description: input.description,
      contentPath: input.contentPath,
      assetsPath: input.assetsPath,
      status: input.status,
      categoryId: input.categoryId,
      tagsJson: JSON.stringify(input.tags),
      createdById: input.user?.id ?? null,
      createdByName: input.user?.name ?? null,
    },
  });
}

/**
 * Safely parse a `tagsJson` column into a list of tag names.
 * Returns an empty array on malformed input.
 */
export function parseTagsJson(tagsJson: string): string[] {
  try {
    const parsed: unknown = JSON.parse(tagsJson);
    if (Array.isArray(parsed)) {
      return parsed.filter(
        (t): t is string => typeof t === "string" && t.length > 0,
      );
    }
  } catch {
    /* fallthrough */
  }
  return [];
}
