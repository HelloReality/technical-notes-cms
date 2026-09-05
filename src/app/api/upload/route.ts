import { NextRequest, NextResponse } from "next/server";
import { randomUUID } from "crypto";
import path from "path";
import fs from "fs/promises";
import { existsSync } from "fs";
import AdmZip from "adm-zip";
import { requireAdmin, AuthError } from "@/lib/auth";

export const dynamic = "force-dynamic";

const UPLOAD_ROOT = path.join(process.cwd(), "public", "uploads");
const PUBLIC_PREFIX = "/uploads";

/**
 * Recursively locate the first index.html in a directory tree.
 */
async function findIndexHtml(dir: string): Promise<string | null> {
  const entries = await fs.readdir(dir, { withFileTypes: true });
  // Prefer a top-level index.html
  for (const entry of entries) {
    if (entry.isFile() && entry.name.toLowerCase() === "index.html") {
      return path.join(dir, entry.name);
    }
  }
  // Then search subdirectories
  for (const entry of entries) {
    if (entry.isDirectory()) {
      const found = await findIndexHtml(path.join(dir, entry.name));
      if (found) return found;
    }
  }
  return null;
}

/**
 * Normalise a filesystem path so it points to the URL-friendly relative
 * location under /uploads.
 */
function toPublicPath(absPath: string): string {
  const rel = path.relative(path.join(process.cwd(), "public"), absPath);
  // Use forward slashes for URLs
  return `/${rel.split(path.sep).join("/")}`;
}

/**
 * POST /api/upload (admin only)
 * Accepts a FormData upload with a single `file` field.
 * - If the file is a ZIP, extracts it to /public/uploads/{id}/
 * - Otherwise saves the file directly to /public/uploads/{id}/{filename}
 * Returns { success, contentPath, assetsPath }
 *  - contentPath: public URL of the index.html (or saved file)
 *  - assetsPath: public URL of the directory containing the assets (or null)
 */
export async function POST(request: NextRequest) {
  try {
    await requireAdmin();

    const formData = await request.formData();
    const file = formData.get("file");

    if (!file || !(file instanceof File)) {
      return NextResponse.json(
        { success: false, error: "No file provided in 'file' field." },
        { status: 400 }
      );
    }

    // Ensure upload root exists
    await fs.mkdir(UPLOAD_ROOT, { recursive: true });

    const uploadId = randomUUID();
    const targetDir = path.join(UPLOAD_ROOT, uploadId);
    await fs.mkdir(targetDir, { recursive: true });

    const originalName = file.name || "upload.bin";
    const buffer = Buffer.from(await file.arrayBuffer());
    const isZip =
      originalName.toLowerCase().endsWith(".zip") ||
      buffer.length >= 4 &&
        buffer[0] === 0x50 &&
        buffer[1] === 0x4b &&
        (buffer[2] === 0x03 || buffer[2] === 0x05 || buffer[2] === 0x07);

    if (isZip) {
      // Write the zip to a temp file then extract
      const tempZipPath = path.join(targetDir, "__upload.zip");
      await fs.writeFile(tempZipPath, buffer);

      try {
        const zip = new AdmZip(tempZipPath);
        zip.extractAllTo(targetDir, true);
      } finally {
        // Remove the zip after extraction
        if (existsSync(tempZipPath)) {
          await fs.unlink(tempZipPath).catch(() => undefined);
        }
      }

      // Find the index.html
      const indexHtmlAbs = await findIndexHtml(targetDir);
      if (!indexHtmlAbs) {
        return NextResponse.json(
          {
            success: false,
            error:
              "ZIP extracted but no index.html was found inside the archive.",
            assetsPath: toPublicPath(targetDir),
          },
          { status: 422 }
        );
      }

      return NextResponse.json({
        success: true,
        contentPath: toPublicPath(indexHtmlAbs),
        assetsPath: toPublicPath(targetDir),
        uploadId,
      });
    }

    // Non-zip: save the single file
    const safeName = originalName.replace(/[^a-zA-Z0-9._-]+/g, "_");
    const savedAbs = path.join(targetDir, safeName);
    await fs.writeFile(savedAbs, buffer);

    return NextResponse.json({
      success: true,
      contentPath: toPublicPath(savedAbs),
      assetsPath: toPublicPath(targetDir),
      uploadId,
    });
  } catch (err) {
    const message =
      err instanceof Error ? err.message : "Upload failed.";
    const status = err instanceof AuthError ? err.statusCode : 500;
    return NextResponse.json(
      { success: false, error: message },
      { status }
    );
  }
}
