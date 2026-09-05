// Shared types for the Technical Notes CMS

export type NoteStatus = "DRAFT" | "PUBLISHED" | "UNPUBLISHED";
export type UserRole = "ADMIN" | "VISITOR";

export type ViewKey =
  | "public-home"
  | "admin-dashboard"
  | "note-viewer"
  | "search-results";

export interface Tag {
  id: string;
  name: string;
  slug: string;
}

export interface Category {
  id: string;
  name: string;
  slug: string;
  description?: string;
  parentId?: string | null;
  parent?: Category | null;
  children?: Category[];
  noteCount?: number;
}

export interface Note {
  id: string;
  title: string;
  slug: string;
  description?: string;
  contentPath: string;
  status: NoteStatus;
  categoryId: string;
  category?: Category;
  subcategoryId?: string | null;
  subcategory?: Category | null;
  tags?: Tag[];
  assetsPath?: string;
  createdAt: string;
  updatedAt: string;
  publishedAt?: string | null;
}

export interface SessionUser {
  id: string;
  email: string;
  name?: string;
  role: UserRole;
}

export interface Session {
  user: SessionUser;
}

export interface NoteInput {
  title: string;
  slug: string;
  description?: string;
  categoryId: string;
  subcategoryId?: string | null;
  tags?: string[];
  contentPath?: string;
  status?: NoteStatus;
}

export interface UploadResult {
  contentPath: string;
  assetsPath?: string;
  fileName: string;
  size: number;
}

// Curated default category list for the public homepage pills
export const DEFAULT_CATEGORY_PILLS: { name: string; slug: string }[] = [
  { name: "Cybersecurity", slug: "cybersecurity" },
  { name: "Development", slug: "development" },
  { name: "DevOps", slug: "devops" },
  { name: "Cloud", slug: "cloud" },
  { name: "Networking", slug: "networking" },
  { name: "Databases", slug: "databases" },
  { name: "AI / ML", slug: "ai-ml" },
  { name: "Web", slug: "web" },
];
