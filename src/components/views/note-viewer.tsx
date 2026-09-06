"use client";

import * as React from "react";
import {
  ChevronLeft,
  ChevronRight,
  ChevronUp,
  Clock,
  Download,
  ExternalLink,
  FileJson,
  FileImage,
  FileText,
  Grid2x2,
  History,
  Home,
  LayoutGrid,
  List,
  Maximize2,
  Minimize2,
  PanelLeft,
  PanelRight,
  Plane,
  Search,
  Share2,
  Upload,
  X,
  ZoomIn,
  ZoomOut,
} from "lucide-react";

import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { useAppStore } from "@/lib/store";
import { formatDateTime, fromNow } from "@/lib/format";
import type { Note } from "@/lib/types";
import { cn } from "@/lib/utils";

// ─── Reader Types ──────────────────────────────────────────────
type SidebarMode = "tile" | "list";

// ─── Main NoteViewer (Reader) ──────────────────────────────────
export function NoteViewer() {
  const note = useAppStore((s) => s.selectedNote);
  const loading = useAppStore((s) => s.noteLoading);
  const allNotes = useAppStore((s) => s.notes);
  const openNote = useAppStore((s) => s.openNote);
  const goHome = useAppStore((s) => s.goHome);

  // Reader UI state
  const [sidebarOpen, setSidebarOpen] = React.useState(true);
  const [sidebarMode, setSidebarMode] = React.useState<SidebarMode>("tile");
  const [rightPanelOpen, setRightPanelOpen] = React.useState(true);
  const [topBarCollapsed, setTopBarCollapsed] = React.useState(false);
  const [zoom, setZoom] = React.useState(1);
  const [isFullscreen, setIsFullscreen] = React.useState(false);
  const [sidebarSearch, setSidebarSearch] = React.useState("");
  const [exportMenuOpen, setExportMenuOpen] = React.useState(false);
  const iframeRef = React.useRef<HTMLIFrameElement>(null);
  const readerRef = React.useRef<HTMLDivElement>(null);
  const exportMenuRef = React.useRef<HTMLDivElement>(null);

  // Collect "pages" — all notes in the same category, sorted by createdAt
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

  const prevPage = currentIndex > 0 ? pages[currentIndex - 1] : null;
  const nextPage = currentIndex < pages.length - 1 ? pages[currentIndex + 1] : null;

  const filteredPages = React.useMemo(() => {
    if (!sidebarSearch.trim()) return pages;
    const q = sidebarSearch.toLowerCase();
    return pages.filter((p) => p.title.toLowerCase().includes(q));
  }, [pages, sidebarSearch]);

  // Auto-close sidebar on mobile when navigating to a page
  const handleNavigate = React.useCallback((page: Note) => {
    openNote(page);
    if (typeof window !== "undefined" && window.innerWidth < 768) {
      setSidebarOpen(false);
    }
  }, [openNote]);

  // Fullscreen handler
  const toggleFullscreen = React.useCallback(() => {
    if (!document.fullscreenElement) {
      readerRef.current?.requestFullscreen?.();
    } else {
      document.exitFullscreen?.();
    }
  }, []);

  React.useEffect(() => {
    const handler = () => setIsFullscreen(!!document.fullscreenElement);
    document.addEventListener("fullscreenchange", handler);
    return () => document.removeEventListener("fullscreenchange", handler);
  }, []);

  // Close export menu on outside click
  React.useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (exportMenuOpen && exportMenuRef.current && !exportMenuRef.current.contains(e.target as Node)) {
        setExportMenuOpen(false);
      }
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, [exportMenuOpen]);

  // Keyboard navigation
  React.useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return;
      if (e.key === "ArrowLeft" && prevPage) {
        e.preventDefault();
        handleNavigate(prevPage);
      } else if (e.key === "ArrowRight" && nextPage) {
        e.preventDefault();
        handleNavigate(nextPage);
      } else if (e.key === "Escape" && isFullscreen) {
        document.exitFullscreen?.();
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [prevPage, nextPage, handleNavigate, isFullscreen]);

  // Inject CSS into iframe for binding visibility
  const handleIframeLoad = React.useCallback((e: React.SyntheticEvent<HTMLIFrameElement>) => {
    try {
      const iframe = e.currentTarget;
      const doc = iframe.contentDocument;
      if (!doc) return;
      const existing = doc.getElementById("reader-injected-style");
      if (existing) existing.remove();
      const style = doc.createElement("style");
      style.id = "reader-injected-style";
      style.textContent = `
        body {
          justify-content: flex-start !important;
          padding-left: 42px !important;
          padding-right: 14px !important;
        }
        @media (max-width: 1120px) {
          html { overflow-x: auto; }
        }
      `;
      doc.head.appendChild(style);
      const resize = () => {
        const body = doc.body;
        const html = doc.documentElement;
        const height = Math.max(
          body.scrollHeight,
          body.offsetHeight,
          html.scrollHeight,
          html.offsetHeight
        );
        iframe.style.height = `${height + 20}px`;
      };
      resize();
      setTimeout(resize, 500);
      setTimeout(resize, 1500);
    } catch {
      // Cross-origin or sandbox restriction — ignore
    }
  }, []);

  const category = note?.category;
  const subcategory = note?.subcategory ?? (category?.parentId ? category : null);
  const topCategory = category && category.parentId ? null : category;

  if (loading) {
    return (
      <div className="flex flex-1 items-center justify-center bg-slate-800 p-12">
        <Skeleton className="h-[60vh] w-full max-w-4xl rounded-xl" />
      </div>
    );
  }

  if (!note) {
    return (
      <div className="flex flex-1 flex-col items-center justify-center gap-4 bg-slate-800 p-12 text-center text-slate-200">
        <div className="flex size-16 items-center justify-center rounded-full bg-slate-700">
          <Search className="size-8 text-slate-400" />
        </div>
        <div>
          <h2 className="text-xl font-bold text-white">Note not found</h2>
          <p className="mt-1 text-sm text-slate-400">
            The note you're looking for doesn't exist or is no longer published.
          </p>
        </div>
        <Button onClick={goHome} variant="default" className="gap-2">
          <Home className="size-4" />
          Browse all notes
        </Button>
      </div>
    );
  }

  return (
    <div ref={readerRef} className="flex h-screen flex-col bg-slate-800">
      {/* ═══ Floating Top Toolbar (pill-shaped, centered) ═══ */}
      <div className="pointer-events-none absolute inset-x-0 top-0 z-50 flex justify-center px-4 pt-3">
        <div className={cn(
          "pointer-events-auto flex items-center gap-1 rounded-full border border-slate-200 bg-white px-2 py-1.5 shadow-lg transition-all duration-200 dark:border-slate-700 dark:bg-slate-900",
          topBarCollapsed && "opacity-60 hover:opacity-100"
        )}>
          {/* Sidebar toggle */}
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="size-8 rounded-full"
            title="Toggle page navigation"
          >
            <PanelLeft className="size-4" />
          </Button>

          {/* Divider */}
          <div className="h-5 w-px bg-slate-200 dark:bg-slate-700" />

          {/* Prev / Page indicator / Next */}
          <Button
            variant="ghost"
            size="icon"
            disabled={!prevPage}
            onClick={() => prevPage && handleNavigate(prevPage)}
            className="size-8 rounded-full"
            title="Previous page"
          >
            <ChevronLeft className="size-4" />
          </Button>
          <span className="min-w-[3rem] text-center text-xs font-medium tabular-nums text-slate-600 dark:text-slate-300">
            {currentIndex + 1} / {pages.length}
          </span>
          <Button
            variant="ghost"
            size="icon"
            disabled={!nextPage}
            onClick={() => nextPage && handleNavigate(nextPage)}
            className="size-8 rounded-full"
            title="Next page"
          >
            <ChevronRight className="size-4" />
          </Button>

          {/* Divider */}
          <div className="h-5 w-px bg-slate-200 dark:bg-slate-700" />

          {/* Zoom controls */}
          <Button
            variant="ghost"
            size="icon"
            className="size-8 rounded-full"
            onClick={() => setZoom(Math.max(0.3, zoom - 0.1))}
            title="Zoom out"
          >
            <ZoomOut className="size-4" />
          </Button>
          <span className="min-w-[2.5rem] text-center text-xs font-medium tabular-nums text-slate-600 dark:text-slate-300">
            {Math.round(zoom * 100)}%
          </span>
          <Button
            variant="ghost"
            size="icon"
            className="size-8 rounded-full"
            onClick={() => setZoom(Math.min(2, zoom + 0.1))}
            title="Zoom in"
          >
            <ZoomIn className="size-4" />
          </Button>

          {/* Divider */}
          <div className="h-5 w-px bg-slate-200 dark:bg-slate-700" />

          {/* Export/download dropdown */}
          <div className="relative" ref={exportMenuRef}>
            <Button
              variant="ghost"
              size="icon"
              className={cn("size-8 rounded-full", exportMenuOpen && "bg-slate-100 dark:bg-slate-800")}
              onClick={() => setExportMenuOpen(!exportMenuOpen)}
              title="Export"
            >
              <Download className="size-4" />
            </Button>
            {exportMenuOpen && (
              <div className="absolute left-0 top-full mt-2 w-56 rounded-lg border border-slate-200 bg-white p-1.5 shadow-xl dark:border-slate-700 dark:bg-slate-900">
                <ExportSection title={`CURRENT PAGE (${currentIndex + 1})`}>
                  <ExportItem icon={FileImage} label="PNG" onClick={() => setExportMenuOpen(false)} />
                  <ExportItem icon={FileImage} label="JPEG" onClick={() => setExportMenuOpen(false)} />
                  <ExportItem icon={FileText} label="PDF" onClick={() => setExportMenuOpen(false)} />
                  <ExportItem icon={FileJson} label="Polotno JSON" onClick={() => setExportMenuOpen(false)} />
                </ExportSection>
                <div className="my-1 h-px bg-slate-100 dark:bg-slate-800" />
                <ExportSection title="ALL PAGES">
                  <ExportItem icon={FileText} label="PDF" onClick={() => setExportMenuOpen(false)} />
                  <ExportItem icon={FileImage} label="PNG (ZIP)" onClick={() => setExportMenuOpen(false)} />
                  <ExportItem icon={FileJson} label="Polotno JSON (ZIP)" onClick={() => setExportMenuOpen(false)} />
                </ExportSection>
                <div className="my-1 h-px bg-slate-100 dark:bg-slate-800" />
                <ExportSection title="FULL DOCUMENT">
                  <ExportItem icon={FileJson} label="Full Polotno JSON" onClick={() => setExportMenuOpen(false)} />
                </ExportSection>
              </div>
            )}
          </div>

          {/* Right panel toggle */}
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setRightPanelOpen(!rightPanelOpen)}
            className={cn("size-8 rounded-full", rightPanelOpen && "bg-slate-100 dark:bg-slate-800")}
            title="Toggle actions panel"
          >
            <PanelRight className="size-4" />
          </Button>

          {/* Fullscreen */}
          <Button
            variant="ghost"
            size="icon"
            onClick={toggleFullscreen}
            className="size-8 rounded-full"
            title={isFullscreen ? "Exit fullscreen" : "Enter fullscreen"}
          >
            {isFullscreen ? <Minimize2 className="size-4" /> : <Maximize2 className="size-4" />}
          </Button>

          {/* Collapse/expand top bar */}
          <Button
            variant="ghost"
            size="icon"
            className="size-8 rounded-full"
            onClick={() => setTopBarCollapsed(!topBarCollapsed)}
            title={topBarCollapsed ? "Expand toolbar" : "Collapse toolbar"}
          >
            <ChevronUp className={cn("size-4 transition-transform", topBarCollapsed && "rotate-180")} />
          </Button>
        </div>
      </div>

      {/* ═══ Main Reader Area ═══ */}
      <div className="flex min-h-0 flex-1 pt-16">
        {/* ─── Left Sidebar (Page Navigation) ─── */}
        {sidebarOpen && (
          <aside className="absolute inset-y-0 left-0 z-40 flex w-72 shrink-0 flex-col border-r border-slate-200 bg-white dark:border-slate-700 dark:bg-slate-900 md:relative md:z-auto md:shadow-none">
            {/* Sidebar header */}
            <div className="flex items-center justify-between border-b border-slate-200 px-4 py-3 dark:border-slate-700">
              <span className="text-sm font-bold text-slate-800 dark:text-slate-200">Pages</span>
              <Button
                variant="ghost"
                size="icon"
                className="size-6"
                onClick={() => setSidebarOpen(false)}
              >
                <X className="size-3.5" />
              </Button>
            </div>

            {/* View toggle */}
            <div className="flex items-center gap-1 border-b border-slate-200 px-4 py-2 dark:border-slate-700">
              <button
                onClick={() => setSidebarMode("list")}
                className={cn(
                  "flex items-center gap-1.5 rounded-md px-3 py-1 text-xs font-medium transition-colors",
                  sidebarMode === "list"
                    ? "bg-slate-100 text-slate-900 dark:bg-slate-800 dark:text-white"
                    : "text-slate-500 hover:text-slate-700 dark:text-slate-400"
                )}
              >
                <List className="size-3.5" />
                List
              </button>
              <button
                onClick={() => setSidebarMode("tile")}
                className={cn(
                  "flex items-center gap-1.5 rounded-md px-3 py-1 text-xs font-medium transition-colors",
                  sidebarMode === "tile"
                    ? "bg-slate-100 text-slate-900 dark:bg-slate-800 dark:text-white"
                    : "text-slate-500 hover:text-slate-700 dark:text-slate-400"
                )}
              >
                <Grid2x2 className="size-3.5" />
                Tiles
              </button>
            </div>

            {/* Search within pages */}
            {pages.length > 3 && (
              <div className="border-b border-slate-200 px-3 py-2 dark:border-slate-700">
                <div className="relative">
                  <Search className="pointer-events-none absolute left-2.5 top-1/2 size-3.5 -translate-y-1/2 text-slate-400" />
                  <Input
                    value={sidebarSearch}
                    onChange={(e) => setSidebarSearch(e.target.value)}
                    placeholder="Filter pages…"
                    className="h-8 border-slate-200 pl-8 text-xs dark:border-slate-700"
                  />
                </div>
              </div>
            )}

            {/* Page list / tiles */}
            <ScrollArea className="flex-1">
              {sidebarMode === "list" ? (
                <PageListView
                  pages={filteredPages}
                  currentPageId={note.id}
                  onNavigate={handleNavigate}
                />
              ) : (
                <PageTileView
                  pages={filteredPages}
                  currentPageId={note.id}
                  onNavigate={handleNavigate}
                />
              )}
            </ScrollArea>

            {/* Prev/Next at bottom */}
            {pages.length > 1 && (
              <div className="flex items-center justify-between border-t border-slate-200 px-3 py-2 dark:border-slate-700">
                <Button
                  variant="ghost"
                  size="sm"
                  disabled={!prevPage}
                  onClick={() => prevPage && handleNavigate(prevPage)}
                  className="gap-1 text-xs"
                >
                  <ChevronLeft className="size-3.5" />
                  Prev
                </Button>
                <span className="text-xs tabular-nums text-slate-500">
                  {currentIndex + 1}/{pages.length}
                </span>
                <Button
                  variant="ghost"
                  size="sm"
                  disabled={!nextPage}
                  onClick={() => nextPage && handleNavigate(nextPage)}
                  className="gap-1 text-xs"
                >
                  Next
                  <ChevronRight className="size-3.5" />
                </Button>
              </div>
            )}
          </aside>
        )}

        {/* ─── Center Reading Area (floating white paper on dark bg) ─── */}
        <div className="flex min-w-0 flex-1 flex-col overflow-auto bg-slate-800">
          {/* Breadcrumb */}
          <div className="flex items-center gap-2 px-4 py-2 text-xs text-slate-400">
            <button onClick={goHome} className="flex items-center gap-1 hover:text-slate-200">
              <Home className="size-3" />
              Home
            </button>
            {topCategory && (
              <>
                <ChevronRight className="size-3" />
                <span>{topCategory.name}</span>
              </>
            )}
            {subcategory && subcategory.id !== topCategory?.id && (
              <>
                <ChevronRight className="size-3" />
                <span>{subcategory.name}</span>
              </>
            )}
            <ChevronRight className="size-3" />
            <span className="max-w-[300px] truncate text-slate-300">{note.title}</span>
          </div>

          {/* Note header */}
          <div className="px-4 pb-2 md:px-6">
            <div className="mb-1 flex flex-wrap items-center gap-2 text-xs text-slate-400">
              {topCategory && (
                <Badge variant="outline" className="border-red-500/30 bg-red-50 text-red-600 dark:bg-red-950/30 dark:text-red-400">
                  {topCategory.name}
                </Badge>
              )}
              {subcategory && subcategory.id !== topCategory?.id && (
                <Badge variant="secondary" className="dark:bg-slate-700">{subcategory.name}</Badge>
              )}
              <span className="flex items-center gap-1">
                <Clock className="size-3" />
                {fromNow(note.updatedAt)}
              </span>
            </div>
            <h1 className="text-xl font-bold tracking-tight text-white md:text-2xl">{note.title}</h1>
            {note.description && (
              <p className="mt-1 text-sm text-slate-400">{note.description}</p>
            )}
          </div>

          {/* Floating white paper container with iframe */}
          <div className="flex-1 p-4 md:p-6">
            <div
              className="mx-auto overflow-x-auto rounded-xl bg-white shadow-2xl dark:bg-white"
              style={{ maxWidth: `${1080 + 56}px` }}
            >
              <iframe
                ref={iframeRef}
                title={note.title}
                className="note-iframe block"
                style={{
                  minHeight: "60vh",
                  transform: `scale(${zoom})`,
                  transformOrigin: "top left",
                  width: `${100 / zoom}%`,
                  border: 0,
                }}
                src={note.contentPath}
                sandbox="allow-same-origin allow-popups"
                onLoad={handleIframeLoad}
              />
            </div>
          </div>

          {/* Bottom prev/next bar */}
          {pages.length > 1 && (
            <div className="flex items-center justify-between border-t border-slate-700 px-4 py-2">
              {prevPage ? (
                <Button variant="ghost" size="sm" onClick={() => handleNavigate(prevPage)} className="gap-1.5 text-slate-300 hover:text-white">
                  <ChevronLeft className="size-4" />
                  <span className="hidden max-w-[200px] truncate sm:inline">{prevPage.title}</span>
                  <span className="sm:hidden">Prev</span>
                </Button>
              ) : (
                <div />
              )}
              {nextPage ? (
                <Button variant="ghost" size="sm" onClick={() => handleNavigate(nextPage)} className="gap-1.5 text-slate-300 hover:text-white">
                  <span className="hidden max-w-[200px] truncate sm:inline">{nextPage.title}</span>
                  <span className="sm:hidden">Next</span>
                  <ChevronRight className="size-4" />
                </Button>
              ) : (
                <div />
              )}
            </div>
          )}
        </div>

        {/* ─── Right Panel (Actions) ─── */}
        {rightPanelOpen && (
          <aside className="hidden w-64 shrink-0 flex-col border-l border-slate-200 bg-white dark:border-slate-700 dark:bg-slate-900 lg:flex">
            <RightPanel
              note={note}
              pages={pages}
              currentIndex={currentIndex}
              onNavigate={handleNavigate}
              goHome={goHome}
            />
          </aside>
        )}
      </div>
    </div>
  );
}

