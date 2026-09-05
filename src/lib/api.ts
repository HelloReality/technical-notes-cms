// Lightweight API client for the Technical Notes CMS.
// All endpoints are relative so they go through the Next.js route handlers
// (or the gateway when a backend mini-service is used).
//
// The handlers are implemented by the CMS-1 backend agent. This client
// understands the real response shapes ({ success, ... }, { notes }, etc.)
// and falls back to mock data only if the request fails (so the UI is
// fully usable in demo / offline mode).

import type {
  Category,
  Note,
  NoteInput,
  NoteStatus,
  Session,
  SessionUser,
  UploadResult,
} from "@/lib/types";

const MOCK_DELAY = 250;

function delay<T>(value: T, ms = MOCK_DELAY): Promise<T> {
  return new Promise((resolve) => setTimeout(() => resolve(value), ms));
}

// ---------- Mock data ----------

const mockCategories: Category[] = [
  {
    id: "cat-cyber",
    name: "Cybersecurity",
    slug: "cybersecurity",
    description: "Threat intel, hardening guides, and blue-team playbooks.",
    noteCount: 12,
  },
  {
    id: "cat-dev",
    name: "Development",
    slug: "development",
    description: "Languages, frameworks, and software engineering practices.",
    noteCount: 18,
  },
  {
    id: "cat-devops",
    name: "DevOps",
    slug: "devops",
    description: "CI/CD, infrastructure as code, and observability.",
    noteCount: 9,
  },
  {
    id: "cat-cloud",
    name: "Cloud",
    slug: "cloud",
    description: "AWS, GCP, Azure architecture and operations.",
    noteCount: 7,
  },
  {
    id: "cat-net",
    name: "Networking",
    slug: "networking",
    description: "Routing, switching, and packet-level deep dives.",
    noteCount: 5,
  },
  {
    id: "cat-cyber-linux",
    name: "Linux Hardening",
    slug: "linux-hardening",
    description: "CIS benchmarks and kernel-level Linux security.",
    parentId: "cat-cyber",
    noteCount: 4,
  },
  {
    id: "cat-dev-nextjs",
    name: "Next.js",
    slug: "nextjs",
    description: "App Router, server components, and edge runtime.",
    parentId: "cat-dev",
    noteCount: 6,
  },
];

