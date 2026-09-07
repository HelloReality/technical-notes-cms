"use client";

import { create } from "zustand";
import type {
  Category,
  Note,
  NoteStatus,
  NoteVersion,
  ScheduledPublish,
  NoteView,
  BulkAction,
  BulkResult,
  Session,
  SessionUser,
  ViewKey,
} from "@/lib/types";
import * as api from "@/lib/api";

/**
 * Enrich a list of notes with parent-category information using the full
 * categories tree. The backend's `/api/notes` response only includes the
 * immediate category as `{ id, name, slug }` (no parentId), so we look up
 * the parent here so the UI can render "Top Category › Subcategory".
 */
function enrichNotes(notes: Note[], categories: Category[]): Note[] {
  const byId = new Map<string, Category>();
  for (const c of categories) byId.set(c.id, c);
  return notes.map((n) => {
    const cat = n.category && byId.get(n.category.id);
    if (cat && cat.parentId) {
      const parent = byId.get(cat.parentId);
      if (parent) {
        return { ...n, category: { ...parent }, subcategory: cat };
      }
    }
    return n;
  });
}

interface AppState {
  // View routing
  view: ViewKey;
  // Auth
  user: SessionUser | null;
  authLoading: boolean;
  // Data
  notes: Note[];
  categories: Category[];
  dataLoading: boolean;
  // Selected note (viewer)
  selectedNote: Note | null;
  noteLoading: boolean;
  // Search
  searchQuery: string;
  searchResults: Note[];
  searchCategoryFilter: string | null;
  searching: boolean;
  // Admin search filter
  adminStatusFilter: NoteStatus | "ALL";
  // Modals
  loginModalOpen: boolean;
  uploadModalOpen: boolean;
  searchModalOpen: boolean;
  // Versioning
  noteVersions: NoteVersion[];
  versionsLoading: boolean;
  // Scheduled publish
  pendingSchedules: ScheduledPublish[];
  // Recently viewed
  recentViews: NoteView[];
  recentLoading: boolean;

  // ---------- Actions ----------
  setView: (view: ViewKey) => void;
  openLoginModal: () => void;
  closeLoginModal: () => void;
  openUploadModal: () => void;
  closeUploadModal: () => void;
  openSearchModal: () => void;
  closeSearchModal: () => void;

  bootstrap: () => Promise<void>;
  refreshNotes: (opts?: { status?: NoteStatus }) => Promise<void>;

  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;

  openNote: (note: Note) => Promise<void>;
  openNoteBySearchResult: (note: Note) => void;

  setSearchQuery: (q: string) => void;
  runSearch: (q?: string) => Promise<void>;
  setSearchCategoryFilter: (categoryId: string | null) => void;
  setAdminStatusFilter: (s: NoteStatus | "ALL") => void;

  publishNote: (id: string) => Promise<void>;
  unpublishNote: (id: string) => Promise<void>;
  deleteNote: (id: string) => Promise<void>;
  onNoteCreated: (note: Note) => void;

  // Versioning
  loadNoteVersions: (noteId: string) => Promise<void>;
  restoreVersion: (noteId: string, versionId: string) => Promise<void>;
  // Scheduled publish
  schedulePublish: (noteId: string, publishAt: Date) => Promise<void>;
  cancelSchedule: (noteId: string) => Promise<void>;
  loadPendingSchedules: () => Promise<void>;
  // Recently viewed
  recordView: (noteId: string) => Promise<void>;
  loadRecentViews: (limit?: number) => Promise<void>;
  clearRecent: () => Promise<void>;
  // Bulk operations
  bulkAction: (action: BulkAction, noteIds: string[]) => Promise<BulkResult>;

  goToDashboard: () => void;
  goHome: () => void;
  goSearch: (q?: string) => void;
}