// ─── Page List View ────────────────────────────────────────────
function PageListView({
  pages,
  currentPageId,
  onNavigate,
}: {
  pages: Note[];
  currentPageId: string;
  onNavigate: (note: Note) => void;
}) {
  return (
    <div className="flex flex-col py-1">
      {pages.map((page, idx) => {
        const isActive = page.id === currentPageId;
        return (
          <button
            key={page.id}
            onClick={() => onNavigate(page)}
            className={cn(
              "flex items-start gap-2.5 px-3 py-2 text-left transition-colors hover:bg-slate-50 dark:hover:bg-slate-800",
              isActive && "bg-red-50 dark:bg-red-950/20"
            )}
          >
            <span
              className={cn(
                "mt-0.5 flex size-6 shrink-0 items-center justify-center rounded text-xs font-bold tabular-nums",
                isActive
                  ? "bg-red-500 text-white"
                  : "bg-slate-100 text-slate-500 dark:bg-slate-800"
              )}
            >
              {String(idx + 1).padStart(2, "0")}
            </span>
            <div className="min-w-0 flex-1">
              <p className={cn(
                "truncate text-sm leading-tight",
                isActive ? "font-semibold text-red-600 dark:text-red-400" : "text-slate-700 dark:text-slate-300"
              )}>
                {page.title}
              </p>
              {page.description && (
                <p className="mt-0.5 truncate text-xs text-slate-400">
                  {page.description}
                </p>
              )}
            </div>
            {isActive && (
              <span className="mt-1 size-2 shrink-0 rounded-full bg-red-500" />
            )}
          </button>
        );
      })}
    </div>
  );
}