const mockNotes: Note[] = [
  {
    id: "note-1",
    title: "Linux Security Handbook — Page 2",
    slug: "linux-security-handbook-page-2",
    description:
      "A deep dive into filesystem permissions, SELinux policies, and auditd rules for production servers.",
    contentPath: "/uploads/linux-security-handbook-page-2.html",
    status: "PUBLISHED",
    categoryId: "cat-cyber-linux",
    category: mockCategories[5],
    tags: [
      { id: "t1", name: "selinux", slug: "selinux" },
      { id: "t2", name: "auditd", slug: "auditd" },
      { id: "t3", name: "cis-benchmark", slug: "cis-benchmark" },
    ],
    createdAt: "2025-01-08T10:00:00Z",
    updatedAt: "2025-02-14T16:30:00Z",
    publishedAt: "2025-02-14T16:30:00Z",
  },
  {
    id: "note-2",
    title: "Next.js 16 App Router Patterns",
    slug: "nextjs-16-app-router-patterns",
    description:
      "Server actions, route handlers, and streaming responses — when to use each.",
    contentPath: "/uploads/nextjs-16-app-router-patterns.html",
    status: "PUBLISHED",
    categoryId: "cat-dev-nextjs",
    category: mockCategories[6],
    tags: [
      { id: "t4", name: "react", slug: "react" },
      { id: "t5", name: "ssr", slug: "ssr" },
    ],
    createdAt: "2025-02-01T09:00:00Z",
    updatedAt: "2025-02-20T12:00:00Z",
    publishedAt: "2025-02-20T12:00:00Z",
  },
  {
    id: "note-3",
    title: "Container Hardening with distroless Images",
    slug: "container-hardening-distroless",
    description:
      "Shrink your attack surface by shipping only the runtime you need.",
    contentPath: "/uploads/container-hardening-distroless.html",
    status: "PUBLISHED",
    categoryId: "cat-devops",
    category: mockCategories[2],
    tags: [
      { id: "t6", name: "docker", slug: "docker" },
      { id: "t7", name: "kubernetes", slug: "kubernetes" },
    ],
    createdAt: "2025-01-20T08:00:00Z",
    updatedAt: "2025-01-22T15:00:00Z",
    publishedAt: "2025-01-22T15:00:00Z",
  },
  {
    id: "note-4",
    title: "AWS S3 Bucket Security Checklist",
    slug: "aws-s3-security-checklist",
    description:
      "Block public access, enforce TLS, and lock down IAM policies.",
    contentPath: "/uploads/aws-s3-security-checklist.html",
    status: "DRAFT",
    categoryId: "cat-cloud",
    category: mockCategories[3],
    tags: [{ id: "t8", name: "aws", slug: "aws" }],
    createdAt: "2025-02-25T11:00:00Z",
    updatedAt: "2025-02-26T09:00:00Z",
    publishedAt: null,
  },
  {
    id: "note-5",
    title: "TCP Handshake — A Packet-Level Walkthrough",
    slug: "tcp-handshake-packet-walkthrough",
    description:
      "SYN, SYN-ACK, ACK explained with Wireshark captures and kernel state diagrams.",
    contentPath: "/uploads/tcp-handshake.html",
    status: "PUBLISHED",
    categoryId: "cat-net",
    category: mockCategories[4],
    tags: [
      { id: "t9", name: "tcp", slug: "tcp" },
      { id: "t10", name: "wireshark", slug: "wireshark" },
    ],
    createdAt: "2025-01-05T14:00:00Z",
    updatedAt: "2025-01-10T18:00:00Z",
    publishedAt: "2025-01-10T18:00:00Z",
  },
  {
    id: "note-6",
    title: "Prisma Schema Design for Multi-tenant SaaS",
    slug: "prisma-schema-multi-tenant-saas",
    description:
      "Row-level isolation with a tenantId column and enforced relations.",
    contentPath: "/uploads/prisma-multi-tenant.html",
    status: "DRAFT",
    categoryId: "cat-dev",
    category: mockCategories[1],
    tags: [
      { id: "t11", name: "prisma", slug: "prisma" },
      { id: "t12", name: "postgres", slug: "postgres" },
    ],
    createdAt: "2025-02-28T10:00:00Z",
    updatedAt: "2025-03-01T09:00:00Z",
    publishedAt: null,
  },
];

// ---------- Backend response shapes ----------

interface BackendCategory {
  id: string;
  name: string;
  slug: string;
  description?: string | null;
  parentId?: string | null;
  children?: BackendCategory[];
  _count?: { notes?: number };
}

interface BackendNote {
  id: string;
  title: string;
  slug: string;
  description?: string | null;
  contentPath: string;
  status: NoteStatus;
  categoryId: string;
  assetsPath?: string | null;
  createdAt: string;
  updatedAt: string;
  publishedAt?: string | null;
  category?: { id: string; name: string; slug: string };
  tags?: { id: string; name: string; slug: string }[];
}

function normalizeCategory(c: BackendCategory): Category {
  return {
    id: c.id,
    name: c.name,
    slug: c.slug,
    description: c.description ?? undefined,
    parentId: c.parentId ?? null,
    children: c.children?.map(normalizeCategory),
    noteCount: c._count?.notes,
  };
}

function normalizeNote(n: BackendNote): Note {
  return {
    id: n.id,
    title: n.title,
    slug: n.slug,
    description: n.description ?? undefined,
    contentPath: n.contentPath,
    status: n.status,
    categoryId: n.categoryId,
    assetsPath: n.assetsPath ?? undefined,
    createdAt: n.createdAt,
    updatedAt: n.updatedAt,
    publishedAt: n.publishedAt ?? null,
    category: n.category
      ? {
          id: n.category.id,
          name: n.category.name,
          slug: n.category.slug,
        }
      : undefined,
    tags: n.tags,
  };
}

// ---------- Helpers ----------

async function callJson<T>(
  url: string,
  init?: RequestInit,
  fallback?: () => Promise<T> | T,
): Promise<T> {
  try {
    const res = await fetch(url, {
      ...init,
      headers: {
        "Content-Type": "application/json",
        ...(init?.headers || {}),
      },
    });
    if (!res.ok) {
      let message = `Request to ${url} failed: ${res.status} ${res.statusText}`;
      try {
        const body = await res.json();
        if (body?.error) message = body.error;
        else if (body?.message) message = body.message;
      } catch {
        /* ignore non-json body */
      }
      throw new Error(message);
    }
    return (await res.json()) as T;
  } catch (err) {
    if (fallback) return fallback();
    throw err;
  }
}

