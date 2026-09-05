/**
 * Seed script for the Technical Notes CMS.
 *
 * Usage: bun run scripts/seed.ts
 *
 * Reads ADMIN_EMAIL and ADMIN_PASSWORD from environment (or .env) and:
 *   1. Creates (or updates) the admin user with a hashed password.
 *   2. Seeds the default categories.
 *
 * Existing data is upserted, so this script is safe to run repeatedly.
 */

import { PrismaClient } from "@prisma/client";
import bcrypt from "bcryptjs";
import path from "path";

// Load env vars from .env if running standalone
async function loadEnv() {
  try {
    const fs = await import("fs/promises");
    const envPath = path.join(process.cwd(), ".env");
    const contents = await fs.readFile(envPath, "utf8");
    for (const rawLine of contents.split("\n")) {
      const line = rawLine.trim();
      if (!line || line.startsWith("#")) continue;
      const eq = line.indexOf("=");
      if (eq === -1) continue;
      const key = line.slice(0, eq).trim();
      const value = line.slice(eq + 1).trim().replace(/^["']|["']$/g, "");
      if (!(key in process.env)) {
        process.env[key] = value;
      }
    }
  } catch {
    // ignore: .env might not exist in some environments
  }
}

const prisma = new PrismaClient();

const DEFAULT_CATEGORIES: { name: string; description?: string }[] = [
  { name: "Cybersecurity", description: "Security concepts, threats, defense, and best practices." },
  { name: "Development", description: "Software development practices, patterns, and methodologies." },
  { name: "DevOps", description: "CI/CD, automation, infrastructure as code, and operations." },
  { name: "Cloud", description: "Cloud platforms, services, and architecture patterns." },
  { name: "AI & Machine Learning", description: "Artificial intelligence, ML models, training, and inference." },
  { name: "Networking", description: "Network protocols, routing, security, and infrastructure." },
  { name: "Databases", description: "Relational, NoSQL, and other data storage systems." },
  { name: "Operating Systems", description: "Linux, Windows, and other operating system internals." },
  { name: "System Design", description: "Distributed systems, scalability, and architecture design." },
  { name: "Programming Languages", description: "Languages, syntax, idioms, and runtimes." },
  { name: "Tools", description: "Developer tools, CLIs, editors, and productivity software." },
];

function slugify(input: string): string {
  return input
    .toString()
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9\s-]/g, "")
    .replace(/[\s_-]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

async function seedAdmin() {
  const email = (process.env.ADMIN_EMAIL || "admin@notes.local").trim().toLowerCase();
  const password = process.env.ADMIN_PASSWORD || "Admin@2026";

  if (!password) {
    throw new Error("ADMIN_PASSWORD environment variable must be set.");
  }

  const hashed = await bcrypt.hash(password, 10);

  const user = await prisma.user.upsert({
    where: { email },
    update: { password: hashed, role: "ADMIN" },
    create: {
      email,
      name: "Administrator",
      role: "ADMIN",
      password: hashed,
    },
  });

  console.log(`[seed] Admin user ready: ${user.email} (id=${user.id})`);
  return user;
}

async function seedCategories() {
  let createdCount = 0;
  let updatedCount = 0;

  for (const cat of DEFAULT_CATEGORIES) {
    const slug = slugify(cat.name);
    const existing = await prisma.category.findUnique({ where: { slug } });

    if (existing) {
      await prisma.category.update({
        where: { slug },
        data: {
          name: cat.name,
          description: cat.description ?? null,
        },
      });
      updatedCount++;
    } else {
      await prisma.category.create({
        data: {
          name: cat.name,
          slug,
          description: cat.description ?? null,
        },
      });
      createdCount++;
    }
  }

  console.log(
    `[seed] Categories ready: ${createdCount} created, ${updatedCount} updated (${DEFAULT_CATEGORIES.length} total).`
  );
}

async function main() {
  await loadEnv();
  console.log("[seed] Starting seed...");
  await seedAdmin();
  await seedCategories();
  console.log("[seed] Done.");
}

main()
  .catch((err) => {
    console.error("[seed] Error:", err);
    process.exitCode = 1;
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
