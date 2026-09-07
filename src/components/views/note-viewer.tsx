"use client";

import * as React from "react";
import { AnimatePresence, motion } from "framer-motion";
import {
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  ChevronUp,
  Clock,
  Download,
  ExternalLink,
  FileImage,
  FileText,
  Folder,
  FolderOpen,
  FolderTree,
  Home,
  Maximize,
  Menu,
  Minimize,
  MoreVertical,
  Search,
  Share2,
  X,
  ZoomIn,
  ZoomOut,
} from "lucide-react";

import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { ScrollArea } from "@/components/ui/scroll-area";
import { useAppStore } from "@/lib/store";
import { fromNow, formatDateTime } from "@/lib/format";
import type { Note, Category } from "@/lib/types";
import { cn } from "@/lib/utils";

type SidebarMode = "tile" | "list";

// ─── Tree node type ───────────────────────────────────────────
interface TreeNode {
  category: Category;
  topics: { category: Category; notes: Note[] }[];
  notes: Note[];
}

function buildTree(categories: Category[], notes: Note[]): TreeNode[] {
  const top = categories.filter((c) => !c.parentId);
  return top
    .map((cat) => {
      const topics = categories
        .filter((c) => c.parentId === cat.id)
        .map((sub) => ({
          category: sub,
          notes: notes
            .filter((n) => n.categoryId === sub.id)
            .sort(
              (a, b) =>
                new Date(a.createdAt).getTime() -
                new Date(b.createdAt).getTime(),
            ),
        }))
        .filter((t) => t.notes.length > 0);
      const directNotes = notes
        .filter((n) => n.categoryId === cat.id)
        .sort(
          (a, b) =>
            new Date(a.createdAt).getTime() -
            new Date(b.createdAt).getTime(),
        );
      return { category: cat, topics, notes: directNotes };
    })
    .filter((n) => n.topics.length > 0 || n.notes.length > 0);
}

// ─── Animation variants ───────────────────────────────────────
const drawerVariants = {
  hidden: { x: "-100%", opacity: 0 },
  visible: { x: 0, opacity: 1, transition: { type: "spring", damping: 30, stiffness: 300 } },
  exit: { x: "-100%", opacity: 0, transition: { duration: 0.2 } },
};

const actionsVariants = {
  hidden: { x: 20, opacity: 0, scale: 0.95 },
  visible: { x: 0, opacity: 1, scale: 1, transition: { type: "spring", damping: 25, stiffness: 300 } },
  exit: { x: 20, opacity: 0, scale: 0.95, transition: { duration: 0.15 } },
};

const toolbarVariants = {
  hidden: { y: -20, opacity: 0, scale: 0.95 },
  visible: { y: 0, opacity: 1, scale: 1, transition: { type: "spring", damping: 25, stiffness: 300 } },
  exit: { y: -20, opacity: 0, scale: 0.95, transition: { duration: 0.15 } },
};

const collapsedHandleVariants = {
  hidden: { y: -10, opacity: 0 },
  visible: { y: 0, opacity: 1, transition: { delay: 0.1, duration: 0.2 } },
  exit: { y: -10, opacity: 0, transition: { duration: 0.1 } },
};

const pageTransition = {
  initial: { opacity: 0, y: 10 },
  animate: { opacity: 1, y: 0, transition: { duration: 0.25, ease: "easeOut" } },
  exit: { opacity: 0, y: -10, transition: { duration: 0.15, ease: "easeIn" } },
};

const tileVariants = {
  hidden: { opacity: 0, scale: 0.9 },
  visible: (i: number) => ({
    opacity: 1,
    scale: 1,
    transition: { delay: i * 0.04, duration: 0.2, ease: "easeOut" },
  }),
};

const listItemVariants = {
  hidden: { opacity: 0, x: -10 },
  visible: (i: number) => ({
    opacity: 1,
    x: 0,
    transition: { delay: i * 0.03, duration: 0.15, ease: "easeOut" },
  }),
};

const backdropVariants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { duration: 0.2 } },
  exit: { opacity: 0, transition: { duration: 0.15 } },
};

