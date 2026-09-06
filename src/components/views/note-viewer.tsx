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
  Home,
  Maximize,
  Menu,
  Minimize,
  MoreVertical,
  PanelLeftClose,
  PanelLeftOpen,
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

type SidebarMode = "list" | "tile";

// ─── Tree node type ───────────────────────────────────────────
interface TreeNode {
  category: Category;
  topics: { category: Category; notes: Note[] }[];
  notes: Note[];
}

function buildTree(categories: Category[], notes: Note[]): TreeNode[] {
  const top = categories.filter((c) => !c.parentId);
  return top.map((cat) => {
    const topics = categories
      .filter((c) => c.parentId === cat.id)
      .map((sub) => ({
        category: sub,
        notes: notes
          .filter((n) => n.categoryId === sub.id)
          .sort((a, b) => new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime()),
      }))
      .filter((t) => t.notes.length > 0);
    const directNotes = notes
      .filter((n) => n.categoryId === cat.id)
      .sort((a, b) => new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime());
    return { category: cat, topics, notes: directNotes };
  }).filter((n) => n.topics.length > 0 || n.notes.length > 0);
}

// ─── Main NoteViewer ──────────────────────────────────────────
export function NoteViewer() {
  const note = useAppStore((s) => s.selectedNote);
  const loading = useAppStore((s) => s.noteLoading);
  const allNotes = useAppStore((s) => s.notes);
  const allCategories = useAppStore((s) => s.categories);
  const openNote = useAppStore((s) => s.openNote);
  const goHome = useAppStore((s) => s.goHome);

  // Sidebar state
  const [sidebarCollapsed, setSidebarCollapsed] = React.useState(false);
  const [mobileSidebarOpen, setMobileSidebarOpen] = React.useState(false);
  const [sidebarMode, setSidebarMode] = React.useState<SidebarMode>("list");
  const [expandedCats, setExpandedCats] = React.useState<Set<string>>(new Set());
  const [expandedTopics, setExpandedTopics] = React.useState<Set<string>>(new Set());
  const [sidebarSearch, setSidebarSearch] = React.useState("");

  // Toolbar / right panel
  const [toolbarExpanded, setToolbarExpanded] = React.useState(true);
  const [rightPanelOpen, setRightPanelOpen] = React.useState(false);
  const [downloadOpen, setDownloadOpen] = React.useState(false);
  const [zoomPresetsOpen, setZoomPresetsOpen] = React.useState(false);
  const [zoom, setZoom] = React.useState(1);
  const [zoomMode, setZoomMode] = React.useState<"fit" | "manual">("fit");
  const [isFullscreen, setIsFullscreen] = React.useState(false);
  const [copied, setCopied] = React.useState(false);
  const [pageInputValue, setPageInputValue] = React.useState("");
  const [pageInputFocused, setPageInputFocused] = React.useState(false);

  const containerRef = React.useRef<HTMLDivElement>(null);
  const downloadRef = React.useRef<HTMLDivElement>(null);
  const zoomRef = React.useRef<HTMLDivElement>(null);

  // ─── Build tree ─────────────────────────────────────────────
  const tree = React.useMemo(() => buildTree(allCategories, allNotes), [allCategories, allNotes]);

  // ─── Pages in current category ─────────────────────────────
  const pages = React.useMemo(() => {
    if (!note) return [];
    const noteCat = allCategories.find((c) => c.id === note.categoryId);
    if (!noteCat) return [note];
    if (noteCat.parentId) {
      return allNotes
        .filter((n) => n.categoryId === noteCat.id)
        .sort((a, b) => new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime());
    }
    const subIds = allCategories.filter((c) => c.parentId === noteCat.id).map((c) => c.id);
    return allNotes
      .filter((n) => n.categoryId === noteCat.id || subIds.includes(n.categoryId))
      .sort((a, b) => new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime());
  }, [allNotes, allCategories, note]);

  const currentIndex = React.useMemo(() => note ? pages.findIndex((p) => p.id === note.id) : -1, [pages, note]);
  const totalPages = pages.length;
  const prevPage = currentIndex > 0 ? pages[currentIndex - 1] : null;
  const nextPage = currentIndex < totalPages - 1 ? pages[currentIndex + 1] : null;

  const relatedNotes = React.useMemo(() => {
    if (!note) return [];
    return allNotes
      .filter((n) => n.id !== note.id && (n.categoryId === note.categoryId || n.tags?.some((t) => note.tags?.some((nt) => nt.id === t.id))))
      .slice(0, 5);
  }, [allNotes, note]);

  // ─── Auto-expand active category ───────────────────────────
  React.useEffect(() => {
    if (!note) return;
    const noteCat = allCategories.find((c) => c.id === note.categoryId);
    if (!noteCat) return;
    const parentId = noteCat.parentId ?? noteCat.id;
    setExpandedCats((prev) => new Set([...prev, parentId]));
    if (noteCat.parentId) setExpandedTopics((prev) => new Set([...prev, noteCat.id]));
  }, [note, allCategories]);

  // ─── Handlers ──────────────────────────────────────────────
  const handleNavigate = React.useCallback((n: Note) => {
    openNote(n);
    if (typeof window !== "undefined" && window.innerWidth < 768) setMobileSidebarOpen(false);
  }, [openNote]);

  const toggleCat = (id: string) => setExpandedCats((prev) => { const n = new Set(prev); if (n.has(id)) n.delete(id); else n.add(id); return n; });
  const toggleTopic = (id: string) => setExpandedTopics((prev) => { const n = new Set(prev); if (n.has(id)) n.delete(id); else n.add(id); return n; });

  // ─── Fit zoom ──────────────────────────────────────────────
  const computeFitScale = React.useCallback(() => {
    const el = containerRef.current;
    if (!el) return;
    const w = el.clientWidth - 48;
    setZoom(Math.max(0.25, Math.min(w / 1136, 1)));
  }, []);

  React.useEffect(() => {
    if (zoomMode === "fit") { const t = setTimeout(computeFitScale, 80); return () => clearTimeout(t); }
  }, [note, zoomMode, computeFitScale, sidebarCollapsed]);

  React.useEffect(() => {
    if (zoomMode !== "fit") return;
    const h = () => computeFitScale();
    window.addEventListener("resize", h);
    return () => window.removeEventListener("resize", h);
  }, [zoomMode, computeFitScale]);

  // ─── Fullscreen ────────────────────────────────────────────
  const toggleFullscreen = React.useCallback(() => {
    if (document.fullscreenElement) document.exitFullscreen?.();
    else containerRef.current?.requestFullscreen?.();
  }, []);
  React.useEffect(() => { const h = () => setIsFullscreen(!!document.fullscreenElement); document.addEventListener("fullscreenchange", h); return () => document.removeEventListener("fullscreenchange", h); }, []);

  // ─── Close popovers ────────────────────────────────────────
  React.useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (downloadOpen && downloadRef.current && !downloadRef.current.contains(e.target as Node)) setDownloadOpen(false);
      if (zoomPresetsOpen && zoomRef.current && !zoomRef.current.contains(e.target as Node)) setZoomPresetsOpen(false);
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, [downloadOpen, zoomPresetsOpen]);

  // ─── Keyboard ──────────────────────────────────────────────
  React.useEffect(() => {
    const handleKey = (e: KeyboardEvent) => {
      const t = e.target as HTMLElement;
      const typing = t.tagName === "INPUT" || t.tagName === "TEXTAREA";
      if (e.key === "Escape") {
        if (mobileSidebarOpen) { setMobileSidebarOpen(false); return; }
        if (downloadOpen) { setDownloadOpen(false); return; }
        if (zoomPresetsOpen) { setZoomPresetsOpen(false); return; }
        setToolbarExpanded(false);
      }
      if ((e.ctrlKey || e.metaKey) && (e.key === "+" || e.key === "=")) { e.preventDefault(); setZoomMode("manual"); setZoom(z => Math.min(4, z + 0.1)); return; }
      if ((e.ctrlKey || e.metaKey) && e.key === "-") { e.preventDefault(); setZoomMode("manual"); setZoom(z => Math.max(0.25, z - 0.1)); return; }
      if ((e.ctrlKey || e.metaKey) && e.key === "0") { e.preventDefault(); setZoomMode("fit"); computeFitScale(); return; }
      if (typing) return;
      if (e.key === "ArrowLeft" && !mobileSidebarOpen && prevPage) { e.preventDefault(); handleNavigate(prevPage); }
      if (e.key === "ArrowRight" && !mobileSidebarOpen && nextPage) { e.preventDefault(); handleNavigate(nextPage); }
    };
    window.addEventListener("keydown", handleKey);
    return () => window.removeEventListener("keydown", handleKey);
  }, [mobileSidebarOpen, downloadOpen, zoomPresetsOpen, prevPage, nextPage, handleNavigate, computeFitScale]);

  // ─── Iframe ────────────────────────────────────────────────
  const handleIframeLoad = React.useCallback((e: React.SyntheticEvent<HTMLIFrameElement>) => {
    try {
      const iframe = e.currentTarget;
      const doc = iframe.contentDocument;
      if (!doc) return;
      const ex = doc.getElementById("reader-style");
      if (ex) ex.remove();
      const style = doc.createElement("style");
      style.id = "reader-style";
      style.textContent = `body { justify-content: flex-start !important; padding-left: 42px !important; padding-right: 14px !important; } @media (max-width: 1120px) { html { overflow-x: auto; } }`;
      doc.head.appendChild(style);
      const resize = () => { const h = Math.max(doc.body.scrollHeight, doc.body.offsetHeight, doc.documentElement.scrollHeight, doc.documentElement.offsetHeight); iframe.style.height = `${h + 20}px`; };
      resize(); setTimeout(resize, 500); setTimeout(resize, 1500);
    } catch {}
  }, []);

  const handleShare = () => { navigator.clipboard?.writeText(window.location.href).then(() => { setCopied(true); setTimeout(() => setCopied(false), 2000); }); };

  // ─── Render ────────────────────────────────────────────────
  if (loading) return (<div className="flex h-screen items-center justify-center bg-slate-900"><Skeleton className="h-[60vh] w-full max-w-4xl rounded-xl" /></div>);
  if (!note) return (<div className="flex h-screen flex-col items-center justify-center gap-4 bg-slate-900 text-slate-200"><Home className="size-8 text-slate-400" /><h2 className="text-xl font-bold text-white">Note not found</h2><Button onClick={goHome} className="gap-2"><Home className="size-4" /> Browse all notes</Button></div>);

  const zoomLabel = zoomMode === "fit" ? "Fit" : `${Math.round(zoom * 100)}%`;

  // Filter tree
  const filteredTree = sidebarSearch.trim()
    ? tree.map((node) => {
        const q = sidebarSearch.toLowerCase();
        return {
          ...node,
          topics: node.topics.map(t => ({ ...t, notes: t.notes.filter(n => n.title.toLowerCase().includes(q)) })).filter(t => t.notes.length > 0),
          notes: node.notes.filter(n => n.title.toLowerCase().includes(q)),
        };
      }).filter(n => n.topics.length > 0 || n.notes.length > 0)
    : tree;

  return (
    <div ref={containerRef} className="flex h-screen w-full overflow-hidden bg-slate-900 text-slate-100">
      {/* ═══ Mobile backdrop ═══ */}
      <AnimatePresence>
        {mobileSidebarOpen && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            className="fixed inset-0 z-40 bg-black/50 md:hidden" onClick={() => setMobileSidebarOpen(false)} />
        )}
      </AnimatePresence>

      {/* ═══ Left Sidebar (desktop inline) ═══ */}
      <motion.aside
        animate={{ width: sidebarCollapsed ? 0 : 280 }}
        transition={{ type: "spring", damping: 30, stiffness: 300 }}
        className="relative z-30 hidden shrink-0 overflow-hidden border-r border-slate-800 bg-slate-950 md:block"
      >
        <SidebarContent
          tree={filteredTree} note={note} expandedCats={expandedCats} expandedTopics={expandedTopics}
          toggleCat={toggleCat} toggleTopic={toggleTopic} onNavigate={handleNavigate}
          sidebarMode={sidebarMode} setSidebarMode={setSidebarMode}
          sidebarSearch={sidebarSearch} setSidebarSearch={setSidebarSearch} goHome={goHome}
        />
      </motion.aside>

      {/* ═══ Left Sidebar (mobile drawer) ═══ */}
      <AnimatePresence>
        {mobileSidebarOpen && (
          <motion.aside
            initial={{ x: "-100%" }} animate={{ x: 0 }} exit={{ x: "-100%" }}
            transition={{ type: "spring", damping: 30, stiffness: 300 }}
            className="fixed inset-y-0 left-0 z-50 w-[85vw] max-w-[320px] overflow-hidden border-r border-slate-800 bg-slate-950 md:hidden"
          >
            <SidebarContent
              tree={filteredTree} note={note} expandedCats={expandedCats} expandedTopics={expandedTopics}
              toggleCat={toggleCat} toggleTopic={toggleTopic} onNavigate={handleNavigate}
              sidebarMode={sidebarMode} setSidebarMode={setSidebarMode}
              sidebarSearch={sidebarSearch} setSidebarSearch={setSidebarSearch} goHome={goHome}
            />
          </motion.aside>
        )}
      </AnimatePresence>

      {/* ═══ Main Area ═══ */}
      <div className="flex min-w-0 flex-1 flex-col">
        {/* ── Top Bar ── */}
        <div className="flex h-12 shrink-0 items-center gap-2 border-b border-slate-800 bg-slate-950/80 px-3 backdrop-blur-md">
          <Button variant="ghost" size="icon" className="size-8 shrink-0 text-slate-400 hover:text-slate-200"
            onClick={() => { if (window.innerWidth >= 768) setSidebarCollapsed(!sidebarCollapsed); else setMobileSidebarOpen(true); }}
            title="Toggle sidebar">
            {sidebarCollapsed ? <PanelLeftOpen className="size-4" /> : <PanelLeftClose className="size-4" />}
          </Button>
          <Button variant="ghost" size="icon" className="size-8 shrink-0 text-slate-400 hover:text-slate-200" onClick={goHome} title="Home">
            <Home className="size-4" />
          </Button>
          <div className="hidden min-w-0 flex-1 items-center gap-1.5 text-xs text-slate-400 sm:flex">
            {note.category && <span className="truncate">{note.category.name}</span>}
            <ChevronRight className="size-3 shrink-0 text-slate-600" />
            <span className="truncate text-slate-200">{note.title}</span>
            {totalPages > 1 && <span className="ml-1 text-slate-500">· {currentIndex + 1}/{totalPages}</span>}
          </div>
          <div className="flex-1 sm:hidden" />
          <Button variant="ghost" size="icon" className="size-8 shrink-0 text-slate-400 hover:text-slate-200"
            onClick={() => setRightPanelOpen(!rightPanelOpen)} title="Toggle info">
            <MoreVertical className="size-4" />
          </Button>
          <Button variant="ghost" size="icon" className="size-8 shrink-0 text-slate-400 hover:text-slate-200"
            onClick={toggleFullscreen} title="Fullscreen">
            {isFullscreen ? <Minimize className="size-4" /> : <Maximize className="size-4" />}
          </Button>
        </div>

        {/* ── Floating Toolbar ── */}
        <AnimatePresence>
          {toolbarExpanded && (
            <motion.div
              initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.2 }}
              className="pointer-events-none absolute left-1/2 top-14 z-20 -translate-x-1/2"
            >
              <div className="pointer-events-auto flex items-center gap-1 rounded-full border border-slate-700 bg-slate-800/95 px-2 py-1.5 shadow-lg backdrop-blur-md">
                <div className="relative" ref={downloadRef}>
                  <Button variant="ghost" size="icon" className={cn("size-7 rounded-full text-slate-400 hover:text-slate-200", downloadOpen && "bg-slate-700")}
                    onClick={() => setDownloadOpen(!downloadOpen)} title="Export">
                    <Download className="size-3.5" />
                  </Button>
                  <AnimatePresence>
                    {downloadOpen && (
                      <motion.div initial={{ opacity: 0, y: -5 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -5 }} transition={{ duration: 0.15 }}
                        className="absolute left-0 top-full mt-2 w-48 rounded-lg border border-slate-700 bg-slate-800 p-1 shadow-xl">
                        <div className="px-2 py-1 text-[10px] font-bold uppercase tracking-wider text-slate-500">Current Page</div>
                        {["PNG", "JPEG", "PDF"].map(f => <button key={f} onClick={() => setDownloadOpen(false)} className="flex w-full items-center gap-2 rounded px-2 py-1.5 text-xs text-slate-300 hover:bg-slate-700"><FileImage className="size-3.5 text-slate-500" /> {f}</button>)}
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>
                <Sep />
                <Button variant="ghost" size="icon" disabled={!prevPage} className="size-7 rounded-full text-slate-400 hover:text-slate-200" onClick={() => prevPage && handleNavigate(prevPage)} title="Prev (←)"><ChevronLeft className="size-3.5" /></Button>
                <span className="min-w-[3rem] text-center text-xs font-mono text-slate-400">{currentIndex + 1}/{totalPages}</span>
                <Button variant="ghost" size="icon" disabled={!nextPage} className="size-7 rounded-full text-slate-400 hover:text-slate-200" onClick={() => nextPage && handleNavigate(nextPage)} title="Next (→)"><ChevronRight className="size-3.5" /></Button>
                <Sep />
                <Button variant="ghost" size="icon" className="size-7 rounded-full text-slate-400 hover:text-slate-200" onClick={() => { setZoomMode("manual"); setZoom(Math.max(0.25, zoom - 0.1)); }} title="Zoom out"><ZoomOut className="size-3.5" /></Button>
                <div className="relative" ref={zoomRef}>
                  <button className="h-6 min-w-[44px] rounded border border-transparent bg-slate-700 px-1 text-center text-xs font-mono text-slate-300 hover:border-slate-600" onClick={() => setZoomPresetsOpen(!zoomPresetsOpen)}>{zoomLabel}</button>
                  <AnimatePresence>
                    {zoomPresetsOpen && (
                      <motion.div initial={{ opacity: 0, y: -5 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -5 }} transition={{ duration: 0.15 }}
                        className="absolute left-1/2 top-full mt-2 w-32 -translate-x-1/2 rounded-lg border border-slate-700 bg-slate-800 p-1 shadow-xl">
                        <button onClick={() => { setZoomMode("fit"); computeFitScale(); setZoomPresetsOpen(false); }} className="flex w-full items-center gap-2 rounded px-2 py-1 text-xs text-slate-300 hover:bg-slate-700"><Maximize className="size-3" /> Fit</button>
                        <div className="my-1 h-px bg-slate-700" />
                        {["50%", "75%", "100%", "125%", "150%"].map(l => <button key={l} onClick={() => { setZoomMode("manual"); setZoom(parseInt(l)/100); setZoomPresetsOpen(false); }} className="flex w-full rounded px-2 py-1 text-xs text-slate-300 hover:bg-slate-700">{l}</button>)}
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>
                <Button variant="ghost" size="icon" className="size-7 rounded-full text-slate-400 hover:text-slate-200" onClick={() => { setZoomMode("manual"); setZoom(Math.min(4, zoom + 0.1)); }} title="Zoom in"><ZoomIn className="size-3.5" /></Button>
                <Sep />
                <Button variant="ghost" size="icon" className="size-7 rounded-full text-slate-400 hover:text-slate-200" onClick={() => setToolbarExpanded(false)} title="Collapse"><ChevronUp className="size-3.5" /></Button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {!toolbarExpanded && (
          <button onClick={() => setToolbarExpanded(true)} className="absolute left-1/2 top-14 z-20 flex -translate-x-1/2 items-center gap-1 rounded-full border border-slate-700 bg-slate-800/95 px-3 py-1 text-xs text-slate-400 shadow-md backdrop-blur-sm hover:text-slate-200" title="Expand toolbar">
            <ChevronDown className="size-3" /><span className="font-mono">{currentIndex + 1}/{totalPages}</span>
          </button>
        )}

        {/* ── Document ── */}
        <div className="flex-1 overflow-auto bg-slate-900 p-4 pt-12">
          <AnimatePresence mode="wait">
            <motion.div key={note.id} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }} transition={{ duration: 0.25 }}
              className="mx-auto overflow-x-auto rounded-xl bg-white shadow-2xl" style={{ maxWidth: `${1080 + 56}px`, width: "100%" }}>
              <iframe title={note.title} className="block" style={{ minHeight: "60vh", transform: `scale(${zoom})`, transformOrigin: "top left", width: `${100 / zoom}%`, border: 0 }}
                src={note.contentPath} sandbox="allow-same-origin allow-popups" onLoad={handleIframeLoad} />
            </motion.div>
          </AnimatePresence>

          {totalPages > 1 && (
            <div className="mx-auto mt-4 flex max-w-3xl items-center justify-between border-t border-slate-800 pt-3">
              {prevPage ? <Button variant="ghost" size="sm" onClick={() => handleNavigate(prevPage)} className="gap-1.5 text-slate-400 hover:text-slate-200"><ChevronLeft className="size-4" /><span className="hidden max-w-[200px] truncate sm:inline">{prevPage.title}</span><span className="sm:hidden">Prev</span></Button> : <div />}
              {nextPage ? <Button variant="ghost" size="sm" onClick={() => handleNavigate(nextPage)} className="gap-1.5 text-slate-400 hover:text-slate-200"><span className="hidden max-w-[200px] truncate sm:inline">{nextPage.title}</span><span className="sm:hidden">Next</span><ChevronRight className="size-4" /></Button> : <div />}
            </div>
          )}
        </div>
      </div>

      {/* ═══ Right Panel ═══ */}
      <AnimatePresence>
        {rightPanelOpen && (
          <motion.aside initial={{ width: 0, opacity: 0 }} animate={{ width: 240, opacity: 1 }} exit={{ width: 0, opacity: 0 }} transition={{ type: "spring", damping: 30, stiffness: 300 }}
            className="hidden shrink-0 overflow-hidden border-l border-slate-800 bg-slate-950 lg:block">
            <RightPanel note={note} pages={pages} currentIndex={currentIndex} relatedNotes={relatedNotes} onNavigate={handleNavigate} copied={copied} onShare={handleShare} />
          </motion.aside>
        )}
      </AnimatePresence>
    </div>
  );
}