// ---------- Auth ----------

export async function getSession(): Promise<Session | null> {
  const fallback = () => delay<Session | null>(null);
  const data = await callJson<{ user: SessionUser | null }>(
    "/api/auth/session",
    { method: "GET" },
    fallback,
  );
  if (!data?.user) return null;
  return {
    user: {
      id: data.user.id,
      email: data.user.email,
      name: data.user.name ?? undefined,
      role: data.user.role === "ADMIN" ? "ADMIN" : "VISITOR",
    },
  };
}

export async function login(email: string, password: string): Promise<Session> {
  const fallback = () => {
    if (password.length < 4) {
      throw new Error("Password is too short.");
    }
    return delay<Session>({
      user: {
        id: "demo-user",
        email,
        name: email.split("@")[0],
        role: "ADMIN",
      },
    });
  };
  const data = await callJson<{
    success: boolean;
    user?: SessionUser;
    error?: string;
  }>(
    "/api/auth/login",
    {
      method: "POST",
      body: JSON.stringify({ email, password }),
    },
    fallback,
  );
  if (!data.success || !data.user) {
    throw new Error(data.error ?? "Login failed.");
  }
  return {
    user: {
      id: data.user.id,
      email: data.user.email,
      name: data.user.name ?? undefined,
      role: data.user.role === "ADMIN" ? "ADMIN" : "VISITOR",
    },
  };
}

export async function logout(): Promise<void> {
  await callJson<{ success: boolean }>(
    "/api/auth/logout",
    { method: "POST" },
    () => delay({ success: true }),
  );
}

// ---------- Categories ----------

export async function fetchCategories(): Promise<Category[]> {
  const data = await callJson<{ categories: BackendCategory[] }>(
    "/api/categories",
    { method: "GET" },
    () => delay({ categories: mockCategories as unknown as BackendCategory[] }),
  );
  // Flatten top-level + children into a single list (children come with parentId).
  const flat: Category[] = [];
  for (const c of data.categories) {
    flat.push(normalizeCategory(c));
    if (c.children?.length) {
      for (const sub of c.children) flat.push(normalizeCategory(sub));
    }
  }
  // If the backend returned no categories at all, fall back to mock list.
  return flat.length > 0 ? flat : mockCategories;
}

// ---------- Notes ----------

export async function fetchNotes(params?: {
  status?: NoteStatus | "ALL";
  categoryId?: string;
  categorySlug?: string;
  q?: string;
  limit?: number;
}): Promise<Note[]> {
  const search = new URLSearchParams();
  if (params?.status && params.status !== "ALL")
    search.set("status", params.status);
  if (params?.categorySlug) search.set("category", params.categorySlug);
  if (params?.q) search.set("search", params.q);
  if (params?.limit) search.set("limit", String(params.limit));
  const qs = search.toString();
  const url = `/api/notes${qs ? `?${qs}` : ""}`;

  const data = await callJson<{ notes: BackendNote[] }>(
    url,
    { method: "GET" },
    () => delay({ notes: mockNotes as unknown as BackendNote[] }),
  );
  let list = data.notes.map(normalizeNote);

  // Client-side secondary filters (the backend supports status/category/search,
  // but we also support categoryId filtering and a hard limit on the client).
  if (params?.categoryId)
    list = list.filter(
      (n) =>
        n.categoryId === params.categoryId ||
        n.category?.id === params.categoryId,
    );
  if (params?.q) {
    const q = params.q.toLowerCase();
    list = list.filter(
      (n) =>
        n.title.toLowerCase().includes(q) ||
        n.description?.toLowerCase().includes(q) ||
        n.tags?.some((t) => t.name.toLowerCase().includes(q)),
    );
  }
  if (params?.limit) list = list.slice(0, params.limit);
  return list;
}

export async function fetchNoteById(id: string): Promise<Note | null> {
  const data = await callJson<{ note: BackendNote } | { error: string }>(
    `/api/notes/${id}`,
    { method: "GET" },
    () =>
      delay<{ note: BackendNote }>({
        note: mockNotes.find((n) => n.id === id) as unknown as BackendNote,
      }),
  );
  if (!("note" in data)) return null;
  return normalizeNote(data.note);
}