// ─── Page Tile View ────────────────────────────────────────────
function PageTileView({
  pages,
  currentPageId,
  onNavigate,
}: {
  pages: Note[];
  currentPageId: string;
  onNavigate: (note: Note) => void;
}) {
  return (
    <div className="grid grid-cols-2 gap-2 p-2">
      {pages.map((page, idx) => {
        const isActive = page.id === currentPageId;
        return (
          <button
            key={page.id}
            onClick={() => onNavigate(page)}
            className={cn(
              "group flex flex-col gap-1.5 rounded-lg border-2 p-2 text-left transition-all hover:shadow-md",
              isActive
                ? "border-red-500 bg-red-50 dark:bg-red-950/20"
                : "border-slate-200 bg-white hover:border-slate-300 dark:border-slate-700 dark:bg-slate-800"
            )}
          >
            {/* Thumbnail */}
            <div className={cn(
              "flex aspect-[3/4] items-center justify-center rounded-md overflow-hidden",
              isActive ? "bg-red-100 dark:bg-red-900/30" : "bg-slate-100 dark:bg-slate-700"
            )}>
              <div className="flex h-full w-full flex-col gap-0.5 p-1.5 opacity-60">
                <div className={cn("h-1.5 w-3/4 rounded", isActive ? "bg-red-400" : "bg-slate-300 dark:bg-slate-500")} />
                <div className={cn("h-1 w-full rounded", isActive ? "bg-red-300" : "bg-slate-200 dark:bg-slate-600")} />
                <div className={cn("h-1 w-2/3 rounded", isActive ? "bg-red-300" : "bg-slate-200 dark:bg-slate-600")} />
                <div className="mt-1 flex gap-0.5">
                  <div className={cn("h-3 flex-1 rounded", isActive ? "bg-red-200" : "bg-slate-200 dark:bg-slate-600")} />
                  <div className={cn("h-3 flex-1 rounded", isActive ? "bg-blue-200" : "bg-blue-100 dark:bg-slate-600")} />
                </div>
                <div className={cn("h-1 w-full rounded", isActive ? "bg-red-300" : "bg-slate-200 dark:bg-slate-600")} />
                <div className={cn("h-1 w-1/2 rounded", isActive ? "bg-red-300" : "bg-slate-200 dark:bg-slate-600")} />
              </div>
            </div>
            {/* Page number */}
            <span className={cn(
              "text-center text-xs font-bold tabular-nums",
              isActive ? "text-red-600 dark:text-red-400" : "text-slate-400"
            )}>
              {String(idx + 1).padStart(2, "0")}
            </span>
            {/* Title */}
            <p className={cn(
              "line-clamp-2 text-[10px] leading-tight",
              isActive ? "font-semibold text-red-600 dark:text-red-400" : "text-slate-600 dark:text-slate-400"
            )}>
              {page.title}
            </p>
          </button>
        );
      })}
    </div>
  );
}