// ─── Sidebar Content ───────────────────────────────────────────
function SidebarContent({ tree, note, expandedCats, expandedTopics, toggleCat, toggleTopic, onNavigate, sidebarMode, setSidebarMode, sidebarSearch, setSidebarSearch, goHome }: {
  tree: TreeNode[]; note: Note; expandedCats: Set<string>; expandedTopics: Set<string>;
  toggleCat: (id: string) => void; toggleTopic: (id: string) => void; onNavigate: (n: Note) => void;
  sidebarMode: SidebarMode; setSidebarMode: (m: SidebarMode) => void;
  sidebarSearch: string; setSidebarSearch: (s: string) => void; goHome: () => void;
}) {
  return (
    <div className="flex h-full w-[280px] flex-col">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 px-3 py-2.5">
        <button onClick={goHome} className="flex items-center gap-2 text-sm font-semibold text-slate-200 hover:text-white">
          <Home className="size-4 text-slate-400" /> Notes
        </button>
        <button className="text-slate-500 hover:text-slate-300 md:hidden" onClick={() => {}}>
          <X className="size-4" />
        </button>
      </div>

      {/* Search */}
      <div className="border-b border-slate-800 px-3 py-2">
        <div className="relative">
          <Search className="pointer-events-none absolute left-2.5 top-1/2 size-3.5 -translate-y-1/2 text-slate-600" />
          <input value={sidebarSearch} onChange={(e) => setSidebarSearch(e.target.value)} placeholder="Filter topics…"
            className="w-full rounded-md border border-slate-800 bg-slate-900 py-1.5 pl-8 pr-2 text-xs text-slate-300 outline-none placeholder:text-slate-600 focus:border-slate-700" />
        </div>
      </div>

      {/* View toggle */}
      <div className="flex items-center gap-1 border-b border-slate-800 px-3 py-1.5">
        <div className="flex items-center gap-0.5 rounded-md bg-slate-800 p-0.5">
          <button onClick={() => setSidebarMode("list")} className={cn("flex items-center gap-1 rounded px-2 py-0.5 text-xs transition-all", sidebarMode === "list" ? "bg-slate-700 font-semibold text-slate-100" : "text-slate-500")}>
            <ChevronRight className="size-3" /> List
          </button>
          <button onClick={() => setSidebarMode("tile")} className={cn("flex items-center gap-1 rounded px-2 py-0.5 text-xs transition-all", sidebarMode === "tile" ? "bg-slate-700 font-semibold text-slate-100" : "text-slate-500")}>
            <FileText className="size-3" /> Tiles
          </button>
        </div>
      </div>

      {/* Tree */}
      <ScrollArea className="flex-1 px-1 py-1">
        {tree.length === 0 ? (
          <div className="px-3 py-8 text-center text-xs text-slate-600">No notes found</div>
        ) : (
          <div className="space-y-0.5 pb-4">
            {tree.map((node) => {
              const isExpanded = expandedCats.has(node.category.id) || !!sidebarSearch.trim();
              const allNotes = [...node.notes, ...node.topics.flatMap(t => t.notes)];
              const isActiveCat = allNotes.some(n => n.id === note.id);
              return (
                <div key={node.category.id}>
                  {/* Category */}
                  <button onClick={() => toggleCat(node.category.id)}
                    className={cn("group flex w-full items-center gap-1.5 rounded-md px-2 py-1.5 text-left text-xs font-medium transition-colors",
                      isActiveCat ? "bg-slate-800 text-slate-200" : "text-slate-400 hover:bg-slate-900 hover:text-slate-300")}>
                    <ChevronDown className={cn("size-3 shrink-0 transition-transform text-slate-600", !isExpanded && "-rotate-90")} />
                    {isExpanded ? <FolderOpen className="size-3.5 shrink-0 text-slate-500" /> : <Folder className="size-3.5 shrink-0 text-slate-500" />}
                    <span className="truncate">{node.category.name}</span>
                    <span className="ml-auto text-[10px] text-slate-600">{allNotes.length}</span>
                  </button>

                  {/* Expanded content */}
                  <AnimatePresence>
                    {isExpanded && (
                      <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: "auto", opacity: 1 }} exit={{ height: 0, opacity: 0 }} transition={{ duration: 0.2 }} className="overflow-hidden">
                        <div className="ml-3 border-l border-slate-800 pl-2">
                          {/* Direct notes */}
                          {node.notes.map((n, idx) => (
                            <PageItem key={n.id} note={n} index={idx} isActive={n.id === note.id} onNavigate={onNavigate} mode={sidebarMode} />
                          ))}
                          {/* Topics */}
                          {node.topics.map((topic) => {
                            const tExp = expandedTopics.has(topic.category.id) || !!sidebarSearch.trim();
                            const isActiveT = topic.notes.some(n => n.id === note.id);
                            return (
                              <div key={topic.category.id}>
                                <button onClick={() => toggleTopic(topic.category.id)}
                                  className={cn("flex w-full items-center gap-1.5 rounded-md px-2 py-1 text-left text-xs transition-colors",
                                    isActiveT ? "text-slate-200" : "text-slate-500 hover:text-slate-300")}>
                                  <ChevronDown className={cn("size-3 shrink-0 transition-transform text-slate-600", !tExp && "-rotate-90")} />
                                  <span className="truncate">{topic.category.name}</span>
                                  <span className="ml-auto text-[10px] text-slate-600">{topic.notes.length}</span>
                                </button>
                                <AnimatePresence>
                                  {tExp && (
                                    <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: "auto", opacity: 1 }} exit={{ height: 0, opacity: 0 }} transition={{ duration: 0.2 }} className="overflow-hidden">
                                      <div className="ml-3 border-l border-slate-800 pl-2">
                                        {topic.notes.map((n, idx) => (
                                          <PageItem key={n.id} note={n} index={idx} isActive={n.id === note.id} onNavigate={onNavigate} mode={sidebarMode} />
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
  );
}

// ─── Page Item ────────────────────────────────────────────────
function PageItem({ note: n, index, isActive, onNavigate, mode }: { note: Note; index: number; isActive: boolean; onNavigate: (n: Note) => void; mode: SidebarMode }) {
  if (mode === "tile") {
    return (
      <button onClick={() => onNavigate(n)} className={cn("mb-1 block w-full overflow-hidden rounded-lg border text-left transition-colors", isActive ? "border-rose-500/50 bg-rose-500/10" : "border-slate-800 hover:border-slate-700")}>
        <div className="flex items-center gap-1.5 px-2 py-1">
          <span className={cn("text-[10px] font-mono", isActive ? "text-rose-400" : "text-slate-600")}>{String(index + 1).padStart(2, "0")}</span>
          <span className={cn("truncate text-[11px]", isActive ? "font-medium text-rose-300" : "text-slate-400")}>{n.title}</span>
        </div>
      </button>
    );
  }
  return (
    <button onClick={() => onNavigate(n)} className={cn("flex w-full items-center gap-2 rounded-md px-2 py-1.5 text-left text-xs transition-colors", isActive ? "bg-rose-500/10 text-rose-300" : "text-slate-400 hover:bg-slate-900 hover:text-slate-300")}>
      <span className={cn("flex size-4 shrink-0 items-center justify-center rounded text-[9px] font-mono", isActive ? "bg-rose-500 text-white" : "bg-slate-800 text-slate-600")}>{index + 1}</span>
      <span className={cn("truncate", isActive && "font-medium")}>{n.title}</span>
      {isActive && <span className="ml-auto size-1.5 shrink-0 rounded-full bg-rose-500" />}
    </button>
  );
}

// ─── Right Panel ───────────────────────────────────────────────
function RightPanel({ note, pages, currentIndex, relatedNotes, onNavigate, copied, onShare }: {
  note: Note; pages: Note[]; currentIndex: number; relatedNotes: Note[]; onNavigate: (n: Note) => void; copied: boolean; onShare: () => void;
}) {
  return (
    <div className="flex h-full w-[240px] flex-col overflow-y-auto">
      <div className="border-b border-slate-800 p-3">
        <h3 className="mb-2 text-[10px] font-bold uppercase tracking-wider text-slate-600">Info</h3>
        <div className="space-y-1 text-xs text-slate-500">
          <div className="flex items-center gap-1.5"><Clock className="size-3" /> {fromNow(note.updatedAt)}</div>
          <div>{formatDateTime(note.updatedAt)}</div>
        </div>
        {note.tags && note.tags.length > 0 && (
          <div className="mt-2 flex flex-wrap gap-1">{note.tags.map(t => <Badge key={t.id} variant="outline" className="border-slate-700 bg-slate-800 text-[10px] font-normal text-slate-400">{t.name}</Badge>)}</div>
        )}
      </div>
      <div className="border-b border-slate-800 p-3">
        <h3 className="mb-2 text-[10px] font-bold uppercase tracking-wider text-slate-600">Actions</h3>
        <div className="space-y-0.5">
          <button onClick={onShare} className="flex w-full items-center gap-2 rounded px-2 py-1.5 text-xs text-slate-400 hover:bg-slate-900 hover:text-slate-300"><Share2 className="size-3.5" /> {copied ? "Link Copied!" : "Copy Link"}</button>
          <a href={note.contentPath} target="_blank" rel="noopener noreferrer" className="flex w-full items-center gap-2 rounded px-2 py-1.5 text-xs text-slate-400 hover:bg-slate-900 hover:text-slate-300"><ExternalLink className="size-3.5" /> Open Raw</a>
        </div>
      </div>
      {relatedNotes.length > 0 && (
        <div className="border-b border-slate-800 p-3">
          <h3 className="mb-2 text-[10px] font-bold uppercase tracking-wider text-slate-600">Related</h3>
          <div className="space-y-0.5">{relatedNotes.map(rel => <button key={rel.id} onClick={() => onNavigate(rel)} className="flex w-full items-center gap-2 rounded px-2 py-1.5 text-left text-xs text-slate-400 hover:bg-slate-900 hover:text-slate-300"><FileText className="size-3 shrink-0 text-slate-600" /><span className="truncate">{rel.title}</span></button>)}</div>
        </div>
      )}
      {pages.length > 1 && (
        <div className="p-3">
          <h3 className="mb-2 text-[10px] font-bold uppercase tracking-wider text-slate-600">All Pages</h3>
          <div className="space-y-0.5">{pages.map((p, idx) => <button key={p.id} onClick={() => onNavigate(p)} className={cn("flex w-full items-center gap-2 rounded px-2 py-1 text-left text-xs transition-colors", p.id === note.id ? "font-semibold text-rose-400" : "text-slate-500 hover:text-slate-300")}><span className="w-4 shrink-0 font-mono text-[10px]">{String(idx + 1).padStart(2, "0")}.</span><span className="truncate">{p.title}</span></button>)}</div>
        </div>
      )}
    </div>
  );
}

function Sep() { return <div className="mx-0.5 h-4 w-px bg-slate-700" />; }
