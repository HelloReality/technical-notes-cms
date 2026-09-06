"use client";

import * as React from "react";
import {
  ChevronDown,
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
  Layers,
  List,
  Maximize,
  Menu,
  Minimize,
  MoreVertical,
  Send,
  Share2,
  Upload,
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
import type { Note } from "@/lib/types";
import { cn } from "@/lib/utils";

type SidebarMode = "tile" | "list";

export function NoteViewer() {
  const note = useAppStore((s) => s.selectedNote);
  const loading = useAppStore((s) => s.noteLoading);
  const allNotes = useAppStore((s) => s.notes);
  const openNote = useAppStore((s) => s.openNote);
  const goHome = useAppStore((s) => s.goHome);

  // ─── State ───
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

  const containerRef = React.useRef<HTMLDivElement>(null);
  const downloadRef = React.useRef<HTMLDivElement>(null);
  const zoomRef = React.useRef<HTMLDivElement>(null);

  // ─── Pages (notes in same category) ───
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
    openNote(page);
    setDrawerOpen(false);
  }, [openNote]);

  // ─── Fit-to-view zoom ───
  const computeFitScale = React.useCallback(() => {
    const el = containerRef.current;
    if (!el) return;
    const w = el.clientWidth - 64;
    const h = el.clientHeight - 64;
    if (w <= 0 || h <= 0) return;
    // target: fit 1080px wide content
    const scaleW = w / 1136; // 1080 + 56 padding
    const fit = Math.min(scaleW, 1);
    setZoom(Math.max(0.25, fit));
  }, []);

  React.useEffect(() => {
    if (zoomMode === "fit") {
      const t = setTimeout(computeFitScale, 50);
      return () => clearTimeout(t);
    }
  }, [note, zoomMode, computeFitScale, drawerOpen]);

  React.useEffect(() => {
    if (zoomMode !== "fit") return;
    const handler = () => computeFitScale();
    window.addEventListener("resize", handler);
    return () => window.removeEventListener("resize", handler);
  }, [zoomMode, computeFitScale]);

  // ─── Fullscreen ───
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

  // ─── Close popovers on outside click ───
  React.useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (downloadOpen && downloadRef.current && !downloadRef.current.contains(e.target as Node)) setDownloadOpen(false);
      if (zoomPresetsOpen && zoomRef.current && !zoomRef.current.contains(e.target as Node)) setZoomPresetsOpen(false);
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, [downloadOpen, zoomPresetsOpen]);

  // ─── Keyboard shortcuts ───
  React.useEffect(() => {
    const handleKey = (e: KeyboardEvent) => {
      const target = e.target as HTMLElement;
      const isTyping = target.tagName === "INPUT" || target.tagName === "TEXTAREA";

      if (e.key === "Escape") {
        if (drawerOpen) { setDrawerOpen(false); return; }
        if (downloadOpen) { setDownloadOpen(false); return; }
        if (actionsOpen) { setActionsOpen(false); return; }
        if (zoomPresetsOpen) { setZoomPresetsOpen(false); return; }
        setToolbarExpanded(false);
      }

      if ((e.ctrlKey || e.metaKey) && (e.key === "+" || e.key === "=")) {
        e.preventDefault();
        setZoomMode("manual");
        setZoom(z => Math.min(4, z + 0.1));
        return;
      }
      if ((e.ctrlKey || e.metaKey) && e.key === "-") {
        e.preventDefault();
        setZoomMode("manual");
        setZoom(z => Math.max(0.25, z - 0.1));
        return;
      }
      if ((e.ctrlKey || e.metaKey) && e.key === "0") {
        e.preventDefault();
        setZoomMode("fit");
        computeFitScale();
        return;
      }

      if (isTyping) return;

      if (e.key === "ArrowLeft" && !drawerOpen && prevPage) {
        e.preventDefault();
        handleNavigate(prevPage);
      }
      if (e.key === "ArrowRight" && !drawerOpen && nextPage) {
        e.preventDefault();
        handleNavigate(nextPage);
      }
    };
    window.addEventListener("keydown", handleKey);
    return () => window.removeEventListener("keydown", handleKey);
  }, [drawerOpen, downloadOpen, actionsOpen, zoomPresetsOpen, prevPage, nextPage, handleNavigate, computeFitScale]);

  // ─── Iframe load: inject padding + auto-resize ───
  const handleIframeLoad = React.useCallback((e: React.SyntheticEvent<HTMLIFrameElement>) => {
    try {
      const iframe = e.currentTarget;
      const doc = iframe.contentDocument;
      if (!doc) return;
      const existing = doc.getElementById("reader-style");
      if (existing) existing.remove();
      const style = doc.createElement("style");
      style.id = "reader-style";
      style.textContent = `
        body { justify-content: flex-start !important; padding-left: 42px !important; padding-right: 14px !important; }
        @media (max-width: 1120px) { html { overflow-x: auto; } }
      `;
      doc.head.appendChild(style);
      const resize = () => {
        const h = Math.max(doc.body.scrollHeight, doc.body.offsetHeight, doc.documentElement.scrollHeight, doc.documentElement.offsetHeight);
        iframe.style.height = `${h + 20}px`;
      };
      resize();
      setTimeout(resize, 500);
      setTimeout(resize, 1500);
    } catch { /* sandbox */ }
  }, []);

  const handleShare = () => {
    navigator.clipboard?.writeText(window.location.href).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  // ─── Render ───
  if (loading) {
    return (
      <div className="flex h-screen items-center justify-center bg-slate-800">
        <Skeleton className="h-[60vh] w-full max-w-4xl rounded-xl" />
      </div>
    );
  }

  if (!note) {
    return (
      <div className="flex h-screen flex-col items-center justify-center gap-4 bg-slate-800 text-center text-slate-200">
        <div className="flex size-16 items-center justify-center rounded-full bg-slate-700">
          <Home className="size-8 text-slate-400" />
        </div>
        <div>
          <h2 className="text-xl font-bold text-white">Note not found</h2>
          <p className="mt-1 text-sm text-slate-400">The note doesn't exist or is no longer published.</p>
        </div>
        <Button onClick={goHome} className="gap-2">
          <Home className="size-4" /> Browse all notes
        </Button>
      </div>
    );
  }

  const zoomLabel = zoomMode === "fit" ? "Fit" : `${Math.round(zoom * 100)}%`;

  return (
    <div ref={containerRef} className="relative h-screen w-full overflow-hidden bg-slate-800">
      {/* ═══ Top-left: Home button + Breadcrumb ═══ */}
      <div className="absolute left-3 top-3 z-30 flex items-center gap-2">
        <button
          onClick={goHome}
          className="flex h-9 w-9 items-center justify-center rounded-full border border-slate-200 bg-white/95 text-slate-600 shadow-md backdrop-blur-sm transition-colors hover:bg-white hover:text-slate-900"
          title="Back to home"
        >
          <Home className="h-4 w-4" />
        </button>
        {/* Breadcrumb directory */}
        <div className="hidden items-center gap-1.5 rounded-full border border-slate-200 bg-white/95 px-3 py-1.5 text-xs text-slate-500 shadow-md backdrop-blur-sm sm:flex">
          {note.category && (
            <>
              <span className="text-slate-400">{note.category.name}</span>
              <ChevronRight className="h-3 w-3 text-slate-300" />
            </>
          )}
          <span className="max-w-[200px] truncate text-slate-700">{note.title}</span>
          {totalPages > 1 && (
            <span className="ml-1 text-slate-400">· {currentIndex + 1}/{totalPages}</span>
          )}
        </div>
      </div>

      {/* ═══ Top-right: Pages sidebar toggle + Actions toggle ═══ */}
      <div className="absolute right-3 top-3 z-30 flex items-center gap-2">
        <button
          onClick={() => setDrawerOpen(true)}
          className="flex h-9 w-9 items-center justify-center rounded-full border border-slate-200 bg-white/95 text-slate-600 shadow-md backdrop-blur-sm transition-colors hover:bg-white hover:text-slate-900"
          title="Open pages"
        >
          <Menu className="h-4 w-4" />
        </button>
        <button
          onClick={() => setActionsOpen(!actionsOpen)}
          className={cn(
            "flex h-9 w-9 items-center justify-center rounded-full border border-slate-200 shadow-md backdrop-blur-sm transition-colors",
            actionsOpen ? "bg-white text-slate-900" : "bg-white/95 text-slate-600 hover:bg-white hover:text-slate-900"
          )}
          title="Toggle actions"
        >
          <MoreVertical className="h-4 w-4" />
        </button>
      </div>
      <div className="absolute inset-0 overflow-auto">
        <div className="flex min-h-full items-start justify-center p-4 sm:p-8">
          <div
            className="overflow-x-auto rounded-xl bg-white shadow-2xl"
            style={{ maxWidth: `${1080 + 56}px`, width: "100%" }}
          >
            <iframe
              title={note.title}
              className="block"
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
      </div>

      {/* ═══ Top Floating Toolbar ═══ */}
      {toolbarExpanded ? (
        <div className="absolute left-1/2 top-3 z-30 -translate-x-1/2">
          <div className="flex items-center gap-1 rounded-full border border-slate-200 bg-white/95 px-2 py-1.5 shadow-lg backdrop-blur-md">
            {/* Download */}
            <div className="relative" ref={downloadRef}>
              <Button
                variant="ghost" size="icon"
                className={cn("h-8 w-8 rounded-full", downloadOpen && "bg-slate-100")}
                onClick={() => setDownloadOpen(!downloadOpen)}
                title="Export"
              >
                <Download className="h-4 w-4" />
              </Button>
              {downloadOpen && (
                <div className="absolute left-0 top-full mt-2 w-56 rounded-lg border border-slate-200 bg-white p-1 shadow-xl">
                  <div className="px-2 py-1 text-[10px] font-bold uppercase tracking-wider text-slate-400">
                    Current Page ({currentIndex + 1})
                  </div>
                  {["PNG", "JPEG", "PDF"].map(fmt => (
                    <button key={fmt} onClick={() => setDownloadOpen(false)}
                      className="flex w-full items-center gap-2 rounded-md px-2 py-1.5 text-xs text-slate-700 hover:bg-slate-100">
                      <FileImage className="h-3.5 w-3.5 text-slate-400" /> {fmt}
                    </button>
                  ))}
                  <div className="my-1 h-px bg-slate-100" />
                  <div className="px-2 py-1 text-[10px] font-bold uppercase tracking-wider text-slate-400">All Pages</div>
                  {["PDF", "PNG (ZIP)"].map(fmt => (
                    <button key={fmt} onClick={() => setDownloadOpen(false)}
                      className="flex w-full items-center gap-2 rounded-md px-2 py-1.5 text-xs text-slate-700 hover:bg-slate-100">
                      <FileText className="h-3.5 w-3.5 text-slate-400" /> {fmt}
                    </button>
                  ))}
                </div>
              )}
            </div>

            <Sep />

            {/* Prev / page indicator / Next */}
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
              {zoomPresetsOpen && (
                <div className="absolute left-1/2 top-full mt-2 w-40 -translate-x-1/2 rounded-lg border border-slate-200 bg-white p-1 shadow-xl">
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
                </div>
              )}
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
        </div>
      ) : (
        <button
          className="absolute left-1/2 top-2 z-30 flex -translate-x-1/2 items-center gap-1.5 rounded-full border border-slate-200 bg-white/95 px-4 py-1.5 text-xs text-slate-600 shadow-md backdrop-blur-sm transition-colors hover:bg-white"
          onClick={() => setToolbarExpanded(true)}
          title="Expand toolbar"
        >
          <ChevronDown className="h-3 w-3" />
          <span className="font-mono">{currentIndex + 1}/{totalPages}</span>
        </button>
      )}

      {/* ═══ Left Pages Sidebar (overlay drawer) ═══ */}
      {drawerOpen && (
        <>
          {/* Backdrop */}
          <div className="absolute inset-0 z-30 bg-black/30" onClick={() => setDrawerOpen(false)} />
          <div className="absolute bottom-0 left-0 top-0 z-40 flex w-[85vw] flex-col bg-white shadow-2xl sm:w-80 sm:max-w-[320px]">
          {/* Header */}
          <div className="flex items-center justify-between border-b border-slate-200 px-4 py-3">
            <span className="text-sm font-semibold text-slate-900">Pages</span>
            <button onClick={() => setDrawerOpen(false)}
              className="rounded p-1 text-slate-400 hover:bg-slate-100 hover:text-slate-600">
              <X className="h-4 w-4" />
            </button>
          </div>
          {/* List/Tiles toggle */}
          <div className="border-b border-slate-200 px-4 py-2">
            <div className="flex w-fit items-center gap-0.5 rounded-md bg-slate-100 p-0.5">
              <button className={cn("rounded px-3 py-1 text-xs", pageViewMode === "list" ? "bg-white font-semibold shadow-sm" : "text-slate-500")}
                onClick={() => setPageViewMode("list")}>List</button>
              <button className={cn("rounded px-3 py-1 text-xs", pageViewMode === "tiles" ? "bg-white font-semibold shadow-sm" : "text-slate-500")}
                onClick={() => setPageViewMode("tiles")}>Tiles</button>
            </div>
          </div>
          {/* Content */}
          <ScrollArea className="flex-1">
            {pageViewMode === "list" ? (
              <div className="space-y-0.5 p-3">
                {pages.map((page, idx) => (
                  <button key={page.id} onClick={() => handleNavigate(page)}
                    className={cn("flex w-full items-center rounded-lg border px-3 py-2.5 text-left",
                      idx === currentIndex ? "border-rose-200 bg-rose-50" : "border-transparent hover:bg-slate-50")}>
                    <span className={cn("mr-3 font-mono text-xs", idx === currentIndex ? "font-bold text-rose-600" : "text-slate-400")}>
                      {String(idx + 1).padStart(2, "0")}
                    </span>
                    <span className={cn("truncate text-sm", idx === currentIndex ? "font-medium text-rose-900" : "text-slate-700")}>
                      {page.title}
                    </span>
                  </button>
                ))}
              </div>
            ) : (
              <div className="grid grid-cols-2 gap-2 p-3">
                {pages.map((page, idx) => (
                  <button key={page.id} onClick={() => handleNavigate(page)}
                    className={cn("overflow-hidden rounded-lg border-2 text-left",
                      idx === currentIndex ? "border-rose-400 shadow-md" : "border-slate-200 hover:border-slate-300")}>
                    <div className="border-b border-slate-100 bg-slate-50 px-2 py-1 text-center text-[10px] font-semibold">
                      {String(idx + 1).padStart(2, "0")}
                    </div>
                    {/* Real page preview via iframe */}
                    <div className="relative aspect-[3/4] overflow-hidden bg-white">
                      <iframe
                        src={page.contentPath}
                        className="pointer-events-none absolute left-0 top-0 border-0"
                        style={{
                          width: "1080px",
                          height: "1440px",
                          transform: "scale(0.12)",
                          transformOrigin: "top left",
                        }}
                        sandbox="allow-same-origin"
                        title={page.title}
                      />
                    </div>
                    <div className="truncate border-t border-slate-100 bg-slate-50 px-2 py-1 text-[10px] text-slate-600">
                      {page.title}
                    </div>
                  </button>
                ))}
              </div>
            )}
          </ScrollArea>
          </div>
        </>
      )}

      {/* ═══ Right Actions Panel ═══ */}
      {actionsOpen && (
        <div className="absolute right-3 top-16 z-30 w-44 rounded-xl border border-slate-200 bg-white/95 p-3 shadow-lg backdrop-blur-md">
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
          {/* Note info */}
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
        </div>
      )}
    </div>
  );
}

// ─── Helper components ────────────────────────────────────────

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
    <button onClick={onClick}
      className="flex w-full items-center gap-2.5 rounded-md px-3 py-2 text-left text-sm transition-colors hover:bg-slate-50">
      <Icon className={cn("h-4 w-4", textColor ?? "text-slate-500")} />
      <span className={textColor ?? "text-slate-700"}>{label}</span>
    </button>
  );
}