export const useAppStore = create<AppState>((set, get) => ({
  view: "public-home",
  user: null,
  authLoading: true,
  notes: [],
  categories: [],
  dataLoading: false,
  selectedNote: null,
  noteLoading: false,
  searchQuery: "",
  searchResults: [],
  searchCategoryFilter: null,
  searching: false,
  adminStatusFilter: "ALL",
  loginModalOpen: false,
  uploadModalOpen: false,
  searchModalOpen: false,
  noteVersions: [],
  versionsLoading: false,
  pendingSchedules: [],
  recentViews: [],
  recentLoading: false,

  setView: (view) => set({ view }),

  openLoginModal: () => set({ loginModalOpen: true }),
  closeLoginModal: () => set({ loginModalOpen: false }),
  openUploadModal: () => set({ uploadModalOpen: true }),
  closeUploadModal: () => set({ uploadModalOpen: false }),
  openSearchModal: () => set({ searchModalOpen: true }),
  closeSearchModal: () => set({ searchModalOpen: false }),

  bootstrap: async () => {
    set({ authLoading: true, dataLoading: true });
    try {
      const [session, categories] = await Promise.all([
        api.getSession(),
        api.fetchCategories(),
      ]);
      const isAdmin = session?.user?.role === "ADMIN";
      set({
        user: session?.user ?? null,
        categories,
        authLoading: false,
      });
      // Authenticated admins see every note (incl. drafts); visitors only see published.
      const notes = await api.fetchNotes(
        isAdmin ? { status: "ALL" } : { status: "PUBLISHED" },
      );
      set({
        notes: enrichNotes(notes, categories),
        dataLoading: false,
      });
    } catch {
      set({ authLoading: false, dataLoading: false });
    }
  },

  refreshNotes: async (opts) => {
    set({ dataLoading: true });
    try {
      const categories = get().categories;
      const notes = await api.fetchNotes(opts);
      set({ notes: enrichNotes(notes, categories) });
    } finally {
      set({ dataLoading: false });
    }
  },

  login: async (email, password) => {
    set({ authLoading: true });
    try {
      const session = await api.login(email, password);
      if (session.user.role !== "ADMIN") {
        // Non-admins are not allowed to open the dashboard.
        // Keep them signed out of the UI as well.
        try {
          await api.logout();
        } catch {
          /* ignore */
        }
        throw new Error(
          "This account does not have administrator privileges.",
        );
      }
      set({ user: session.user, loginModalOpen: false });
      // Load admin notes (all statuses) for the dashboard
      const categories = get().categories;
      const notes = await api.fetchNotes();
      set({
        notes: enrichNotes(notes, categories),
        view: "admin-dashboard",
      });
    } finally {
      set({ authLoading: false });
    }
  },

  logout: async () => {
    set({ authLoading: true });
    try {
      await api.logout();
    } finally {
      set({
        user: null,
        view: "public-home",
        authLoading: false,
        adminStatusFilter: "ALL",
      });
      const categories = get().categories;
      const notes = await api.fetchNotes({ status: "PUBLISHED" });
      set({ notes: enrichNotes(notes, categories) });
    }
  },

  openNote: async (note) => {
    set({ selectedNote: note, noteLoading: true, view: "note-viewer" });
    try {
      // If the caller only passed a partial note (e.g. search result), hydrate it.
      if (!note.description || !note.category) {
        const full = await api.fetchNoteById(note.id);
        if (full) {
          const categories = get().categories;
          const [enriched] = enrichNotes([full], categories);
          set({ selectedNote: enriched });
        }
      } else {
        const categories = get().categories;
        const [enriched] = enrichNotes([note], categories);
        set({ selectedNote: enriched });
      }
    } finally {
      set({ noteLoading: false });
    }
  },

  openNoteBySearchResult: (note) => {
    const categories = get().categories;
    const [enriched] = enrichNotes([note], categories);
    set({ selectedNote: enriched, view: "note-viewer", noteLoading: false });
  },

  setSearchQuery: (q) => set({ searchQuery: q }),

  runSearch: async (q) => {
    const query = q ?? get().searchQuery;
    set({ searchQuery: query, searching: true, view: "search-results" });
    try {
      const categories = get().categories;
      const results = await api.fetchNotes({ q: query, status: "PUBLISHED" });
      set({ searchResults: enrichNotes(results, categories) });
    } finally {
      set({ searching: false });
    }
  },

  setSearchCategoryFilter: (categoryId) =>
    set({ searchCategoryFilter: categoryId }),

  setAdminStatusFilter: (s) => set({ adminStatusFilter: s }),

  publishNote: async (id) => {
    const updated = await api.updateNoteStatus(id, "PUBLISHED");
    const categories = get().categories;
    const [enriched] = enrichNotes([updated], categories);
    set({
      notes: get().notes.map((n) => (n.id === id ? enriched : n)),
    });
  },

  unpublishNote: async (id) => {
    const updated = await api.updateNoteStatus(id, "UNPUBLISHED");
    const categories = get().categories;
    const [enriched] = enrichNotes([updated], categories);
    set({
      notes: get().notes.map((n) => (n.id === id ? enriched : n)),
    });
  },

  deleteNote: async (id) => {
    await api.deleteNote(id);
    set({ notes: get().notes.filter((n) => n.id !== id) });
  },

  onNoteCreated: (note) => {
    const categories = get().categories;
    const [enriched] = enrichNotes([note], categories);
    set({
      notes: [enriched, ...get().notes],
      uploadModalOpen: false,
      view: "admin-dashboard",
    });
  },

  // ─── Versioning ────────────────────────────────────────────
  loadNoteVersions: async (noteId) => {
    set({ versionsLoading: true });
    try {
      const versions = await api.fetchNoteVersions(noteId);
      set({ noteVersions: versions });
    } finally {
      set({ versionsLoading: false });
    }
  },

  restoreVersion: async (noteId, versionId) => {
    const restored = await api.restoreNoteVersion(noteId, versionId);
    const categories = get().categories;
    const [enriched] = enrichNotes([restored], categories);
    set({
      notes: get().notes.map((n) => (n.id === noteId ? enriched : n)),
      selectedNote: get().selectedNote?.id === noteId ? enriched : get().selectedNote,
    });
  },

  // ─── Scheduled publish ────────────────────────────────────
  schedulePublish: async (noteId, publishAt) => {
    await api.scheduleNotePublish(noteId, publishAt);
    await get().loadPendingSchedules();
  },

  cancelSchedule: async (noteId) => {
    await api.cancelScheduledPublish(noteId);
    set({
      pendingSchedules: get().pendingSchedules.filter(
        (s) => s.noteId !== noteId,
      ),
    });
  },

  loadPendingSchedules: async () => {
    try {
      const schedules = await api.fetchPendingSchedules();
      set({ pendingSchedules: schedules });
    } catch {
      /* ignore */
    }
  },

  // ─── Recently viewed ──────────────────────────────────────
  recordView: async (noteId) => {
    try {
      await api.recordNoteView(noteId);
    } catch {
      /* ignore — view tracking is best-effort */
    }
  },

  loadRecentViews: async (limit = 8) => {
    set({ recentLoading: true });
    try {
      const views = await api.fetchRecentViews(limit);
      set({ recentViews: views });
    } finally {
      set({ recentLoading: false });
    }
  },

  clearRecent: async () => {
    await api.clearRecentViews();
    set({ recentViews: [] });
  },

  // ─── Bulk operations ──────────────────────────────────────
  bulkAction: async (action, noteIds) => {
    const result = await api.bulkUpdateNotes(action, noteIds);
    // Refresh notes to reflect changes
    if (action === "DELETE") {
      set({
        notes: get().notes.filter((n) => !noteIds.includes(n.id)),
      });
    } else {
      const isAdmin = !!get().user;
      const fresh = await api.fetchNotes(isAdmin ? { status: "ALL" } : undefined);
      const categories = get().categories;
      set({ notes: enrichNotes(fresh, categories) });
    }
    return result;
  },

  goToDashboard: () => set({ view: "admin-dashboard" }),
  goHome: () => set({ view: "public-home" }),
  goSearch: (q) => {
    get().runSearch(q);
  },
}));