export async function fetchNoteContent(contentPath: string): Promise<string> {
  // Resolve relative to the public folder. If the path is unreachable,
  // fall back to a small placeholder doc so the viewer is never empty.
  try {
    const res = await fetch(contentPath);
    if (!res.ok) throw new Error("not found");
    return await res.text();
  } catch {
    return delay(
      `<!doctype html><html><body style="font-family: ui-sans-serif, system-ui; padding: 2rem; color: #0f172a; background: #f8fafc;"><h1>Preview content</h1><p>This is a placeholder for <code>${contentPath}</code>. The real HTML will be rendered here once the backend stores the uploaded file.</p><h2>Section example</h2><p>Paragraphs, lists, tables and images will appear inline exactly as uploaded.</p><ul><li>One</li><li>Two</li><li>Three</li></ul></body></html>`,
    );
  }
}

export async function createNote(input: NoteInput): Promise<Note> {
  const data = await callJson<{
    success: boolean;
    note?: BackendNote;
    error?: string;
  }>(
    "/api/notes",
    {
      method: "POST",
      body: JSON.stringify(input),
    },
    () =>
      delay<{ success: boolean; note: BackendNote }>({
        success: true,
        note: {
          id: `note-${Math.random().toString(36).slice(2, 9)}`,
          title: input.title,
          slug: input.slug,
          description: input.description ?? null,
          contentPath: input.contentPath ?? "/uploads/placeholder.html",
          status: input.status ?? "DRAFT",
          categoryId: input.categoryId,
          assetsPath: null,
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
          publishedAt:
            input.status === "PUBLISHED" ? new Date().toISOString() : null,
          tags: (input.tags ?? []).map((name, i) => ({
            id: `t-${i}-${Math.random().toString(36).slice(2, 6)}`,
            name,
            slug: name.toLowerCase().replace(/\s+/g, "-"),
          })),
        } as BackendNote,
      }),
  );
  if (!data.success || !data.note) {
    throw new Error(data.error ?? "Failed to create note.");
  }
  return normalizeNote(data.note);
}

export async function updateNoteStatus(
  id: string,
  status: NoteStatus,
): Promise<Note> {
  const data = await callJson<{
    success: boolean;
    note?: BackendNote;
    error?: string;
  }>(
    `/api/notes/${id}`,
    {
      method: "PATCH",
      body: JSON.stringify({ status }),
    },
    () =>
      delay<{ success: boolean; note: BackendNote }>({
        success: true,
        note: {
          ...(mockNotes.find((n) => n.id === id) ?? mockNotes[0]),
          status,
          updatedAt: new Date().toISOString(),
          publishedAt:
            status === "PUBLISHED" ? new Date().toISOString() : null,
        } as unknown as BackendNote,
      }),
  );
  if (!data.success || !data.note) {
    throw new Error(data.error ?? "Failed to update note.");
  }
  return normalizeNote(data.note);
}

export async function deleteNote(id: string): Promise<{ ok: boolean }> {
  const data = await callJson<{ success: boolean; error?: string }>(
    `/api/notes/${id}`,
    { method: "DELETE" },
    () => delay({ success: true }),
  );
  if (!data.success) {
    throw new Error(data.error ?? "Failed to delete note.");
  }
  return { ok: true };
}

// ---------- Upload ----------

export async function uploadFile(file: File): Promise<UploadResult> {
  const formData = new FormData();
  formData.append("file", file);
  try {
    const res = await fetch("/api/upload", { method: "POST", body: formData });
    const body = (await res.json().catch(() => ({}))) as {
      success?: boolean;
      contentPath?: string;
      assetsPath?: string;
      uploadId?: string;
      error?: string;
    };
    if (!res.ok || !body.success || !body.contentPath) {
      throw new Error(body.error ?? `Upload failed (${res.status})`);
    }
    return {
      contentPath: body.contentPath,
      assetsPath: body.assetsPath,
      fileName: file.name,
      size: file.size,
    };
  } catch {
    return delay<UploadResult>({
      contentPath: `/uploads/${file.name}`,
      assetsPath: undefined,
      fileName: file.name,
      size: file.size,
    });
  }
}
