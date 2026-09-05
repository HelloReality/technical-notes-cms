"use client";

import * as React from "react";
import {
  ArrowLeft,
  ArrowRight,
  ChevronLeft,
  ChevronRight,
  Clock,
  ExternalLink,
  Grid2x2,
  Home,
  List,
  Maximize,
  Maximize2,
  Minimize2,
  PanelLeft,
  PanelRight,
  Search,
  Share2,
  Tag,
  ZoomIn,
  ZoomOut,
} from "lucide-react";

import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { Input } from "@/components/ui/input";
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb";
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
  const [sidebarMode, setSidebarMode] = React.useState<SidebarMode>("list");
  const [rightPanelOpen, setRightPanelOpen] = React.useState(true);
  const [topBarCollapsed, setTopBarCollapsed] = React.useState(false);
  const [zoom, setZoom] = React.useState(1);
  const [isFullscreen, setIsFullscreen] = React.useState(false);
  const [sidebarSearch, setSidebarSearch] = React.useState("");
  const iframeRef = React.useRef<HTMLIFrameElement>(null);
  const readerRef = React.useRef<HTMLDivElement>(null);

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

  // Keyboard navigation
  React.useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return;
      if (e.key === "ArrowLeft" && prevPage) {
        e.preventDefault();
        openNote(prevPage);
      } else if (e.key === "ArrowRight" && nextPage) {
        e.preventDefault();
        openNote(nextPage);
      } else if (e.key === "Escape" && isFullscreen) {
        document.exitFullscreen?.();
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [prevPage, nextPage, openNote, isFullscreen]);

  // Inject CSS into iframe for binding visibility + zoom
  const handleIframeLoad = React.useCallback((e: React.SyntheticEvent<HTMLIFrameElement>) => {
    try {
      const iframe = e.currentTarget;
      const doc = iframe.contentDocument;
      if (!doc) return;
      const style = doc.createElement("style");
      style.textContent = `
        body {
          justify-content: flex-start !important;
          padding-left: 42px !important;
          padding-right: 14px !important;
          zoom: ${zoom} !important;
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
      // sandbox restriction
    }
  }, [zoom]);

  const category = note?.category;
  const subcategory = note?.subcategory ?? (category?.parentId ? category : null);
  const topCategory = category && category.parentId ? null : category;

  if (loading || !note) {
    return (
      <div className="flex flex-1 items-center justify-center p-12">
        <Skeleton className="h-[60vh] w-full rounded-xl" />
      </div>
    );
  }

  return (
    <div ref={readerRef} className="flex h-[calc(100vh-4rem)] flex-col bg-background">
      {/* ═══ Top Control Bar ═══ */}
      <div className={cn(
        "border-b border-border/60 bg-background/95 backdrop-blur transition-all duration-200",
        topBarCollapsed ? "h-10" : "h-14"
      )}>
        <div className="flex h-full items-center gap-2 px-3">
          {/* Back home */}
          <Button variant="ghost" size="icon" onClick={goHome} className="size-8 shrink-0" title="Back to home">
            <Home className="size-4" />
          </Button>

          {/* Toggle sidebar */}
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className={cn("size-8 shrink-0", sidebarOpen && "bg-accent")}
            title="Toggle page navigation"
          >
            <PanelLeft className="size-4" />
          </Button>

          {/* Breadcrumb */}
          <div className="hidden min-w-0 flex-1 items-center gap-1 text-sm md:flex">
            {topCategory && (
              <span className="text-muted-foreground">{topCategory.name}</span>
            )}
            {subcategory && subcategory.id !== topCategory?.id && (
              <>
                <ChevronRight className="size-3 text-muted-foreground" />
                <span className="text-muted-foreground">{subcategory.name}</span>
              </>
            )}
            <ChevronRight className="size-3 text-muted-foreground" />
            <span className="truncate font-medium">{note.title}</span>
            {pages.length > 1 && (
              <span className="ml-2 text-xs text-muted-foreground">
                Page {currentIndex + 1} of {pages.length}
              </span>
            )}
          </div>

          {/* Spacer for mobile */}
          <div className="flex-1 md:hidden" />

          {/* Zoom controls */}
          <div className="hidden items-center gap-0.5 sm:flex">
            <Button
              variant="ghost"
              size="icon"
              className="size-8"
              onClick={() => setZoom(Math.max(0.5, zoom - 0.1))}
              title="Zoom out"
            >
              <ZoomOut className="size-4" />
            </Button>
            <span className="w-12 text-center text-xs tabular-nums text-muted-foreground">
              {Math.round(zoom * 100)}%
            </span>
            <Button
              variant="ghost"
              size="icon"
              className="size-8"
              onClick={() => setZoom(Math.min(2, zoom + 0.1))}
              title="Zoom in"
            >
              <ZoomIn className="size-4" />
            </Button>
          </div>

          {/* Right panel toggle */}
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setRightPanelOpen(!rightPanelOpen)}
            className={cn("size-8", rightPanelOpen && "bg-accent")}
            title="Toggle info panel"
          >
            <PanelRight className="size-4" />
          </Button>

          {/* Fullscreen */}
          <Button
            variant="ghost"
            size="icon"
            onClick={toggleFullscreen}
            className="size-8 shrink-0"
            title={isFullscreen ? "Exit fullscreen" : "Enter fullscreen"}
          >
            {isFullscreen ? <Minimize2 className="size-4" /> : <Maximize2 className="size-4" />}
          </Button>

          {/* Collapse/expand top bar */}
          <Button
            variant="ghost"
            size="icon"
            className="size-8 shrink-0"
            onClick={() => setTopBarCollapsed(!topBarCollapsed)}
            title={topBarCollapsed ? "Expand toolbar" : "Collapse toolbar"}
          >
            <ChevronLeft className={cn("size-4 transition-transform", topBarCollapsed && "rotate-180")} />
          </Button>
        </div>
      </div>

      {/* ═══ Main Reader Area ═══ */}
      <div className="flex min-h-0 flex-1">
        {/* ─── Left Sidebar (Page Navigation) ─── */}
        {sidebarOpen && (
          <aside className="flex w-64 shrink-0 flex-col border-r border-border/60 bg-background md:w-72">
            {/* Sidebar header */}
            <div className="flex items-center justify-between border-b border-border/60 px-3 py-2">
              <span className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                Pages ({pages.length})
              </span>
              <div className="flex items-center gap-0.5">
                <Button
                  variant="ghost"
                  size="icon"
                  className={cn("size-7", sidebarMode === "list" && "bg-accent")}
                  onClick={() => setSidebarMode("list")}
                  title="List view"
                >
                  <List className="size-3.5" />
                </Button>
                <Button
                  variant="ghost"
                  size="icon"
                  className={cn("size-7", sidebarMode === "tile" && "bg-accent")}
                  onClick={() => setSidebarMode("tile")}
                  title="Grid view"
                >
                  <Grid2x2 className="size-3.5" />
                </Button>
              </div>
            </div>

            {/* Search within pages */}
            {pages.length > 3 && (
              <div className="border-b border-border/60 px-2 py-2">
                <div className="relative">
                  <Search className="pointer-events-none absolute left-2.5 top-1/2 size-3.5 -translate-y-1/2 text-muted-foreground" />
                  <Input
                    value={sidebarSearch}
                    onChange={(e) => setSidebarSearch(e.target.value)}
                    placeholder="Filter pages…"
                    className="h-8 pl-8 text-xs"
                  />
                </div>
              </div>
            )}

            {/* Page list */}
            <ScrollArea className="flex-1">
              {sidebarMode === "list" ? (
                <PageListView
                  pages={filteredPages}
                  currentPageId={note.id}
                  onNavigate={openNote}
                />
              ) : (
                <PageTileView
                  pages={filteredPages}
                  currentPageId={note.id}
                  onNavigate={openNote}
                />
              )}
            </ScrollArea>

            {/* Prev/Next at bottom */}
            {pages.length > 1 && (
              <div className="flex items-center justify-between border-t border-border/60 px-2 py-2">
                <Button
                  variant="ghost"
                  size="sm"
                  disabled={!prevPage}
                  onClick={() => prevPage && openNote(prevPage)}
                  className="gap-1 text-xs"
                >
                  <ChevronLeft className="size-3.5" />
                  Prev
                </Button>
                <span className="text-xs tabular-nums text-muted-foreground">
                  {currentIndex + 1}/{pages.length}
                </span>
                <Button
                  variant="ghost"
                  size="sm"
                  disabled={!nextPage}
                  onClick={() => nextPage && openNote(nextPage)}
                  className="gap-1 text-xs"
                >
                  Next
                  <ChevronRight className="size-3.5" />
                </Button>
              </div>
            )}
          </aside>
        )}

        {/* ─── Reading Area ─── */}
        <div className="flex min-w-0 flex-1 flex-col">
          {/* Note header */}
          <div className="border-b border-border/60 px-4 py-3 md:px-6">
            <div className="mb-1.5 flex flex-wrap items-center gap-2 text-xs text-muted-foreground">
              {topCategory && (
                <Badge variant="outline" className="border-emerald-500/30 bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300">
                  {topCategory.name}
                </Badge>
              )}
              {subcategory && subcategory.id !== topCategory?.id && (
                <Badge variant="secondary">{subcategory.name}</Badge>
              )}
              <span className="flex items-center gap-1">
                <Clock className="size-3" />
                {fromNow(note.updatedAt)}
              </span>
            </div>
            <h1 className="text-xl font-bold tracking-tight md:text-2xl">{note.title}</h1>
            {note.description && (
              <p className="mt-1 text-sm text-muted-foreground">{note.description}</p>
            )}
          </div>

          {/* Iframe content */}
          <div className="flex-1 overflow-auto bg-muted/20 p-2 md:p-4">
            <div className="mx-auto overflow-x-auto rounded-xl border border-border/60 bg-white shadow-sm dark:bg-white" style={{ maxWidth: `${1080 + 56}px` }}>
              <iframe
                ref={iframeRef}
                title={note.title}
                className="note-iframe"
                style={{ minHeight: "60vh", transform: `scale(${zoom})`, transformOrigin: "top left", width: `${100 / zoom}%` }}
                src={note.contentPath}
                sandbox="allow-same-origin allow-popups"
                onLoad={handleIframeLoad}
              />
            </div>
          </div>

          {/* Bottom prev/next bar */}
          {pages.length > 1 && (
            <div className="flex items-center justify-between border-t border-border/60 px-4 py-2">
              {prevPage ? (
                <Button variant="ghost" size="sm" onClick={() => openNote(prevPage)} className="gap-1.5">
                  <ChevronLeft className="size-4" />
                  <span className="hidden sm:inline max-w-[200px] truncate">{prevPage.title}</span>
                  <span className="sm:hidden">Prev</span>
                </Button>
              ) : (
                <div />
              )}
              {nextPage ? (
                <Button variant="ghost" size="sm" onClick={() => openNote(nextPage)} className="gap-1.5">
                  <span className="hidden sm:inline max-w-[200px] truncate">{nextPage.title}</span>
                  <span className="sm:hidden">Next</span>
                  <ChevronRight className="size-4" />
                </Button>
              ) : (
                <div />
              )}
            </div>
          )}
        </div>

        {/* ─── Right Floating Panel ─── */}
        {rightPanelOpen && (
          <aside className="hidden w-60 shrink-0 flex-col border-l border-border/60 bg-background lg:flex">
            <RightPanel
              note={note}
              pages={pages}
              currentIndex={currentIndex}
              onNavigate={openNote}
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
              "flex items-start gap-2.5 px-3 py-2 text-left transition-colors hover:bg-accent/50",
              isActive && "bg-emerald-50 dark:bg-emerald-950/30"
            )}
          >
            <span
              className={cn(
                "mt-0.5 flex size-6 shrink-0 items-center justify-center rounded text-xs font-medium tabular-nums",
                isActive
                  ? "bg-emerald-600 text-white"
                  : "bg-muted text-muted-foreground"
              )}
            >
              {idx + 1}
            </span>
            <div className="min-w-0 flex-1">
              <p className={cn(
                "truncate text-sm leading-tight",
                isActive ? "font-semibold text-emerald-700 dark:text-emerald-300" : "text-foreground"
              )}>
                {page.title}
              </p>
              {page.description && (
                <p className="mt-0.5 truncate text-xs text-muted-foreground">
                  {page.description}
                </p>
              )}
            </div>
            {isActive && (
              <span className="mt-1 size-2 shrink-0 rounded-full bg-emerald-500" />
            )}
          </button>
        );
      })}
    </div>
  );
}

// ─── Page Tile View ───────────────────────────────────────────
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
              "group flex flex-col gap-1.5 rounded-lg border p-2.5 text-left transition-all hover:shadow-md",
              isActive
                ? "border-emerald-500 bg-emerald-50 dark:bg-emerald-950/30"
                : "border-border/60 bg-card hover:border-border"
            )}
          >
            {/* Thumbnail placeholder */}
            <div className={cn(
              "flex aspect-[4/3] items-center justify-center rounded-md",
              isActive ? "bg-emerald-100 dark:bg-emerald-900/40" : "bg-muted"
            )}>
              <span className={cn(
                "text-lg font-bold tabular-nums",
                isActive ? "text-emerald-600 dark:text-emerald-400" : "text-muted-foreground"
              )}>
                {idx + 1}
              </span>
            </div>
            <p className={cn(
              "line-clamp-2 text-xs leading-tight",
              isActive ? "font-semibold text-emerald-700 dark:text-emerald-300" : "text-foreground"
            )}>
              {page.title}
            </p>
          </button>
        );
      })}
    </div>
  );
}

// ─── Right Contextual Panel ──────────────────────────────────
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
      {/* Note info */}
      <div className="border-b border-border/60 p-3">
        <h3 className="mb-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
          Note Info
        </h3>
        <div className="flex flex-col gap-1.5 text-xs">
          <div className="flex items-center gap-1.5 text-muted-foreground">
            <Clock className="size-3" />
            <span>Updated {fromNow(note.updatedAt)}</span>
          </div>
          <div className="text-muted-foreground">
            {formatDateTime(note.updatedAt)}
          </div>
        </div>
        {note.tags && note.tags.length > 0 && (
          <div className="mt-3 flex flex-wrap gap-1">
            {note.tags.map((t) => (
              <Badge key={t.id} variant="outline" className="text-[10px] font-normal">
                <Tag className="mr-1 size-2.5" />
                {t.name}
              </Badge>
            ))}
          </div>
        )}
      </div>

      {/* Quick navigation */}
      {pages.length > 1 && (
        <div className="border-b border-border/60 p-3">
          <h3 className="mb-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
            Quick Navigate
          </h3>
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              disabled={currentIndex === 0}
              onClick={() => onNavigate(pages[0])}
              className="h-7 gap-1 text-xs"
            >
              <ChevronLeft className="size-3" />
              First
            </Button>
            <span className="text-xs tabular-nums text-muted-foreground">
              {currentIndex + 1}/{pages.length}
            </span>
            <Button
              variant="outline"
              size="sm"
              disabled={currentIndex === pages.length - 1}
              onClick={() => onNavigate(pages[pages.length - 1])}
              className="h-7 gap-1 text-xs"
            >
              Last
              <ChevronRight className="size-3" />
            </Button>
          </div>
        </div>
      )}

      {/* Actions */}
      <div className="border-b border-border/60 p-3">
        <h3 className="mb-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
          Actions
        </h3>
        <div className="flex flex-col gap-1.5">
          <Button variant="ghost" size="sm" className="justify-start gap-2 text-xs" onClick={handleShare}>
            <Share2 className="size-3.5" />
            {copied ? "Link Copied!" : "Copy Link"}
          </Button>
          <Button variant="ghost" size="sm" asChild className="justify-start gap-2 text-xs">
            <a href={note.contentPath} target="_blank" rel="noopener noreferrer">
              <ExternalLink className="size-3.5" />
              Open Raw HTML
            </a>
          </Button>
          <Button variant="ghost" size="sm" onClick={goHome} className="justify-start gap-2 text-xs">
            <Home className="size-3.5" />
            Back to Home
          </Button>
        </div>
      </div>

      {/* Page index */}
      {pages.length > 1 && (
        <div className="p-3">
          <h3 className="mb-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
            All Pages
          </h3>
          <div className="flex max-h-48 flex-col gap-0.5 overflow-y-auto">
            {pages.map((p, idx) => (
              <button
                key={p.id}
                onClick={() => onNavigate(p)}
                className={cn(
                  "flex items-center gap-2 rounded px-1.5 py-1 text-left text-xs transition-colors hover:bg-accent/50",
                  p.id === note.id ? "font-semibold text-emerald-600 dark:text-emerald-400" : "text-muted-foreground"
                )}
              >
                <span className="w-4 shrink-0 tabular-nums">{idx + 1}.</span>
                <span className="truncate">{p.title}</span>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

// ─── ScrollArea wrapper (using a simple div with overflow) ────
function ScrollArea({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    <div className={cn("overflow-y-auto", className)} style={{ scrollbarWidth: "thin" }}>
      {children}
    </div>
  );
}
