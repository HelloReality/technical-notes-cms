/**
 * Insert the Shell Scripting for DevOps carousel (Instagram post DcaW1UljsVk)
 * as a new PUBLISHED note in the application database.
 *
 * Run with: bun run scripts/seed-shell-scripting-note.ts
 */
import { db } from "@/lib/db";
import { createNoteVersionSnapshot } from "@/lib/versioning";

const POST_ID = "DcaW1UljsVk";
const SLUG = "shell-scripting-for-devops-handbook";
const TITLE = "Shell Scripting for DevOps Handbook";
const DESCRIPTION =
  "A 20-page Instagram carousel covering shell scripting fundamentals for DevOps — from shebang and variables to loops, functions, text processing, cron scheduling, and CI/CD integration. Built for complete beginners.";
const CONTENT_PATH = `/uploads/instagram-carousel-${POST_ID}.html`;
const ASSETS_PATH = `/uploads/instagram-carousel-${POST_ID}`;
const CATEGORY_SLUG = "devops";
const TAG_NAMES = [
  "Shell Scripting",
  "Bash",
  "DevOps",
  "Automation",
  "Linux",
  "CLI",
];

async function main() {
  // 1. Find the DevOps category.
  const category = await db.category.findUnique({
    where: { slug: CATEGORY_SLUG },
  });
  if (!category) {
    throw new Error(`Category "${CATEGORY_SLUG}" not found.`);
  }
  console.log(`✓ Category: ${category.name} (${category.id})`);

  // 2. Idempotency — skip if the note already exists (by slug).
  const existing = await db.note.findUnique({ where: { slug: SLUG } });
  if (existing) {
    console.log(`✓ Note already exists (id=${existing.id}), skipping insert.`);
    console.log(`  Status: ${existing.status}`);
    console.log(`  Content path: ${existing.contentPath}`);
    return;
  }

  // 3. Ensure tags exist (create missing ones).
  const tagRecords = await Promise.all(
    TAG_NAMES.map((name) =>
      db.tag.upsert({
        where: { slug: name.toLowerCase().replace(/\s+/g, "-") },
        update: {},
        create: {
          name,
          slug: name.toLowerCase().replace(/\s+/g, "-"),
        },
      }),
    ),
  );
  console.log(`✓ Tags: ${tagRecords.map((t) => t.name).join(", ")}`);

  // 4. Create the note (PUBLISHED).
  const note = await db.note.create({
    data: {
      title: TITLE,
      slug: SLUG,
      description: DESCRIPTION,
      contentPath: CONTENT_PATH,
      assetsPath: ASSETS_PATH,
      status: "PUBLISHED",
      categoryId: category.id,
      publishedAt: new Date(),
      tags: {
        connect: tagRecords.map((t) => ({ id: t.id })),
      },
    },
    include: { tags: true, category: true },
  });
  console.log(`✓ Note created: id=${note.id}`);
  console.log(`  Title: ${note.title}`);
  console.log(`  Slug: ${note.slug}`);
  console.log(`  Status: ${note.status}`);
  console.log(`  Content path: ${note.contentPath}`);
  console.log(`  Tags: ${note.tags.map((t) => t.name).join(", ")}`);

  // 5. Create an initial version snapshot (matches the app's pattern).
  await createNoteVersionSnapshot({
    noteId: note.id,
    title: note.title,
    slug: note.slug,
    description: note.description,
    contentPath: note.contentPath,
    assetsPath: note.assetsPath ?? null,
    status: note.status,
    categoryId: note.categoryId,
    tags: note.tags.map((t) => t.name),
    user: null,
  });
  console.log(`✓ Version snapshot created.`);
  console.log("");
  console.log("Done. The note is now live at / (Latest notes section).");
}

main()
  .catch((e) => {
    console.error("✗ Failed:", e);
    process.exit(1);
  })
  .finally(async () => {
    await db.$disconnect();
  });
