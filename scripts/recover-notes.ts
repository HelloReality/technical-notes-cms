/**
 * Re-seed the 4 original notes into the database after a sandbox refresh.
 *
 * Run with: bun run scripts/recover-notes.ts
 */
import { db } from "@/lib/db";
import { createNoteVersionSnapshot } from "@/lib/versioning";

interface NoteSpec {
  title: string;
  slug: string;
  description: string;
  contentPath: string;
  assetsPath?: string;
  categorySlug: string;
  tags: string[];
}

const NOTES: NoteSpec[] = [
  {
    title: "Linux Security Handbook",
    slug: "linux-security-handbook",
    description:
      "From Linux hardening to production security — 19 chapters covering users, permissions, SELinux, auditd, SSH, sudo, firewall, logging, and incident response.",
    contentPath: "/uploads/linux-security-handbook.html",
    categorySlug: "cybersecurity",
    tags: ["Linux", "Security", "Hardening", "SELinux", "Auditd"],
  },
  {
    title: "Linux for Complete Beginners",
    slug: "linux-for-complete-beginners",
    description:
      "A practical guide from zero to confident Linux user — 20 pages covering the terminal, file system, commands, permissions, processes, and shell basics.",
    contentPath: "/uploads/linux-for-beginners.html",
    categorySlug: "operating-systems",
    tags: ["Linux", "Beginners", "Terminal", "Shell"],
  },
  {
    title: "Instagram Carousel — 20 Pages",
    slug: "instagram-carousel-20-pages",
    description:
      "A 20-page Instagram carousel imported from post DcdSiAhFbh0 — notebook-style layout with each carousel image as a page.",
    contentPath: "/uploads/instagram-carousel-dcdsiahfbh0.html",
    assetsPath: "/uploads/instagram-carousel-DcdSiAhFbh0",
    categorySlug: "cybersecurity",
    tags: ["Instagram", "Carousel", "Linux"],
  },
  {
    title: "Shell Scripting for DevOps Handbook",
    slug: "shell-scripting-for-devops-handbook",
    description:
      "A 20-page Instagram carousel covering shell scripting fundamentals for DevOps — from shebang and variables to loops, functions, text processing, cron scheduling, and CI/CD integration. Built for complete beginners.",
    contentPath: "/uploads/instagram-carousel-DcaW1UljsVk.html",
    assetsPath: "/uploads/instagram-carousel-DcaW1UljsVk",
    categorySlug: "devops",
    tags: ["Shell Scripting", "Bash", "DevOps", "Automation", "Linux", "CLI"],
  },
];

async function main() {
  for (const spec of NOTES) {
    // Skip if note already exists (idempotent)
    const existing = await db.note.findUnique({ where: { slug: spec.slug } });
    if (existing) {
      console.log(`✓ [skip] ${spec.title} — already exists`);
      continue;
    }

    // Find category
    const category = await db.category.findUnique({
      where: { slug: spec.categorySlug },
    });
    if (!category) {
      console.log(`✗ [error] Category "${spec.categorySlug}" not found for "${spec.title}"`);
      continue;
    }

    // Ensure tags exist
    const tagRecords = await Promise.all(
      spec.tags.map((name) =>
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

    // Create note
    const note = await db.note.create({
      data: {
        title: spec.title,
        slug: spec.slug,
        description: spec.description,
        contentPath: spec.contentPath,
        assetsPath: spec.assetsPath ?? null,
        status: "PUBLISHED",
        categoryId: category.id,
        publishedAt: new Date(),
        tags: { connect: tagRecords.map((t) => ({ id: t.id })) },
      },
      include: { tags: true },
    });

    // Create version snapshot
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

    console.log(`✓ [created] ${spec.title} (id=${note.id})`);
  }

  // Summary
  const totalNotes = await db.note.count();
  console.log(`\nDone. ${totalNotes} notes in database.`);
}

main()
  .catch((e) => {
    console.error("✗ Failed:", e);
    process.exit(1);
  })
  .finally(async () => {
    await db.$disconnect();
  });
