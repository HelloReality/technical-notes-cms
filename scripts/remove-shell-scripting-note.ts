/**
 * Remove the "Shell Scripting for DevOps Handbook" note (Instagram carousel
 * post DcaW1UljsVk) from the application database.
 *
 * Deletes the note + its version snapshots + view records (cascade).
 * Idempotent — exits cleanly if the note no longer exists.
 *
 * Run with: bun run scripts/remove-shell-scripting-note.ts
 */
import { db } from "@/lib/db";

const SLUG = "shell-scripting-for-devops-handbook";

async function main() {
  const note = await db.note.findUnique({
    where: { slug: SLUG },
    include: { tags: true, _count: { select: { versions: true, views: true } } },
  });

  if (!note) {
    console.log(`✓ No note found with slug "${SLUG}". Nothing to remove.`);
    return;
  }

  console.log(`✓ Found note:`);
  console.log(`  id: ${note.id}`);
  console.log(`  title: ${note.title}`);
  console.log(`  status: ${note.status}`);
  console.log(`  contentPath: ${note.contentPath}`);
  console.log(`  versions: ${note._count.versions}`);
  console.log(`  views: ${note._count.views}`);
  console.log(`  tags: ${note.tags.map((t) => t.name).join(", ")}`);

  // NoteVersion + NoteView have onDelete: Cascade in the schema, so Prisma
  // will drop them automatically when the note is deleted. The tag relations
  // (NoteTag join table) are also cleaned up automatically.
  await db.note.delete({ where: { id: note.id } });
  console.log(`✓ Note deleted (versions + views + tag links cascaded).`);
  console.log("");
  console.log("Done. The note no longer appears on the home page.");
}

main()
  .catch((e) => {
    console.error("✗ Failed:", e);
    process.exit(1);
  })
  .finally(async () => {
    await db.$disconnect();
  });
