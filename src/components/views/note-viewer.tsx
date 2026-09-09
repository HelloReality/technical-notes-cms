"use client";

import * as React from "react";
import { AnimatePresence, motion } from "framer-motion";
import {
  BookImage,
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
  History,
  Home,
  Maximize,
  Menu,
  Minimize,
  MoreVertical,
  Search,
  Share2,
  Trash2,
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
import { useIsMobile } from "@/hooks/use-mobile";

type SidebarMode = "tile" | "list";

// ─── Page layout (background pattern) ──────────────────────────
// Viewer option that swaps the note's page background. The note's HTML/CSS
// is never modified — we inject a small style block that overrides the
// `.page::before` background used for the graph-paper grid.
type PageLayout = "grid" | "plain" | "lined" | "dots";

const PAGE_LAYOUTS: {
  key: PageLayout;
  label: string;
  // CSS for the `.page::before` pseudo-element that draws the pattern.
  // `grid` is empty (keeps the note's own graph-paper background).
  css: string;
}[] = [
  {
    key: "grid",
    label: "Grid",
    css: "", // use the note's original graph paper
  },
  {
    key: "plain",
    label: "Plain",
    css: `.page::before, .notebook::before, .paper::before { background-image: none !important; }`,
  },
  {
    key: "lined",
    label: "Lined",
    css: `.page::before, .notebook::before, .paper::before {
      background-image: linear-gradient(to bottom, #b8c5d6 1px, transparent 1px) !important;
      background-size: 28px 28px !important;
      opacity: .6 !important;
    }`,
  },
  {
    key: "dots",
    label: "Dots",
    css: `.page::before, .notebook::before, .paper::before {
      background-image: radial-gradient(circle, #b8c5d6 1px, transparent 1px) !important;
      background-size: 24px 24px !important;
      opacity: .8 !important;
    }`,
  },
];

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
  // Recently-viewed tracking
  const recentViews = useAppStore((s) => s.recentViews);
  const recentLoading = useAppStore((s) => s.recentLoading);
  const loadRecentViews = useAppStore((s) => s.loadRecentViews);
  const clearRecent = useAppStore((s) => s.clearRecent);
  const recordView = useAppStore((s) => s.recordView);

  // State
  const [toolbarExpanded, setToolbarExpanded] = React.useState(true);
  const [drawerOpen, setDrawerOpen] = React.useState(false);
  const [actionsOpen, setActionsOpen] = React.useState(false);
  const [downloadOpen, setDownloadOpen] = React.useState(false);
  const [zoomPresetsOpen, setZoomPresetsOpen] = React.useState(false);
  const [pageViewMode, setPageViewMode] = React.useState<SidebarMode>("tiles");
  // Page titles/overviews extracted from the note's HTML for the pages drawer.
  const [pageTitles, setPageTitles] = React.useState<string[]>([]);
  const [isFullscreen, setIsFullscreen] = React.useState(false);
  const [copied, setCopied] = React.useState(false);
  const [zoom, setZoom] = React.useState(1);
  const [zoomMode, setZoomMode] = React.useState<"fit" | "manual">("fit");
  const [pageInputValue, setPageInputValue] = React.useState("");
  const [pageInputFocused, setPageInputFocused] = React.useState(false);
  const [isNavigating, setIsNavigating] = React.useState(false);

  // Pages WITHIN the current note. A note's HTML may contain multiple
  // .page-wrapper elements (e.g. a 20-image carousel). We show ONE page
  // at a time and navigate with the prev/next arrows in the top nav.
  const [notePageCount, setNotePageCount] = React.useState(1);
  const [notePageIndex, setNotePageIndex] = React.useState(0);

  // Whether the note's FIRST .page-wrapper is a cover page (contains a
  // `.cover` element). Cover pages are excluded from the pagination so
  // they don't affect the page numbering — page 1 in the viewer is the
  // first CONTENT page. The cover is still reachable via a dedicated
  // "Cover" toggle button in the toolbar.
  const [hasCoverPage, setHasCoverPage] = React.useState(false);
  // When true, the viewer shows the cover wrapper instead of the current
  // content page. The page counter is replaced with a "Cover" label.
  const [showCover, setShowCover] = React.useState(false);

  // Page layout (background pattern) — viewer option that swaps the note's
  // page background via injected CSS. "grid" = the note's original graph paper.
  const [pageLayout, setPageLayout] = React.useState<PageLayout>("grid");

  // Tree drawer state (Category → Topic → subtopic navigation)
  const [treeOpen, setTreeOpen] = React.useState(false);
  const [expandedCats, setExpandedCats] = React.useState<Set<string>>(new Set());
  const [expandedTopics, setExpandedTopics] = React.useState<Set<string>>(new Set());

  const containerRef = React.useRef<HTMLDivElement>(null);
  const mainRef = React.useRef<HTMLDivElement>(null);
  const iframeRef = React.useRef<HTMLIFrameElement>(null);
  const downloadRef = React.useRef<HTMLDivElement>(null);
  const zoomRef = React.useRef<HTMLDivElement>(null);
  const mobileZoomRef = React.useRef<HTMLDivElement>(null);

  // Responsive: below 768px the tree becomes an overlay drawer (no inline rail)
  // and the toolbar zoom group is hidden (moved into the actions panel).
  const isMobile = useIsMobile();

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

  // ─── Pages within the current note ────────────────────────────
  // The note's HTML may contain multiple .page-wrapper elements. We
  // show ONE at a time and navigate with prev/next. For notes with a
  // single page (or no .page-wrapper), there's nothing to navigate.
  //
  // COVER PAGE HANDLING: if the first .page-wrapper is a cover page
  // (it contains a `.cover` element), it is EXCLUDED from pagination.
  // The cover wrapper is always hidden during normal navigation and
  // only shown when the user toggles the "Cover" button. This keeps
  // the page counter accurate (page 1 = first real content page).
  const hasPrevPage = notePageIndex > 0;
  const hasNextPage = notePageIndex < notePageCount - 1;
  const totalPages = notePageCount;
  const currentIndex = notePageIndex;

  // Show a specific page within the note by hiding all .page-wrapper
  // elements except the one at `index`, then resize the iframe to fit
  // just that page (so there's no empty scroll space below).
  const showNotePage = React.useCallback(
    (viewerIndex: number) => {
      const iframe = iframeRef.current;
      if (!iframe) return;
      try {
        const doc = iframe.contentDocument;
        if (!doc) return;
        const wrappers = doc.querySelectorAll(".page-wrapper");
        if (wrappers.length === 0) return;
        const coverOffset = hasCoverPage ? 1 : 0;
        const wrapperIdx = viewerIndex + coverOffset;
        const clamped = Math.max(0, Math.min(wrapperIdx, wrappers.length - 1));
        wrappers.forEach((el, i) => {
          (el as HTMLElement).style.display = i === clamped ? "" : "none";
        });
        // Scroll the iframe's own scroll container to the top of the page.
        doc.defaultView?.scrollTo(0, 0);
      } catch {
        /* cross-origin — ignore */
      }
    },
    [hasCoverPage],
  );

  // Show ONLY the cover wrapper (the first .page-wrapper). Used by the
  // "Cover" toggle button in the toolbar.
  const showCoverPage = React.useCallback(() => {
    const iframe = iframeRef.current;
    if (!iframe) return;
    try {
      const doc = iframe.contentDocument;
      if (!doc) return;
      const wrappers = doc.querySelectorAll(".page-wrapper");
      if (wrappers.length === 0) return;
      wrappers.forEach((el, i) => {
        (el as HTMLElement).style.display = i === 0 ? "" : "none";
      });
      doc.defaultView?.scrollTo(0, 0);
    } catch {
      /* cross-origin — ignore */
    }
  }, []);

  // Toggle the cover view. When switching to cover we remember nothing
  // (notePageIndex stays put so returning to content resumes the same
  // page). When switching back to content we re-show the current page.
  const toggleCover = React.useCallback(() => {
    setShowCover((prev) => {
      const next = !prev;
      if (next) {
        showCoverPage();
      } else {
        showNotePage(notePageIndex);
      }
      return next;
    });
  }, [showCoverPage, showNotePage, notePageIndex]);

  // Detect how many .page-wrapper elements the note has, then show
  // only the first CONTENT page (skipping the cover if one exists).
  // Called from the iframe onLoad + applyNoteScale.
  const detectNotePages = React.useCallback(() => {
    const iframe = iframeRef.current;
    if (!iframe) return;
    try {
      const doc = iframe.contentDocument;
      if (!doc) return;
      const wrappers = doc.querySelectorAll(".page-wrapper");
      // Detect a cover page: the first wrapper contains a `.cover` element.
      const firstWrapper = wrappers[0] as HTMLElement | null;
      const coverDetected =
        !!firstWrapper && !!firstWrapper.querySelector(".cover");
      setHasCoverPage(coverDetected);
      // Content page count = total wrappers minus the cover (if present).
      const contentCount = Math.max(
        1,
        wrappers.length - (coverDetected ? 1 : 0),
      );
      setNotePageCount(contentCount);
      setNotePageIndex(0);
      setShowCover(false);
      // Hide the cover wrapper (if any) and show only the first content
      // page. When no cover exists, wrapper 0 is the first content page.
      const firstContentIdx = coverDetected ? 1 : 0;
      wrappers.forEach((el, i) => {
        (el as HTMLElement).style.display = i === firstContentIdx ? "" : "none";
      });
      // Extract the title (h1) and subtitle/overview for each CONTENT
      // page (skipping the cover) so the pages drawer can show meaningful
      // labels instead of just "Page 1 of 20".
      const titles: string[] = [];
      for (let i = firstContentIdx; i < wrappers.length; i++) {
        const el = wrappers[i] as HTMLElement;
        const h1 = el.querySelector("h1, h2, .title");
        const subtitle = el.querySelector(".subtitle, .page-subtitle, .sub-text");
        let label = "";
        if (h1) {
          label = (h1.textContent || "").replace(/\s+/g, " ").trim();
        }
        if (!label && subtitle) {
          label = (subtitle.textContent || "").replace(/\s+/g, " ").trim();
        }
        if (!label) label = `Page ${i - firstContentIdx + 1}`;
        titles.push(label);
      }
      // If the note has no .page-wrapper (single page), use the note title.
      if (titles.length === 0 && note) {
        titles.push(note.title);
      }
      setPageTitles(titles);
    } catch {
      /* cross-origin — ignore */
    }
  }, [note]);

  // Reset to page 0 + detect pages when the active note changes.
  React.useEffect(() => {
    setNotePageIndex(0);
    setNotePageCount(1);
    setHasCoverPage(false);
    setShowCover(false);
    // detectNotePages runs after the iframe loads (onLoad calls it).
  }, [note?.id]);

  // Navigate to the next/prev page within the note.
  // While the cover is being shown, navigation exits the cover view
  // first (so the counter stays accurate) before moving pages.
  const goToPrevPage = React.useCallback(() => {
    if (showCover) {
      setShowCover(false);
      showNotePage(notePageIndex);
      return;
    }
    setNotePageIndex((i) => {
      const next = Math.max(0, i - 1);
      if (next !== i) showNotePage(next);
      return next;
    });
  }, [showCover, notePageIndex, showNotePage]);
  const goToNextPage = React.useCallback(() => {
    if (showCover) {
      setShowCover(false);
      showNotePage(notePageIndex);
      return;
    }
    setNotePageIndex((i) => {
      const next = Math.min(notePageCount - 1, i + 1);
      if (next !== i) showNotePage(next);
      return next;
    });
  }, [showCover, notePageCount, notePageIndex, showNotePage]);
  const goToPage = React.useCallback(
    (index: number) => {
      // Selecting a page from the pages drawer exits cover view.
      setShowCover(false);
      const clamped = Math.max(0, Math.min(notePageCount - 1, index));
      setNotePageIndex(clamped);
      showNotePage(clamped);
    },
    [notePageCount, showNotePage],
  );

  // ─── Record a view on the active note (best-effort, fire-and-forget) ───
  // Fires whenever the active note id changes — covers direct opens, tree
  // navigation, page-prev/next, and continue-reading clicks.
  const activeNoteId = note?.id;
  React.useEffect(() => {
    if (!activeNoteId) return;
    recordView(activeNoteId).catch(() => {
      /* view tracking is best-effort */
    });
  }, [activeNoteId, recordView]);

  // ─── Load recent views when the actions panel opens ───
  React.useEffect(() => {
    if (!actionsOpen) return;
    loadRecentViews(5).catch(() => {
      /* best-effort */
    });
  }, [actionsOpen, loadRecentViews]);

  // ─── Filter out the active note from the "Continue reading" list ───
  // (we don't want to suggest re-opening the note the user is reading).
  const visibleRecentViews = React.useMemo(() => {
    return recentViews.filter((v) => v.noteId !== activeNoteId).slice(0, 5);
  }, [recentViews, activeNoteId]);

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

  // Fit-to-view: in "fit" mode, applyNoteScale uses zoomMul=1 and
  // computes the fit scale directly from the container width. The
  // zoom state is only used in "manual" mode as a multiplier on top
  // of the fit scale, so no separate computeFitScale is needed.
  const computeFitScale = React.useCallback(() => {
    // Kept as a no-op for backwards-compat with any callers; the real
    // fit logic lives in applyNoteScale.
    setZoom(1);
  }, []);

  // ─── Note scaling (unified page object) ───────────────────────
  // The ENTIRE notebook sheet — spiral rings + ring shadows + page
  // shadow + the complete page design + a small intentional outer
  // margin — is treated as ONE renderable canvas. We measure the
  // note's true bounding box (including absolutely-positioned rings
  // and the box-shadow overflow), size the iframe to that exact box,
  // then scale the whole object as a unit to fit the viewport width.
  //
  // The note's internal design is NEVER modified — we only neutralize
  // the body's outer padding (which is decorative spacing for the raw
  // standalone file) so the page centers cleanly in the iframe. No
  // reflow, no redesign. Only the scale of the complete page object
  // adjusts responsively per device.
  const applyNoteScale = React.useCallback(() => {
    const iframe = iframeRef.current;
    const container = mainRef.current;
    if (!iframe || !container) return;
    try {
      const doc = iframe.contentDocument;
      if (!doc || !doc.body) return;

      // Inject left padding into the note's body so the spiral binding
      // rings (positioned at left:-30px on .page-wrapper, extending
      // ~40px beyond the page edge) have room to render fully. The
      // note's own body padding (24px 12px) is only 12px on the left,
      // which clips the rings. We add padding-left so the ring overflow
      // fits inside the iframe's content area.
      const RING_LEFT_SPACE = 80;  // px — covers 30px ring offset + 50px safety
      doc.body.style.paddingLeft = `${RING_LEFT_SPACE}px`;
      doc.body.style.paddingTop = "24px";
      doc.body.style.paddingBottom = "24px";
      doc.body.style.paddingRight = "24px";

      // Preserve the body's padding so the spiral binding rings
      // (positioned at left:-30px on .page-wrapper) have enough
      // space to be fully visible. The template CSS sets
      // body{padding:24px 48px} — we must NOT override it.
      // (Previously this neutralized padding which clipped the rings.)

      const avail = container.clientWidth;
      // Small intentional margin so the shadow/rings don't touch the
      // viewport edges. Kept constant in screen px (not scaled).
      const VIEWPORT_MARGIN = 16;
      const targetW = Math.max(0, avail - VIEWPORT_MARGIN * 2);

      // Find the page element (.page-wrapper / .page / .notebook).
      const pageEl =
        (doc.querySelector(".page-wrapper") as HTMLElement | null) ||
        (doc.querySelector(".page") as HTMLElement | null) ||
        (doc.querySelector(".notebook") as HTMLElement | null) ||
        (doc.body.firstElementChild as HTMLElement | null) ||
        doc.body;

      // Read the page's CSS width directly (the note uses a fixed
      // width:1080px on .page-wrapper). This is reliable regardless of
      // the iframe's current laid-out width, avoiding chicken-and-egg
      // measurement issues.
      const computedW = doc.defaultView?.getComputedStyle(pageEl).width;
      const parsedW = computedW ? parseFloat(computedW) : 0;
      const pageWNum = isFinite(parsedW) && parsedW > 0 ? parsedW : 1080;

      // The complete page object width = page + ring overflow (left) +
      // shadow spread (both sides). The rings extend ~40px left of the
      // page; the box-shadow spreads ~60px on all sides.
      const RING_OVERFLOW = 40;
      const SHADOW = 60;
      // The injected left padding (RING_LEFT_SPACE above) gives the rings
      // room to render inside the body. Subtract it from the ring overflow
      // so we don't double-count the space.
      const extraLeft = Math.max(0, RING_LEFT_SPACE - RING_OVERFLOW);
      const objectW = pageWNum + RING_OVERFLOW + extraLeft + SHADOW * 2;

      // Body height includes the page; add shadow for the bottom.
      const bodyH = Math.max(
        doc.body.scrollHeight,
        doc.body.offsetHeight,
        doc.documentElement.scrollHeight,
        doc.documentElement.offsetHeight,
      );
      const objectH = bodyH + SHADOW;

      // Base fit-to-width scale (page object fills the viewport).
      const fitScale = targetW < objectW ? targetW / objectW : 1;
      // Apply the user's zoom multiplier. In "fit" mode zoom stays at 1
      // (fitScale alone). In "manual" mode the user's zoom (0.25–4)
      // scales relative to the fit width.
      const zoomMul = zoomMode === "manual" ? zoom : 1;
      const scale = fitScale * zoomMul;

      // Size the iframe to the complete page object.
      const NATIVE_W = objectW;
      iframe.style.width = `${NATIVE_W}px`;
      iframe.style.height = `${objectH}px`;
      iframe.style.transform = `scale(${scale})`;
      iframe.style.transformOrigin = "top left";

      // Reserve the scaled footprint on the wrapper so the page can
      // scroll vertically and centers horizontally. When zoomed in
      // beyond the viewport width, the wrapper grows wider than the
      // container and the scroll container handles horizontal scroll.
      const wrapper = iframe.parentElement;
      if (wrapper) {
        wrapper.style.width = `${NATIVE_W * scale}px`;
        wrapper.style.height = `${objectH * scale}px`;
        wrapper.style.marginLeft = "auto";
        wrapper.style.marginRight = "auto";
      }
    } catch {
      /* cross-origin — ignore */
    }
  }, [zoom, zoomMode]);

  // Re-scale when the viewport changes (resize, tree toggle, orientation).
  React.useEffect(() => {
    const handler = () => applyNoteScale();
    window.addEventListener("resize", handler);
    return () => window.removeEventListener("resize", handler);
  }, [applyNoteScale]);
  React.useEffect(() => {
    // Re-measure shortly after the tree opens/closes (width changes).
    const t = setTimeout(applyNoteScale, 320);
    return () => clearTimeout(t);
  }, [treeOpen, applyNoteScale]);

  // Re-apply the scale whenever the user changes zoom / zoom mode.
  React.useEffect(() => {
    applyNoteScale();
  }, [applyNoteScale]);

  // ─── Zoom controls ────────────────────────────────────────────
  // Zoom is a MULTIPLIER on top of the fit-to-width scale. In "fit" mode
  // the multiplier is 1 (page fills the viewport). Switching to "manual"
  // via the +/- buttons starts from 1.0 (the fit baseline) and adds the
  // increment, so zoom-in always makes the page larger, never smaller.
  const zoomIn = React.useCallback(() => {
    setZoomMode("manual");
    setZoom((z) => {
      // If we were in fit mode, z holds a stale fit value (< 1 on
      // mobile). Reset to 1.0 baseline before applying the increment.
      const base = zoomMode === "fit" ? 1 : z;
      return Math.min(4, +(base + 0.1).toFixed(2));
    });
  }, [zoomMode]);
  const zoomOut = React.useCallback(() => {
    setZoomMode("manual");
    setZoom((z) => {
      const base = zoomMode === "fit" ? 1 : z;
      return Math.max(0.25, +(base - 0.1).toFixed(2));
    });
  }, [zoomMode]);
  const zoomTo = React.useCallback((value: number) => {
    setZoomMode("manual");
    setZoom(value);
  }, []);
  const zoomToFit = React.useCallback(() => {
    setZoomMode("fit");
    setZoom(1);
  }, []);

  // ─── Auto-hide the top nav bar when the tree opens ────────────
  // When the user opens the tree sidebar, the top navigation bar
  // collapses automatically so it doesn't compete for vertical space
  // and the tree gets the full viewport height. The user can re-expand
  // the nav bar via the collapsed handle (or the tree's own controls).
  React.useEffect(() => {
    if (treeOpen) setToolbarExpanded(false);
  }, [treeOpen]);

  // ─── Page layout (background pattern) ─────────────────────────
  // Inject/replace a style block in the note's document to swap the
  // page background. "grid" removes the override so the note's original
  // graph-paper shows through.
  const applyPageLayout = React.useCallback(() => {
    const iframe = iframeRef.current;
    if (!iframe) return;
    try {
      const doc = iframe.contentDocument;
      if (!doc) return;
      const STYLE_ID = "reader-page-layout";
      const existing = doc.getElementById(STYLE_ID);
      const layout = PAGE_LAYOUTS.find((l) => l.key === pageLayout);
      if (layout && layout.css) {
        if (existing) {
          existing.textContent = layout.css;
        } else {
          const style = doc.createElement("style");
          style.id = STYLE_ID;
          style.textContent = layout.css;
          doc.head.appendChild(style);
        }
      } else if (existing) {
        // "grid" → remove the override so the note's original shows.
        existing.remove();
      }
    } catch {
      /* cross-origin — ignore */
    }
  }, [pageLayout]);

  React.useEffect(() => {
    applyPageLayout();
  }, [applyPageLayout]);

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
      if (zoomPresetsOpen) {
        const inDesktop = zoomRef.current?.contains(e.target as Node) ?? false;
        const inMobile = mobileZoomRef.current?.contains(e.target as Node) ?? false;
        if (!inDesktop && !inMobile) setZoomPresetsOpen(false);
      }
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
        e.preventDefault(); zoomIn(); return;
      }
      if ((e.ctrlKey || e.metaKey) && e.key === "-") {
        e.preventDefault(); zoomOut(); return;
      }
      if ((e.ctrlKey || e.metaKey) && e.key === "0") {
        e.preventDefault(); zoomToFit(); return;
      }
      if (isTyping) return;
      if (e.key === "ArrowLeft" && !drawerOpen && !treeOpen && (hasPrevPage || showCover)) { e.preventDefault(); goToPrevPage(); }
      if (e.key === "ArrowRight" && !drawerOpen && !treeOpen && (hasNextPage || showCover)) { e.preventDefault(); goToNextPage(); }
      // "c" toggles the cover view (only for notes that have a cover).
      if ((e.key === "c" || e.key === "C") && !drawerOpen && !treeOpen && hasCoverPage) {
        e.preventDefault(); toggleCover();
      }
    };
    window.addEventListener("keydown", handleKey);
    return () => window.removeEventListener("keydown", handleKey);
  }, [drawerOpen, treeOpen, downloadOpen, actionsOpen, zoomPresetsOpen, hasPrevPage, hasNextPage, hasCoverPage, showCover, goToPrevPage, goToNextPage, toggleCover, zoomIn, zoomOut, zoomToFit]);

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
      {/* ═══ Tree sidebar ═══ */}
      {/* Desktop (≥768px): inline collapsible rail — 48px collapsed, 248px
          expanded. Mobile (<768px): no rail when closed; opens as a
          left-docked overlay drawer (w-85vw max 320px) with a backdrop.
          The tree-toggle + home buttons live ONLY in the tree panel
          header (when open) to avoid duplicating the top nav bar's
          tree/home buttons. When the tree is collapsed, the rail is
          hidden entirely — the top nav bar's Tree button re-opens it. */}
      <motion.aside
        key={isMobile ? "tree-mobile" : "tree-desktop"}
        initial={false}
        animate={
          isMobile
            ? { x: treeOpen ? "0%" : "-100%", opacity: treeOpen ? 1 : 0 }
            : { width: treeOpen ? 248 : 0 }
        }
        transition={{ type: "spring", damping: 30, stiffness: 300 }}
        className={cn(
          "shrink-0 overflow-hidden border-r border-slate-200 bg-slate-50",
          isMobile
            ? "absolute inset-y-0 left-0 z-50 w-[85vw] max-w-[320px] shadow-2xl"
            : "relative z-30",
        )}
      >
        <div className="flex h-full w-full md:w-[248px]">
          {/* ── Expandable content panel (clipped when collapsed) ── */}
          <div className="flex min-w-0 flex-1 flex-col">
            {/* Header — contains the tree toggle + home buttons (only
                visible when the tree is open, avoiding duplicates with
                the top nav bar). */}
            <div className="flex items-center justify-between border-b border-slate-200 bg-white px-3 py-2.5">
              <div className="flex items-center gap-1.5">
                <button
                  onClick={() => setTreeOpen(false)}
                  className="flex size-7 items-center justify-center rounded-md text-slate-500 transition-colors hover:bg-slate-100 hover:text-slate-900"
                  title="Collapse tree (Esc)"
                  aria-pressed={treeOpen}
                >
                  <FolderTree className="h-4 w-4" />
                </button>
                <button
                  onClick={goHome}
                  className="flex size-7 items-center justify-center rounded-md text-slate-500 transition-colors hover:bg-slate-100 hover:text-slate-900"
                  title="Back to home"
                >
                  <Home className="h-4 w-4" />
                </button>
                <span className="ml-1 text-sm font-semibold text-slate-900">Browse</span>
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
      {/* Mobile tree drawer backdrop */}
      <AnimatePresence>
        {isMobile && treeOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="absolute inset-0 z-40 bg-black/30"
            onClick={() => setTreeOpen(false)}
          />
        )}
      </AnimatePresence>

      {/* ═══ Document Viewer ═══ */}
      {/* When the top nav bar is visible, reserve its 40px height (h-10) so the
          document's top isn't hidden behind the overlay bar. */}
      <div className={cn("absolute inset-0 overflow-auto bg-[#cfc9bb]", toolbarExpanded && "pt-10")}>
        <AnimatePresence mode="wait">
          <motion.div
            key={note.id}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="mx-auto"
            style={{
              minHeight: "100%",
            }}
          >
            <iframe
              ref={iframeRef}
              title={note.title}
              src={note.contentPath}
              onLoad={(e) => {
                iframeRef.current = e.currentTarget;
                // The note's HTML/CSS is never modified — we measure its
                // true bounding box (rings + shadow + page) and scale the
                // whole object as a unit. No body padding, no reflow.
                // Detect pages (.page-wrapper elements) and show only the
                // first CONTENT page (skipping the cover if present).
                detectNotePages();
                applyNoteScale();
                applyPageLayout();
                // Re-apply after fonts/images settle (dimensions change).
                setTimeout(() => { detectNotePages(); applyNoteScale(); }, 400);
                setTimeout(() => { applyNoteScale(); }, 1200);
              }}
              className="block border-0 bg-[#cfc9bb]"
              style={{
                minHeight: "100vh",
              }}
            />
          </motion.div>
        </AnimatePresence>
      </div>

      {/* ═══ Top Navigation Bar (consolidated) ═══ */}
      {/* Single horizontal bar spanning the full width of the main area.
          Replaces the old floating top-left toolbar + top-right Pages/Actions
          cluster. Hide/show toggle on the far right reuses `toolbarExpanded`. */}
      <AnimatePresence>
        {toolbarExpanded ? (
          <motion.div
            key="navbar-expanded"
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ type: "spring", damping: 25, stiffness: 300 }}
            className="absolute left-0 right-0 top-0 z-30 flex h-10 items-center gap-1 border-b border-slate-200 bg-white/95 px-2 shadow-sm backdrop-blur-md"
          >
            {/* Group 1: Tree toggle + Home + Search */}
            <Button variant="ghost" size="icon" className="h-8 w-8"
              onClick={() => setTreeOpen(!treeOpen)}
              title={treeOpen ? "Collapse tree (Esc)" : "Browse categories (tree)"}
              aria-pressed={treeOpen}>
              <FolderTree className="h-4 w-4" />
            </Button>
            <Button variant="ghost" size="icon" className="h-8 w-8"
              onClick={goHome}
              title="Back to home">
              <Home className="h-4 w-4" />
            </Button>
            <Button variant="ghost" size="icon" className="h-8 w-8"
              onClick={openSearchModal}
              title="Search notes (Ctrl+K)">
              <Search className="h-4 w-4" />
            </Button>

            <Sep />

            {/* Group 2: Page navigation (prev / counter-input / next) */}
            {/* When showing the cover, the counter is replaced with a
                "Cover" label and prev/next are disabled. The cover is
                NOT counted in the page total. */}
            <Button variant="ghost" size="icon" className="h-8 w-8"
              disabled={!hasPrevPage || showCover}
              onClick={() => goToPrevPage()}
              title="Previous page (←)">
              <ChevronLeft className="h-4 w-4" />
            </Button>
            {showCover ? (
              <div className="flex items-center gap-1 text-xs font-mono">
                <span className="rounded bg-amber-100 px-2 py-0.5 text-[11px] font-semibold uppercase tracking-wide text-amber-700">
                  Cover
                </span>
                <span className="text-slate-400">/</span>
                <span className="min-w-[20px] text-center text-slate-600">{totalPages}</span>
              </div>
            ) : (
              <div className="flex items-center gap-0.5 text-xs font-mono text-slate-700">
                <input
                  type="text"
                  value={pageInputFocused ? pageInputValue : String(currentIndex + 1)}
                  onChange={(e) => setPageInputValue(e.target.value.replace(/[^0-9]/g, ""))}
                  onFocus={() => { setPageInputFocused(true); setPageInputValue(String(currentIndex + 1)); }}
                  onBlur={() => {
                    setPageInputFocused(false);
                    const n = parseInt(pageInputValue, 10);
                    if (!isNaN(n) && n >= 1 && n <= totalPages) goToPage(n - 1);
                  }}
                  onKeyDown={(e) => { if (e.key === "Enter") e.currentTarget.blur(); }}
                  className="h-7 w-8 rounded border border-transparent bg-slate-100 text-center text-xs font-mono outline-none transition-colors hover:bg-slate-200 focus:border-slate-300 focus:bg-white"
                  title="Type page number"
                />
                <span className="text-slate-400">/</span>
                <span className="min-w-[20px] text-center">{totalPages}</span>
              </div>
            )}
            <Button variant="ghost" size="icon" className="h-8 w-8" disabled={!hasNextPage || showCover}
              onClick={() => goToNextPage()}
              title="Next page (→)">
              <ChevronRight className="h-4 w-4" />
            </Button>

            {/* Cover toggle — only shown when the note has a cover page.
                Clicking it swaps between the cover view and the current
                content page WITHOUT affecting the page counter. */}
            {hasCoverPage && (
              <Button
                variant={showCover ? "secondary" : "ghost"}
                size="sm"
                className={cn(
                  "h-8 gap-1 px-2 text-xs",
                  showCover
                    ? "bg-amber-100 text-amber-700 hover:bg-amber-200 hover:text-amber-800"
                    : "text-slate-600 hover:bg-slate-100",
                )}
                onClick={toggleCover}
                title={showCover ? "Back to content" : "View cover page"}
                aria-pressed={showCover}
              >
                <BookImage className="h-3.5 w-3.5" />
                <span className="hidden sm:inline">Cover</span>
              </Button>
            )}

            {/* Group 3: Zoom (hidden on mobile — duplicates the actions panel's
                mobile zoom section to avoid horizontal overflow on 390px). */}
            <div className="hidden items-center gap-1 sm:flex">
              <Sep />
              <Button variant="ghost" size="icon" className="h-8 w-8"
                onClick={zoomOut}
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
                      <button onClick={() => { zoomToFit(); setZoomPresetsOpen(false); }}
                        className="flex w-full items-center gap-2 rounded-md px-2 py-1.5 text-xs text-slate-700 hover:bg-slate-100">
                        <Maximize className="h-3.5 w-3.5" /> Fit
                      </button>
                      <div className="my-1 h-px bg-slate-100" />
                      {["50%", "75%", "100%", "125%", "150%", "200%"].map(label => (
                        <button key={label} onClick={() => { zoomTo(parseInt(label) / 100); setZoomPresetsOpen(false); }}
                          className="flex w-full items-center gap-2 rounded-md px-2 py-1.5 text-xs text-slate-700 hover:bg-slate-100">
                          {label}
                        </button>
                      ))}
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
              <Button variant="ghost" size="icon" className="h-8 w-8"
                onClick={zoomIn}
                title="Zoom in (Ctrl +)">
                <ZoomIn className="h-4 w-4" />
              </Button>
            </div>

            <Sep />

            {/* Group 4: Fullscreen */}
            <Button variant="ghost" size="icon" className="h-8 w-8"
              onClick={toggleFullscreen} title={isFullscreen ? "Exit fullscreen" : "Enter fullscreen"}>
              {isFullscreen ? <Minimize className="h-4 w-4" /> : <Maximize className="h-4 w-4" />}
            </Button>

            <Sep />

            {/* Group 5: Pages drawer + Actions popover */}
            <Button variant="ghost" size="icon" className="h-8 w-8"
              onClick={() => setDrawerOpen(true)}
              title="Open pages">
              <Menu className="h-4 w-4" />
            </Button>
            <Button variant="ghost" size="icon" className="h-8 w-8"
              onClick={() => setActionsOpen(!actionsOpen)}
              title="Toggle actions">
              <MoreVertical className="h-4 w-4" />
            </Button>

            {/* Spacer pushes the hide toggle to the far right edge */}
            <div className="ml-auto flex items-center">
              <Sep />
              <Button variant="ghost" size="icon" className="h-8 w-8"
                onClick={() => setToolbarExpanded(false)}
                title="Hide toolbar (Esc)">
                <ChevronUp className="h-4 w-4" />
              </Button>
            </div>
          </motion.div>
        ) : (
          // Collapsed state: a small floating pill at top-center that
          // re-expands the bar on click. Shows the page counter so the
          // user always knows their position.
          <motion.button
            key="navbar-collapsed"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ delay: 0.1, duration: 0.2 }}
            className="absolute left-1/2 top-2 z-30 flex -translate-x-1/2 items-center gap-1.5 rounded-full border border-slate-200 bg-white/95 px-3 py-1.5 text-xs text-slate-600 shadow-md backdrop-blur-sm transition-colors hover:bg-white"
            onClick={() => setToolbarExpanded(true)}
            title="Show toolbar"
          >
            <ChevronDown className="h-3 w-3" />
            {showCover ? (
              <span className="font-mono uppercase tracking-wide">Cover · {totalPages}p</span>
            ) : (
              <span className="font-mono">{currentIndex + 1}/{totalPages}</span>
            )}
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
                    {Array.from({ length: totalPages }, (_, idx) => (
                      <button
                        key={idx}
                        onClick={() => { goToPage(idx); setDrawerOpen(false); }}
                        className={cn("flex w-full items-center rounded-lg border px-3 py-2.5 text-left",
                          idx === currentIndex ? "border-rose-200 bg-rose-50" : "border-transparent hover:bg-slate-50")}
                      >
                        <span className={cn("mr-3 font-mono text-xs", idx === currentIndex ? "font-bold text-rose-600" : "text-slate-400")}>
                          {String(idx + 1).padStart(2, "0")}
                        </span>
                        <span className={cn("truncate text-sm", idx === currentIndex ? "font-medium text-rose-900" : "text-slate-700")}>
                          {pageTitles[idx] || `Page ${idx + 1}`}
                        </span>
                      </button>
                    ))}
                  </div>
                ) : (
                  <div className="grid grid-cols-2 gap-2 p-3">
                    {Array.from({ length: totalPages }, (_, idx) => (
                      <button
                        key={idx}
                        onClick={() => { goToPage(idx); setDrawerOpen(false); }}
                        className={cn("overflow-hidden rounded-lg border-2 text-left",
                          idx === currentIndex ? "border-rose-400 shadow-md" : "border-slate-200 hover:border-slate-300")}
                      >
                        <div className="border-b border-slate-100 bg-slate-50 px-2 py-1 text-center text-[10px] font-semibold">
                          {String(idx + 1).padStart(2, "0")}
                        </div>
                        {/* Page title/overview preview */}
                        <div className="relative flex aspect-[3/4] flex-col overflow-hidden bg-white p-2">
                          <span className="line-clamp-3 text-[10px] font-bold leading-tight text-slate-700">
                            {pageTitles[idx] || `Page ${idx + 1}`}
                          </span>
                          <span className="mt-auto text-[9px] text-slate-400">
                            Page {idx + 1} of {totalPages}
                          </span>
                        </div>
                        <div className="truncate border-t border-slate-100 bg-slate-50 px-2 py-1 text-[10px] text-slate-600">
                          {pageTitles[idx] ? pageTitles[idx].slice(0, 30) + (pageTitles[idx].length > 30 ? "…" : "") : `Page ${idx + 1}`}
                        </div>
                      </button>
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
            className="absolute right-[45px] top-14 z-30 max-h-[calc(100vh-5rem)] w-52 overflow-y-auto rounded-xl border border-slate-200 bg-white/95 p-3 shadow-lg backdrop-blur-md"
          >
            {/* Mobile: Navigation (the inline icon rail is hidden below md:) */}
            <div className="mb-2 border-b border-slate-100 pb-2 md:hidden">
              <div className="mb-1 px-2 text-[10px] font-bold uppercase tracking-wider text-slate-400">
                Navigate
              </div>
              <div className="space-y-1">
                <ActionBtn icon={FolderTree} label="Browse tree" onClick={() => setTreeOpen(true)} />
                <ActionBtn icon={Home} label="Back to home" onClick={goHome} />
              </div>
            </div>
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

            {/* Mobile: Zoom controls (toolbar zoom group is hidden below sm:) */}
            <div className="mt-2 border-t border-slate-100 pt-2 sm:hidden" ref={mobileZoomRef}>
              <div className="mb-1 flex items-center justify-between px-2">
                <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Zoom</span>
                <span className="font-mono text-[10px] text-slate-500">{zoomLabel}</span>
              </div>
              <div className="flex items-center gap-1 px-1">
                <Button variant="ghost" size="icon" className="h-8 w-8 rounded-full"
                  onClick={zoomOut}
                  title="Zoom out">
                  <ZoomOut className="h-4 w-4" />
                </Button>
                <Button variant="ghost" size="icon" className="h-8 w-8 rounded-full"
                  onClick={zoomIn}
                  title="Zoom in">
                  <ZoomIn className="h-4 w-4" />
                </Button>
                <button
                  className="ml-auto rounded border border-transparent bg-slate-100 px-2 py-1 text-[10px] text-slate-600 transition-colors hover:border-slate-300 hover:bg-slate-200"
                  onClick={() => setZoomPresetsOpen(!zoomPresetsOpen)}
                >
                  {zoomPresetsOpen ? "Hide" : "Presets"}
                </button>
              </div>
              <AnimatePresence>
                {zoomPresetsOpen && (
                  <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: "auto", opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    transition={{ duration: 0.2 }}
                    className="overflow-hidden"
                  >
                    <div className="mt-1 grid grid-cols-3 gap-1 border-t border-slate-100 p-2">
                      <button onClick={() => { zoomToFit(); setZoomPresetsOpen(false); }}
                        className="flex items-center justify-center gap-1 rounded-md px-2 py-1.5 text-[11px] text-slate-700 hover:bg-slate-100">
                        <Maximize className="h-3 w-3" /> Fit
                      </button>
                      {["50%", "75%", "100%", "125%", "150%", "200%"].map(label => (
                        <button key={label} onClick={() => { zoomTo(parseInt(label) / 100); setZoomPresetsOpen(false); }}
                          className="rounded-md px-2 py-1.5 text-center text-[11px] text-slate-700 hover:bg-slate-100">
                          {label}
                        </button>
                      ))}
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
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

            {/* Page layout — background pattern selector */}
            <div className="mt-2 border-t border-slate-100 pt-2">
              <div className="mb-1.5 px-2 text-[10px] font-bold uppercase tracking-wider text-slate-400">
                Page layout
              </div>
              <div className="grid grid-cols-4 gap-1.5 px-1">
                {PAGE_LAYOUTS.map((layout) => (
                  <button
                    key={layout.key}
                    onClick={() => setPageLayout(layout.key)}
                    title={layout.label}
                    className={cn(
                      "flex flex-col items-center gap-1 rounded-md border p-1.5 transition-colors",
                      pageLayout === layout.key
                        ? "border-emerald-500 bg-emerald-50 dark:bg-emerald-950/30"
                        : "border-slate-200 hover:border-slate-300 hover:bg-slate-50",
                    )}
                  >
                    {/* Mini preview swatch of the pattern */}
                    <span
                      className="block h-7 w-full rounded-sm border border-slate-200 bg-[#f5f1e8]"
                      style={
                        layout.key === "grid"
                          ? {
                              backgroundImage:
                                "linear-gradient(to right, #bcc8d6 1px, transparent 1px), linear-gradient(to bottom, #bcc8d6 1px, transparent 1px)",
                              backgroundSize: "6px 6px",
                            }
                          : layout.key === "plain"
                            ? { backgroundImage: "none" }
                            : layout.key === "lined"
                              ? {
                                  backgroundImage:
                                    "linear-gradient(to bottom, #b8c5d6 1px, transparent 1px)",
                                  backgroundSize: "100% 5px",
                                }
                              : {
                                  backgroundImage:
                                    "radial-gradient(circle, #b8c5d6 1px, transparent 1px)",
                                  backgroundSize: "5px 5px",
                                }
                      }
                    />
                    <span
                      className={cn(
                        "text-[10px]",
                        pageLayout === layout.key
                          ? "font-semibold text-emerald-700 dark:text-emerald-300"
                          : "text-slate-500",
                      )}
                    >
                      {layout.label}
                    </span>
                  </button>
                ))}
              </div>
            </div>

            {/* Continue reading — recently viewed notes */}
            <div className="mt-3 border-t border-slate-100 pt-2">
              <div className="mb-1 flex items-center justify-between px-2">
                <div className="flex items-center gap-1.5 text-[10px] font-bold uppercase tracking-wider text-slate-400">
                  <History className="h-3 w-3" /> Continue Reading
                </div>
                {visibleRecentViews.length > 0 && (
                  <button
                    onClick={() => clearRecent().catch(() => { /* ignore */ })}
                    className="flex items-center gap-1 text-[10px] text-slate-400 transition-colors hover:text-rose-600"
                    title="Clear history"
                  >
                    <Trash2 className="h-3 w-3" />
                    Clear
                  </button>
                )}
              </div>

              {recentLoading ? (
                <div className="space-y-1 px-1 py-1">
                  <Skeleton className="h-7 w-full rounded-md" />
                  <Skeleton className="h-7 w-full rounded-md" />
                  <Skeleton className="h-7 w-3/4 rounded-md" />
                </div>
              ) : visibleRecentViews.length === 0 ? (
                <div className="px-2 py-2 text-[11px] text-slate-400">
                  No recently viewed notes yet.
                </div>
              ) : (
                <ScrollArea className="max-h-52">
                  <div className="space-y-0.5 px-1 py-0.5">
                    {visibleRecentViews.map((v) => {
                      const target = v.note;
                      const isDisabled = !target;
                      return (
                        <button
                          key={v.id}
                          onClick={() => {
                            if (!target) return;
                            handleNavigate(target);
                          }}
                          disabled={isDisabled}
                          className="flex w-full items-start gap-2 rounded-md px-2 py-1.5 text-left text-xs text-slate-600 transition-colors hover:bg-slate-100 disabled:cursor-not-allowed disabled:opacity-50"
                          title={target ? target.title : "Note no longer available"}
                        >
                          <FileText className="mt-0.5 h-3 w-3 shrink-0 text-slate-400" />
                          <span className="min-w-0 flex-1">
                            <span className="block truncate font-medium text-slate-700">
                              {target ? target.title : "(deleted)"}
                            </span>
                            <span className="flex items-center gap-1 text-[10px] text-slate-400">
                              <Clock className="h-2.5 w-2.5" />
                              {fromNow(v.viewedAt)}
                            </span>
                          </span>
                        </button>
                      );
                    })}
                  </div>
                </ScrollArea>
              )}
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