// ─── Main NoteViewer ───────────────────────────────────────────
export function NoteViewer() {
  const note = useAppStore((s) => s.selectedNote);
  const loading = useAppStore((s) => s.noteLoading);
  const allNotes = useAppStore((s) => s.notes);
  const allCategories = useAppStore((s) => s.categories);
  const openNote = useAppStore((s) => s.openNote);
  const goHome = useAppStore((s) => s.goHome);
  const openSearchModal = useAppStore((s) => s.openSearchModal);

  // State
  const [toolbarExpanded, setToolbarExpanded] = React.useState(true);
  const [drawerOpen, setDrawerOpen] = React.useState(false);
  const [actionsOpen, setActionsOpen] = React.useState(false);
  const [downloadOpen, setDownloadOpen] = React.useState(false);
  const [zoomPresetsOpen, setZoomPresetsOpen] = React.useState(false);
  const [pageViewMode, setPageViewMode] = React.useState<SidebarMode>("tiles");
  const [isFullscreen, setIsFullscreen] = React.useState(false);
  const [copied, setCopied] = React.useState(false);
  const [zoom, setZoom] = React.useState(1);
  const [zoomMode, setZoomMode] = React.useState<"fit" | "manual">("fit");
  const [pageInputValue, setPageInputValue] = React.useState("");
  const [pageInputFocused, setPageInputFocused] = React.useState(false);
  const [isNavigating, setIsNavigating] = React.useState(false);

  // Tree drawer state (Category → Topic → subtopic navigation)
  const [treeOpen, setTreeOpen] = React.useState(false);
  const [expandedCats, setExpandedCats] = React.useState<Set<string>>(new Set());
  const [expandedTopics, setExpandedTopics] = React.useState<Set<string>>(new Set());

  const containerRef = React.useRef<HTMLDivElement>(null);
  const mainRef = React.useRef<HTMLDivElement>(null);
  const downloadRef = React.useRef<HTMLDivElement>(null);
  const zoomRef = React.useRef<HTMLDivElement>(null);

  // ─── Build tree ─────────────────────────────────────────────
  const tree = React.useMemo(
    () => buildTree(allCategories, allNotes),
    [allCategories, allNotes],
  );

  // ─── Auto-expand active category in the tree ────────────────
  React.useEffect(() => {
    if (!note) return;
    const noteCat = allCategories.find((c) => c.id === note.categoryId);
    if (!noteCat) return;
    const parentId = noteCat.parentId ?? noteCat.id;
    setExpandedCats((prev) => new Set([...prev, parentId]));
    if (noteCat.parentId)
      setExpandedTopics((prev) => new Set([...prev, noteCat.id]));
  }, [note, allCategories]);

  // Pages
  const pages = React.useMemo(() => {
    if (!note) return [];
    return allNotes
      .filter((n) => n.categoryId === note.categoryId)
      .sort((a, b) => new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime());
  }, [allNotes, note]);

  const currentIndex = React.useMemo(() => {
    if (!note) return -1;
    return pages.findIndex((p) => p.id === note.id);
  }, [pages, note]);

  const totalPages = pages.length;
  const prevPage = currentIndex > 0 ? pages[currentIndex - 1] : null;
  const nextPage = currentIndex < totalPages - 1 ? pages[currentIndex + 1] : null;

  const handleNavigate = React.useCallback((page: Note) => {
    setIsNavigating(true);
    openNote(page);
    setDrawerOpen(false);
    setTreeOpen(false);
    setTimeout(() => setIsNavigating(false), 400);
  }, [openNote]);

  const toggleCat = (id: string) =>
    setExpandedCats((prev) => {
      const n = new Set(prev);
      if (n.has(id)) n.delete(id);
      else n.add(id);
      return n;
    });
  const toggleTopic = (id: string) =>
    setExpandedTopics((prev) => {
      const n = new Set(prev);
      if (n.has(id)) n.delete(id);
      else n.add(id);
      return n;
    });

  // Fit-to-view (measures the main document area, excluding the tree sidebar)
  const computeFitScale = React.useCallback(() => {
    const el = mainRef.current;
    if (!el) return;
    const w = el.clientWidth - 64;
    if (w <= 0) return;
    const fit = Math.min(w / 1136, 1);
    setZoom(Math.max(0.25, fit));
  }, []);

  React.useEffect(() => {
    if (zoomMode === "fit") {
      const t = setTimeout(computeFitScale, 50);
      return () => clearTimeout(t);
    }
  }, [note, zoomMode, computeFitScale, drawerOpen, treeOpen]);

  React.useEffect(() => {
    if (zoomMode !== "fit") return;
    const handler = () => computeFitScale();
    window.addEventListener("resize", handler);
    return () => window.removeEventListener("resize", handler);
  }, [zoomMode, computeFitScale]);

  // Fullscreen
  const toggleFullscreen = React.useCallback(() => {
    if (!document.fullscreenElement) {
      containerRef.current?.requestFullscreen?.();
    } else {
      document.exitFullscreen?.();
    }
  }, []);

  React.useEffect(() => {
    const h = () => setIsFullscreen(!!document.fullscreenElement);
    document.addEventListener("fullscreenchange", h);
    return () => document.removeEventListener("fullscreenchange", h);
  }, []);

  // Close popovers on outside click
  React.useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (downloadOpen && downloadRef.current && !downloadRef.current.contains(e.target as Node)) setDownloadOpen(false);
      if (zoomPresetsOpen && zoomRef.current && !zoomRef.current.contains(e.target as Node)) setZoomPresetsOpen(false);
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, [downloadOpen, zoomPresetsOpen]);

  // Keyboard
  React.useEffect(() => {
    const handleKey = (e: KeyboardEvent) => {
      const target = e.target as HTMLElement;
      const isTyping = target.tagName === "INPUT" || target.tagName === "TEXTAREA";

      if (e.key === "Escape") {
        if (treeOpen) { setTreeOpen(false); return; }
        if (drawerOpen) { setDrawerOpen(false); return; }
        if (downloadOpen) { setDownloadOpen(false); return; }
        if (actionsOpen) { setActionsOpen(false); return; }
        if (zoomPresetsOpen) { setZoomPresetsOpen(false); return; }
        setToolbarExpanded(false);
      }

      if ((e.ctrlKey || e.metaKey) && (e.key === "+" || e.key === "=")) {
        e.preventDefault(); setZoomMode("manual"); setZoom(z => Math.min(4, z + 0.1)); return;
      }
      if ((e.ctrlKey || e.metaKey) && e.key === "-") {
        e.preventDefault(); setZoomMode("manual"); setZoom(z => Math.max(0.25, z - 0.1)); return;
      }
      if ((e.ctrlKey || e.metaKey) && e.key === "0") {
        e.preventDefault(); setZoomMode("fit"); computeFitScale(); return;
      }
      if (isTyping) return;
      if (e.key === "ArrowLeft" && !drawerOpen && !treeOpen && prevPage) { e.preventDefault(); handleNavigate(prevPage); }
      if (e.key === "ArrowRight" && !drawerOpen && !treeOpen && nextPage) { e.preventDefault(); handleNavigate(nextPage); }
    };
    window.addEventListener("keydown", handleKey);
    return () => window.removeEventListener("keydown", handleKey);
  }, [drawerOpen, treeOpen, downloadOpen, actionsOpen, zoomPresetsOpen, prevPage, nextPage, handleNavigate, computeFitScale]);

  const handleShare = () => {
    navigator.clipboard?.writeText(window.location.href).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  // Render
  if (loading) {
    return (
      <div className="flex h-screen items-center justify-center bg-slate-800">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.3 }}
        >
          <Skeleton className="h-[60vh] w-full max-w-4xl rounded-xl" />
        </motion.div>
      </div>
    );
  }

  if (!note) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="flex h-screen flex-col items-center justify-center gap-4 bg-slate-800 text-center text-slate-200"
      >
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: "spring", damping: 20, stiffness: 200 }}
          className="flex size-16 items-center justify-center rounded-full bg-slate-700"
        >
          <Home className="size-8 text-slate-400" />
        </motion.div>
        <div>
          <h2 className="text-xl font-bold text-white">Note not found</h2>
          <p className="mt-1 text-sm text-slate-400">The note doesn't exist or is no longer published.</p>
        </div>
        <Button onClick={goHome} className="gap-2">
          <Home className="size-4" /> Browse all notes
        </Button>
      </motion.div>
    );
  }

  const zoomLabel = zoomMode === "fit" ? "Fit" : `${Math.round(zoom * 100)}%`;

  return (
    <div ref={containerRef} className="flex h-screen w-full overflow-hidden bg-slate-800">
      {/* ═══ Inline collapsible tree sidebar ═══ */}
      {/* Always shows a 48px icon rail (tree toggle + home). Expands to
          248px to reveal the full Category → Topic → subtopic tree. */}
      <motion.aside
        initial={false}
        animate={{ width: treeOpen ? 248 : 48 }}
        transition={{ type: "spring", damping: 30, stiffness: 300 }}
        className="relative z-30 shrink-0 overflow-hidden border-r border-slate-200 bg-slate-50"
      >
        <div className="flex h-full w-[248px]">
          {/* ── Always-visible icon rail (48px) ── */}
          <div className="flex w-12 shrink-0 flex-col items-center gap-1 border-r border-slate-200 bg-white py-2.5">
            <button
              onClick={() => setTreeOpen(!treeOpen)}
              className={cn(
                "flex size-9 items-center justify-center rounded-lg transition-colors",
                treeOpen
                  ? "bg-slate-900 text-white"
                  : "text-slate-500 hover:bg-slate-100 hover:text-slate-900",
              )}
              title={treeOpen ? "Collapse tree (Esc)" : "Browse categories (tree)"}
              aria-pressed={treeOpen}
            >
              <FolderTree className="h-4 w-4" />
            </button>
            <button
              onClick={goHome}
              className="flex size-9 items-center justify-center rounded-lg text-slate-500 transition-colors hover:bg-slate-100 hover:text-slate-900"
              title="Back to home"
            >
              <Home className="h-4 w-4" />
            </button>
          </div>

          {/* ── Expandable content panel (clipped when collapsed) ── */}
          <div className="flex min-w-0 flex-1 flex-col">
            {/* Header */}
            <div className="flex items-center justify-between border-b border-slate-200 bg-white px-3 py-2.5">
              <div className="flex items-center gap-2">
                <span className="text-sm font-semibold text-slate-900">Browse</span>
              </div>
              <button
                onClick={() => setTreeOpen(false)}
                className="rounded p-1 text-slate-400 hover:bg-slate-100 hover:text-slate-600"
                title="Collapse tree (Esc)"
              >
                <ChevronLeft className="h-4 w-4" />
              </button>
            </div>

            {/* Search (opens the global search window) */}
            <div className="border-b border-slate-200 bg-white px-3 py-2">
              <button
                onClick={openSearchModal}
                className="flex w-full items-center gap-2 rounded-md border border-slate-200 bg-slate-50 px-2.5 py-1.5 text-xs text-slate-400 transition-colors hover:border-slate-300 hover:bg-white hover:text-slate-600"
                title="Search notes (Ctrl+K)"
              >
                <Search className="h-3.5 w-3.5" />
                <span>Search notes…</span>
                <kbd className="ml-auto rounded border border-slate-200 bg-white px-1 py-0.5 text-[9px] font-mono text-slate-400">
                  ⌘K
                </kbd>
              </button>
            </div>

            {/* Tree */}
            <ScrollArea className="flex-1">
            {tree.length === 0 ? (
              <div className="px-4 py-10 text-center text-xs text-slate-400">
                No notes found
              </div>
            ) : (
              <div className="space-y-0.5 p-2">
                {tree.map((node) => {
                  const isExpanded = expandedCats.has(node.category.id);
                  const allNotes = [
                    ...node.notes,
                    ...node.topics.flatMap((t) => t.notes),
                  ];
                  const isActiveCat = allNotes.some((n) => n.id === note.id);
                  return (
                    <div key={node.category.id}>
                      {/* Category */}
                      <button
                        onClick={() => toggleCat(node.category.id)}
                        className={cn(
                          "flex w-full items-center gap-1.5 rounded-md px-2 py-1.5 text-left text-xs font-medium transition-colors",
                          isActiveCat
                            ? "bg-slate-100 text-slate-900"
                            : "text-slate-600 hover:bg-slate-100 hover:text-slate-900",
                        )}
                      >
                        <ChevronDown
                          className={cn(
                            "h-3 w-3 shrink-0 text-slate-400 transition-transform",
                            !isExpanded && "-rotate-90",
                          )}
                        />
                        {isExpanded ? (
                          <FolderOpen className="h-3.5 w-3.5 shrink-0 text-slate-400" />
                        ) : (
                          <Folder className="h-3.5 w-3.5 shrink-0 text-slate-400" />
                        )}
                        <span className="truncate">{node.category.name}</span>
                        <span className="ml-auto text-[10px] text-slate-400">
                          {allNotes.length}
                        </span>
                      </button>

                      {/* Expanded content */}
                      <AnimatePresence>
                        {isExpanded && (
                          <motion.div
                            initial={{ height: 0, opacity: 0 }}
                            animate={{ height: "auto", opacity: 1 }}
                            exit={{ height: 0, opacity: 0 }}
                            transition={{ duration: 0.2 }}
                            className="overflow-hidden"
                          >
                            <div className="ml-3 border-l border-slate-200 pl-2">
                              {/* Direct notes (subtopics) */}
                              {node.notes.map((n, idx) => (
                                <button
                                  key={n.id}
                                  onClick={() => handleNavigate(n)}
                                  className={cn(
                                    "flex w-full items-center gap-2 rounded-md px-2 py-1.5 text-left text-xs transition-colors",
                                    n.id === note.id
                                      ? "bg-rose-50 font-medium text-rose-700"
                                      : "text-slate-500 hover:bg-slate-100 hover:text-slate-800",
                                  )}
                                >
                                  <span
                                    className={cn(
                                      "flex h-4 w-4 shrink-0 items-center justify-center rounded text-[9px] font-mono",
                                      n.id === note.id
                                        ? "bg-rose-500 text-white"
                                        : "bg-slate-200 text-slate-500",
                                    )}
                                  >
                                    {idx + 1}
                                  </span>
                                  <span className="truncate">{n.title}</span>
                                </button>
                              ))}
                              {/* Topics → subtopics */}
                              {node.topics.map((topic) => {
                                const tExp = expandedTopics.has(topic.category.id);
                                const isActiveT = topic.notes.some(
                                  (n) => n.id === note.id,
                                );
                                return (
                                  <div key={topic.category.id}>
                                    <button
                                      onClick={() => toggleTopic(topic.category.id)}
                                      className={cn(
                                        "flex w-full items-center gap-1.5 rounded-md px-2 py-1 text-left text-xs transition-colors",
                                        isActiveT
                                          ? "text-slate-900"
                                          : "text-slate-500 hover:text-slate-800",
                                      )}
                                    >
                                      <ChevronDown
                                        className={cn(
                                          "h-3 w-3 shrink-0 text-slate-400 transition-transform",
                                          !tExp && "-rotate-90",
                                        )}
                                      />
                                      <span className="truncate">
                                        {topic.category.name}
                                      </span>
                                      <span className="ml-auto text-[10px] text-slate-400">
                                        {topic.notes.length}
                                      </span>
                                    </button>
                                    <AnimatePresence>
                                      {tExp && (
                                        <motion.div
                                          initial={{ height: 0, opacity: 0 }}
                                          animate={{ height: "auto", opacity: 1 }}
                                          exit={{ height: 0, opacity: 0 }}
                                          transition={{ duration: 0.2 }}
                                          className="overflow-hidden"
                                        >
                                          <div className="ml-3 border-l border-slate-200 pl-2">
                                            {topic.notes.map((n, idx) => (
                                              <button
                                                key={n.id}
                                                onClick={() => handleNavigate(n)}
                                                className={cn(
                                                  "flex w-full items-center gap-2 rounded-md px-2 py-1.5 text-left text-xs transition-colors",
                                                  n.id === note.id
                                                    ? "bg-rose-50 font-medium text-rose-700"
                                                    : "text-slate-500 hover:bg-slate-100 hover:text-slate-800",
                                                )}
                                              >
                                                <span
                                                  className={cn(
                                                    "flex h-4 w-4 shrink-0 items-center justify-center rounded text-[9px] font-mono",
                                                    n.id === note.id
                                                      ? "bg-rose-500 text-white"
                                                      : "bg-slate-200 text-slate-500",
                                                  )}
                                                >
                                                  {idx + 1}
                                                </span>
                                                <span className="truncate">{n.title}</span>
                                              </button>
                                            ))}
                                          </div>
                                        </motion.div>
                                      )}
                                    </AnimatePresence>
                                  </div>
                                );
                              })}
                            </div>
                          </motion.div>
                        )}
                      </AnimatePresence>
                    </div>
                  );
                })}
              </div>
            )}
          </ScrollArea>
          </div>
        </div>
      </motion.aside>

      {/* ═══ Main area (document + floating controls) ═══ */}
      <div ref={mainRef} className="relative flex min-w-0 flex-1 flex-col overflow-hidden bg-slate-800">
      {/* ═══ Document Viewer ═══ */}
      <div className="absolute inset-0 overflow-auto bg-[#cfc9bb]">
        <AnimatePresence mode="wait">
          <motion.div
            key={note.id}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="w-full"
            style={{
              minHeight: "100%",
            }}
          >
            <iframe
              title={note.title}
              src={note.contentPath}
              onLoad={(e) => {
                // Grow the iframe to fit its document so the whole note
                // is visible and scrollable inline — no inner scrollbar.
                try {
                  const iframe = e.currentTarget;
                  const doc = iframe.contentDocument;
                  if (!doc) return;
                  const resize = () => {
                    const h = Math.max(
                      doc.body.scrollHeight,
                      doc.body.offsetHeight,
                      doc.documentElement.scrollHeight,
                      doc.documentElement.offsetHeight,
                    );
                    if (h > 0) iframe.style.height = `${h}px`;
                  };
                  resize();
                  setTimeout(resize, 400);
                  setTimeout(resize, 1200);
                } catch {
                  /* cross-origin — ignore */
                }
              }}
              className="block w-full border-0 bg-[#cfc9bb]"
              style={{
                minHeight: "100vh",
                width: "100%",
              }}
            />
          </motion.div>
        </AnimatePresence>
      </div>

      {/* ═══ Top-right: Pages + Actions ═══ */}
      <motion.div
        initial={{ opacity: 0, x: 10 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.3 }}
        className="absolute right-3 top-3 z-30 flex items-center gap-2"
      >
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => setDrawerOpen(true)}
          className="flex h-9 w-9 items-center justify-center rounded-full border border-slate-200 bg-white/95 text-slate-600 shadow-md backdrop-blur-sm transition-colors hover:bg-white hover:text-slate-900"
          title="Open pages"
        >
          <Menu className="h-4 w-4" />
        </motion.button>
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => setActionsOpen(!actionsOpen)}
          className={cn(
            "flex h-9 w-9 items-center justify-center rounded-full border border-slate-200 shadow-md backdrop-blur-sm transition-colors",
            actionsOpen ? "bg-white text-slate-900" : "bg-white/95 text-slate-600 hover:bg-white hover:text-slate-900"
          )}
          title="Toggle actions"
        >
          <MoreVertical className="h-4 w-4" />
        </motion.button>
      </motion.div>

      {/* ═══ Top Floating Toolbar (top-left: page nav + zoom) ═══ */}
      <AnimatePresence>
        {toolbarExpanded ? (
          <motion.div
            key="toolbar-expanded"
            initial={{ opacity: 0, y: -20, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -20, scale: 0.9 }}
            transition={{ type: "spring", damping: 25, stiffness: 300 }}
            style={{ position: "absolute", left: "3.5rem", top: "0.5rem", zIndex: 20 }}
          >
            <div className="flex items-center gap-1 rounded-full border border-slate-200 bg-white/95 px-2 py-1.5 shadow-lg backdrop-blur-md">
              {/* Prev / page input / Next */}
              <Button variant="ghost" size="icon" disabled={!prevPage}
                onClick={() => prevPage && handleNavigate(prevPage)}
                className="h-8 w-8 rounded-full" title="Previous page (←)">
                <ChevronLeft className="h-4 w-4" />
              </Button>
              <div className="flex items-center gap-0.5 text-xs font-mono text-slate-700">
                <input
                  type="text"
                  value={pageInputFocused ? pageInputValue : String(currentIndex + 1)}
                  onChange={(e) => setPageInputValue(e.target.value.replace(/[^0-9]/g, ""))}
                  onFocus={() => { setPageInputFocused(true); setPageInputValue(String(currentIndex + 1)); }}
                  onBlur={() => {
                    setPageInputFocused(false);
                    const n = parseInt(pageInputValue, 10);
                    if (!isNaN(n) && n >= 1 && n <= totalPages) handleNavigate(pages[n - 1]);
                  }}
                  onKeyDown={(e) => { if (e.key === "Enter") e.currentTarget.blur(); }}
                  className="h-7 w-8 rounded border border-transparent bg-slate-100 text-center text-xs font-mono outline-none transition-colors hover:bg-slate-200 focus:border-slate-300 focus:bg-white"
                  title="Type page number"
                />
                <span className="text-slate-400">/</span>
                <span className="min-w-[20px] text-center">{totalPages}</span>
              </div>
              <Button variant="ghost" size="icon" disabled={!nextPage}
                onClick={() => nextPage && handleNavigate(nextPage)}
                className="h-8 w-8 rounded-full" title="Next page (→)">
                <ChevronRight className="h-4 w-4" />
              </Button>

              <Sep />

              {/* Zoom */}
              <Button variant="ghost" size="icon" className="h-8 w-8 rounded-full"
                onClick={() => { setZoomMode("manual"); setZoom(Math.max(0.25, zoom - 0.1)); }}
                title="Zoom out (Ctrl -)">
                <ZoomOut className="h-4 w-4" />
              </Button>
              <div className="relative" ref={zoomRef}>
                <button
                  className="h-7 min-w-[52px] rounded border border-transparent bg-slate-100 px-1.5 text-center text-xs font-mono transition-colors hover:border-slate-300 hover:bg-slate-200 outline-none"
                  onClick={() => setZoomPresetsOpen(!zoomPresetsOpen)}
                  title="Click to set zoom"
                >
                  {zoomLabel}
                </button>
                <AnimatePresence>
                  {zoomPresetsOpen && (
                    <motion.div
                      initial={{ opacity: 0, y: -5, scale: 0.95 }}
                      animate={{ opacity: 1, y: 0, scale: 1 }}
                      exit={{ opacity: 0, y: -5, scale: 0.95 }}
                      transition={{ duration: 0.15 }}
                      className="absolute left-1/2 top-full mt-2 w-40 -translate-x-1/2 rounded-lg border border-slate-200 bg-white p-1 shadow-xl"
                    >
                      <button onClick={() => { setZoomMode("fit"); computeFitScale(); setZoomPresetsOpen(false); }}
                        className="flex w-full items-center gap-2 rounded-md px-2 py-1.5 text-xs text-slate-700 hover:bg-slate-100">
                        <Maximize className="h-3.5 w-3.5" /> Fit
                      </button>
                      <div className="my-1 h-px bg-slate-100" />
                      {["50%", "75%", "100%", "125%", "150%", "200%"].map(label => (
                        <button key={label} onClick={() => { setZoomMode("manual"); setZoom(parseInt(label) / 100); setZoomPresetsOpen(false); }}
                          className="flex w-full items-center gap-2 rounded-md px-2 py-1.5 text-xs text-slate-700 hover:bg-slate-100">
                          {label}
                        </button>
                      ))}
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
              <Button variant="ghost" size="icon" className="h-8 w-8 rounded-full"
                onClick={() => { setZoomMode("manual"); setZoom(Math.min(4, zoom + 0.1)); }}
                title="Zoom in (Ctrl +)">
                <ZoomIn className="h-4 w-4" />
              </Button>

              <Sep />

              {/* Fullscreen */}
              <Button variant="ghost" size="icon" className="h-8 w-8 rounded-full"
                onClick={toggleFullscreen} title={isFullscreen ? "Exit fullscreen" : "Enter fullscreen"}>
                {isFullscreen ? <Minimize className="h-4 w-4" /> : <Maximize className="h-4 w-4" />}
              </Button>

              {/* Collapse */}
              <Button variant="ghost" size="icon" className="h-8 w-8 rounded-full"
                onClick={() => setToolbarExpanded(false)} title="Collapse toolbar (Esc)">
                <ChevronUp className="h-4 w-4" />
              </Button>
            </div>
          </motion.div>
        ) : (
          <motion.button
            key="toolbar-collapsed"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ delay: 0.1, duration: 0.2 }}
            style={{ position: "absolute", left: "3.5rem", top: "0.5rem", zIndex: 20 }}
            className="flex items-center gap-1.5 rounded-full border border-slate-200 bg-white/95 px-4 py-1.5 text-xs text-slate-600 shadow-md backdrop-blur-sm transition-colors hover:bg-white"
            onClick={() => setToolbarExpanded(true)}
            title="Expand toolbar"
          >
            <ChevronDown className="h-3 w-3" />
            <span className="font-mono">{currentIndex + 1}/{totalPages}</span>
          </motion.button>
        )}
      </AnimatePresence>

      {/* ═══ Left Sidebar Drawer ═══ */}
      <AnimatePresence>
        {drawerOpen && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.2 }}
              className="absolute inset-0 z-30 bg-black/30"
              onClick={() => setDrawerOpen(false)}
            />
            <motion.div
              initial={{ x: "100%" }}
              animate={{ x: 0 }}
              exit={{ x: "100%" }}
              transition={{ type: "spring", damping: 30, stiffness: 300 }}
              className="absolute bottom-0 right-0 top-0 z-40 flex w-[85vw] flex-col bg-white shadow-2xl sm:w-80 sm:max-w-[320px]"
            >
              {/* Header */}
              <div className="flex items-center justify-between border-b border-slate-200 px-4 py-3">
                <span className="text-sm font-semibold text-slate-900">Pages</span>
                <button onClick={() => setDrawerOpen(false)}
                  className="rounded p-1 text-slate-400 hover:bg-slate-100 hover:text-slate-600">
                  <X className="h-4 w-4" />
                </button>
              </div>
              {/* Toggle */}
              <div className="border-b border-slate-200 px-4 py-2">
                <div className="flex w-fit items-center gap-0.5 rounded-md bg-slate-100 p-0.5">
                  <button className={cn("rounded px-3 py-1 text-xs transition-all", pageViewMode === "list" ? "bg-white font-semibold shadow-sm" : "text-slate-500")}
                    onClick={() => setPageViewMode("list")}>List</button>
                  <button className={cn("rounded px-3 py-1 text-xs transition-all", pageViewMode === "tiles" ? "bg-white font-semibold shadow-sm" : "text-slate-500")}
                    onClick={() => setPageViewMode("tiles")}>Tiles</button>
                </div>
              </div>
              {/* Content */}
              <ScrollArea className="flex-1">
                {pageViewMode === "list" ? (
                  <div className="space-y-0.5 p-3">
                    {pages.map((page, idx) => (
                      <motion.button
                        key={page.id}
                        custom={idx}
                        initial={{ x: -10, opacity: 0 }}
                        animate={{ x: 0, opacity: 1, transition: { delay: idx * 0.03, duration: 0.15, ease: "easeOut" } }}
                        onClick={() => handleNavigate(page)}
                        className={cn("flex w-full items-center rounded-lg border px-3 py-2.5 text-left",
                          idx === currentIndex ? "border-rose-200 bg-rose-50" : "border-transparent hover:bg-slate-50")}
                      >
                        <span className={cn("mr-3 font-mono text-xs", idx === currentIndex ? "font-bold text-rose-600" : "text-slate-400")}>
                          {String(idx + 1).padStart(2, "0")}
                        </span>
                        <span className={cn("truncate text-sm", idx === currentIndex ? "font-medium text-rose-900" : "text-slate-700")}>
                          {page.title}
                        </span>
                      </motion.button>
                    ))}
                  </div>
                ) : (
                  <div className="grid grid-cols-2 gap-2 p-3">
                    {pages.map((page, idx) => (
                      <motion.button
                        key={page.id}
                        custom={idx}
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1, transition: { delay: idx * 0.04, duration: 0.2, ease: "easeOut" } }}
                        whileHover={{ scale: 1.03, transition: { duration: 0.15 } }}
                        whileTap={{ scale: 0.97 }}
                        onClick={() => handleNavigate(page)}
                        className={cn("overflow-hidden rounded-lg border-2 text-left",
                          idx === currentIndex ? "border-rose-400 shadow-md" : "border-slate-200 hover:border-slate-300")}
                      >
                        <div className="border-b border-slate-100 bg-slate-50 px-2 py-1 text-center text-[10px] font-semibold">
                          {String(idx + 1).padStart(2, "0")}
                        </div>
                        {/* Real preview */}
                        <div className="relative aspect-[3/4] overflow-hidden bg-white">
                          <iframe
                            src={page.contentPath}
                            className="pointer-events-none absolute left-0 top-0 border-0"
                            style={{ width: "1080px", height: "1440px", transform: "scale(0.12)", transformOrigin: "top left" }}
                            sandbox="allow-same-origin"
                            title={page.title}
                          />
                        </div>
                        <div className="truncate border-t border-slate-100 bg-slate-50 px-2 py-1 text-[10px] text-slate-600">
                          {page.title}
                        </div>
                      </motion.button>
                    ))}
                  </div>
                )}
              </ScrollArea>
            </motion.div>
          </>
        )}
      </AnimatePresence>

      {/* ═══ Right Actions Panel ═══ */}
      <AnimatePresence>
        {actionsOpen && (
          <motion.div
            initial={{ opacity: 0, x: 20, scale: 0.95 }}
            animate={{ opacity: 1, x: 0, scale: 1 }}
            exit={{ opacity: 0, x: 20, scale: 0.95 }}
            transition={{ type: "spring", damping: 25, stiffness: 300 }}
            className="absolute right-3 top-16 z-30 w-52 rounded-xl border border-slate-200 bg-white/95 p-3 shadow-lg backdrop-blur-md"
          >
            <div className="mb-2 flex items-center justify-between">
              <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">Actions</span>
              <button onClick={() => setActionsOpen(false)} className="text-slate-400 hover:text-slate-600">
                <X className="h-3.5 w-3.5" />
              </button>
            </div>
            <div className="space-y-1">
              <ActionBtn icon={Share2} label={copied ? "Link Copied!" : "Copy Link"} onClick={handleShare} />
              <ActionBtn icon={ExternalLink} label="Open Raw" onClick={() => window.open(note.contentPath, "_blank")} />
            </div>

            {/* Download / Export */}
            <div className="mt-2 border-t border-slate-100 pt-2" ref={downloadRef}>
              <button
                onClick={() => setDownloadOpen(!downloadOpen)}
                className={cn(
                  "flex w-full items-center gap-2.5 rounded-md px-3 py-2 text-left text-sm transition-colors hover:bg-slate-50",
                  downloadOpen && "bg-slate-50",
                )}
              >
                <Download className={cn("h-4 w-4 text-slate-500", downloadOpen && "text-slate-900")} />
                <span className={cn("text-slate-700", downloadOpen && "font-medium text-slate-900")}>Download</span>
                <ChevronDown className={cn("ml-auto h-3.5 w-3.5 text-slate-400 transition-transform", downloadOpen && "rotate-180")} />
              </button>
              <AnimatePresence>
                {downloadOpen && (
                  <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: "auto", opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    transition={{ duration: 0.2 }}
                    className="overflow-hidden"
                  >
                    <div className="ml-2 mt-1 space-y-0.5 border-l border-slate-100 pl-2">
                      <div className="px-2 py-1 text-[10px] font-bold uppercase tracking-wider text-slate-400">
                        Current Page ({currentIndex + 1})
                      </div>
                      {["PNG", "JPEG", "PDF"].map((fmt) => (
                        <button
                          key={fmt}
                          onClick={() => setDownloadOpen(false)}
                          className="flex w-full items-center gap-2 rounded-md px-2 py-1.5 text-xs text-slate-600 hover:bg-slate-100"
                        >
                          <FileImage className="h-3.5 w-3.5 text-slate-400" /> {fmt}
                        </button>
                      ))}
                      <div className="my-1 h-px bg-slate-100" />
                      <div className="px-2 py-1 text-[10px] font-bold uppercase tracking-wider text-slate-400">All Pages</div>
                      {["PDF", "PNG (ZIP)"].map((fmt) => (
                        <button
                          key={fmt}
                          onClick={() => setDownloadOpen(false)}
                          className="flex w-full items-center gap-2 rounded-md px-2 py-1.5 text-xs text-slate-600 hover:bg-slate-100"
                        >
                          <FileText className="h-3.5 w-3.5 text-slate-400" /> {fmt}
                        </button>
                      ))}
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>

            <div className="mt-3 border-t border-slate-100 pt-3">
              <div className="flex flex-col gap-1 text-xs text-slate-500">
                <div className="flex items-center gap-1.5">
                  <Clock className="h-3 w-3" /> Updated {fromNow(note.updatedAt)}
                </div>
                <div>{formatDateTime(note.updatedAt)}</div>
              </div>
              {note.tags && note.tags.length > 0 && (
                <div className="mt-2 flex flex-wrap gap-1">
                  {note.tags.map(t => (
                    <Badge key={t.id} variant="outline" className="text-[10px] font-normal">{t.name}</Badge>
                  ))}
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
      </div>
    </div>
  );
}

// ─── Helpers ──────────────────────────────────────────────────
function Sep() {
  return <div className="mx-0.5 h-5 w-px bg-slate-200" />;
}

function ActionBtn({
  icon: Icon,
  label,
  onClick,
  textColor,
}: {
  icon: React.ElementType;
  label: string;
  onClick: () => void;
  textColor?: string;
}) {
  return (
    <motion.button
      whileHover={{ x: 2 }}
      onClick={onClick}
      className="flex w-full items-center gap-2.5 rounded-md px-3 py-2 text-left text-sm transition-colors hover:bg-slate-50"
    >
      <Icon className={cn("h-4 w-4", textColor ?? "text-slate-500")} />
      <span className={textColor ?? "text-slate-700"}>{label}</span>
    </motion.button>
  );
}