// ─── Right Actions Panel ───────────────────────────────────────
function RightPanel({
  note,
  pages,
  currentIndex,
  onNavigate,
  goHome,
}: {
  note: Note;
  pages: Note[];
  currentIndex: number;
  onNavigate: (note: Note) => void;
  goHome: () => void;
}) {
  const [copied, setCopied] = React.useState(false);

  const handleShare = () => {
    const url = window.location.href;
    navigator.clipboard?.writeText(url).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  return (
    <div className="flex h-full flex-col overflow-y-auto">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-200 px-4 py-3 dark:border-slate-700">
        <span className="text-xs font-bold uppercase tracking-wider text-slate-500">Actions</span>
      </div>

      {/* Action items */}
      <div className="flex flex-col gap-0.5 p-2">
        <ActionButton icon={Upload} label="Replace Page" />
        <ActionButton icon={History} label="Version History" />
        <ActionButton icon={LayoutGrid} label="Overview Grid" />
        <ActionButton icon={Plane} label="Publish" textColor="text-green-600 dark:text-green-400" />
      </div>

      <div className="my-1 h-px bg-slate-100 dark:bg-slate-800" />

      {/* Note info */}
      <div className="p-3">
        <h3 className="mb-2 text-xs font-bold uppercase tracking-wider text-slate-500">
          Note Info
        </h3>
        <div className="flex flex-col gap-1.5 text-xs text-slate-600 dark:text-slate-400">
          <div className="flex items-center gap-1.5">
            <Clock className="size-3" />
            <span>Updated {fromNow(note.updatedAt)}</span>
          </div>
          <div>{formatDateTime(note.updatedAt)}</div>
        </div>
        {note.tags && note.tags.length > 0 && (
          <div className="mt-3 flex flex-wrap gap-1">
            {note.tags.map((t) => (
              <Badge key={t.id} variant="outline" className="text-[10px] font-normal">
                {t.name}
              </Badge>
            ))}
          </div>
        )}
      </div>

      {/* Quick share */}
      <div className="border-t border-slate-100 p-3 dark:border-slate-800">
        <Button variant="outline" size="sm" className="w-full justify-start gap-2 text-xs" onClick={handleShare}>
          <Share2 className="size-3.5" />
          {copied ? "Link Copied!" : "Copy Link"}
        </Button>
        <Button variant="ghost" size="sm" asChild className="mt-1 w-full justify-start gap-2 text-xs">
          <a href={note.contentPath} target="_blank" rel="noopener noreferrer">
            <ExternalLink className="size-3.5" />
            Open Raw HTML
          </a>
        </Button>
      </div>

      {/* All pages list */}
      {pages.length > 1 && (
        <div className="border-t border-slate-100 p-3 dark:border-slate-800">
          <h3 className="mb-2 text-xs font-bold uppercase tracking-wider text-slate-500">
            All Pages
          </h3>
          <div className="flex max-h-48 flex-col gap-0.5 overflow-y-auto">
            {pages.map((p, idx) => (
              <button
                key={p.id}
                onClick={() => onNavigate(p)}
                className={cn(
                  "flex items-center gap-2 rounded px-1.5 py-1 text-left text-xs transition-colors hover:bg-slate-50 dark:hover:bg-slate-800",
                  p.id === note.id ? "font-semibold text-red-600 dark:text-red-400" : "text-slate-500"
                )}
              >
                <span className="w-5 shrink-0 tabular-nums">{String(idx + 1).padStart(2, "0")}.</span>
                <span className="truncate">{p.title}</span>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Back to notes */}
      <div className="mt-auto border-t border-slate-100 p-3 dark:border-slate-800">
        <Button variant="ghost" size="sm" onClick={goHome} className="w-full justify-start gap-2 text-xs text-slate-600 dark:text-slate-400">
          <ChevronLeft className="size-3.5" />
          Back to Notes
        </Button>
      </div>
    </div>
  );
}

// ─── Helper Components ─────────────────────────────────────────

function ActionButton({
  icon: Icon,
  label,
  textColor,
}: {
  icon: React.ElementType;
  label: string;
  textColor?: string;
}) {
  return (
    <button className="flex w-full items-center gap-2.5 rounded-md px-3 py-2 text-left text-sm transition-colors hover:bg-slate-50 dark:hover:bg-slate-800">
      <Icon className={cn("size-4", textColor ?? "text-slate-500")} />
      <span className={textColor ?? "text-slate-700 dark:text-slate-300"}>{label}</span>
    </button>
  );
}

function ExportSection({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="mb-1">
      <div className="px-2 py-1 text-[10px] font-bold uppercase tracking-wider text-slate-400">{title}</div>
      {children}
    </div>
  );
}

function ExportItem({
  icon: Icon,
  label,
  onClick,
}: {
  icon: React.ElementType;
  label: string;
  onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      className="flex w-full items-center gap-2 rounded-md px-2 py-1.5 text-left text-xs text-slate-700 transition-colors hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800"
    >
      <Icon className="size-3.5 text-slate-400" />
      {label}
    </button>
  );
}
