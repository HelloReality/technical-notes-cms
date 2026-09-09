"use client";

import * as React from "react";
import { ArrowUpRight } from "lucide-react";

import { cn } from "@/lib/utils";
import type { Note } from "@/lib/types";

interface NoteCoverThumbProps {
  note: Note;
  onOpen?: (note: Note) => void;
  className?: string;
}

/**
 * Renders a scaled-down live preview of a note's COVER page inside a card.
 *
 * The note's HTML (served at `note.contentPath`) may contain many
 * `.page-wrapper` elements. The first one is typically a cover page
 * (it contains a `.cover` element). We load the full note into a hidden
 * iframe, then inject CSS so only the cover wrapper is visible, and scale
 * the whole page object down to fit a small thumbnail box.
 *
 * This is the same note file the viewer uses, so the browser cache serves
 * the iframe instantly after the first load. The iframe only mounts when
 * the thumbnail scrolls into view (IntersectionObserver) to keep the
 * home page fast.
 */
export function NoteCoverThumb({
  note,
  onOpen,
  className,
}: NoteCoverThumbProps) {
  const containerRef = React.useRef<HTMLDivElement>(null);
  const iframeRef = React.useRef<HTMLIFrameElement>(null);
  const [mounted, setMounted] = React.useState(false);
  const [ready, setReady] = React.useState(false);
  const [hasCover, setHasCover] = React.useState(true);

  // Lazy-mount the iframe only when the thumbnail scrolls into view.
  React.useEffect(() => {
    const el = containerRef.current;
    if (!el) return;
    if (mounted) return;
    const io = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            setMounted(true);
            io.disconnect();
            break;
          }
        }
      },
      { rootMargin: "200px" },
    );
    io.observe(el);
    return () => io.disconnect();
  }, [mounted]);

  // Once the iframe loads, hide everything except the first .page-wrapper
  // and scale it to fit the thumbnail container.
  const handleLoad = React.useCallback(() => {
    const iframe = iframeRef.current;
    const container = containerRef.current;
    if (!iframe || !container) return;
    try {
      const doc = iframe.contentDocument;
      if (!doc || !doc.body) return;

      // Detect cover: first .page-wrapper containing `.cover`.
      const wrappers = doc.querySelectorAll(".page-wrapper");
      let coverIdx = 0;
      if (wrappers.length > 0) {
        const first = wrappers[0] as HTMLElement;
        if (!first.querySelector(".cover")) {
          // No cover page — fall back to showing the first page anyway.
          setHasCover(false);
        }
      }

      // Hide every wrapper except the cover (first) one.
      wrappers.forEach((el, i) => {
        (el as HTMLElement).style.display = i === coverIdx ? "" : "none";
      });

      // Neutralize the body's outer padding so the page sits flush in
      // the thumbnail (the standalone file uses padding for display).
      doc.body.style.padding = "0";
      doc.body.style.margin = "0";
      doc.body.style.background = "#f5f1e8";

      // Measure the cover page and scale to fit the container width.
      const pageEl =
        (doc.querySelector(".page-wrapper") as HTMLElement | null) ||
        (doc.querySelector(".page") as HTMLElement | null) ||
        (doc.body.firstElementChild as HTMLElement | null) ||
        doc.body;

      // Read the page's intrinsic width (e.g. 1080px on .page).
      const computedW = doc.defaultView?.getComputedStyle(pageEl).width;
      const parsedW = computedW ? parseFloat(computedW) : 0;
      const pageW = isFinite(parsedW) && parsedW > 0 ? parsedW : 1080;
      // Body height includes the page; use the page's own height when
      // available so the thumbnail matches the page aspect ratio.
      const pageH =
        pageEl.scrollHeight || pageEl.offsetHeight || Math.round(pageW * 1.25);

      const availW = container.clientWidth;
      const scale = availW < pageW ? availW / pageW : 1;

      iframe.style.width = `${pageW}px`;
      iframe.style.height = `${pageH}px`;
      iframe.style.transform = `scale(${scale})`;
      iframe.style.transformOrigin = "top left";
      iframe.style.position = "absolute";
      iframe.style.top = "0";
      iframe.style.left = "0";

      // Reserve the scaled footprint so the container has the right height.
      const wrapper = iframe.parentElement;
      if (wrapper) {
        wrapper.style.width = `${pageW * scale}px`;
        wrapper.style.height = `${pageH * scale}px`;
      }
      setReady(true);
    } catch {
      /* cross-origin — ignore */
    }
  }, []);

  return (
    <div
      ref={containerRef}
      className={cn(
        "group/cover relative aspect-[4/5] w-full overflow-hidden rounded-lg border border-border/60 bg-[#f5f1e8] shadow-inner",
        className,
      )}
    >
      {/* Loading shimmer until the iframe is ready */}
      {!ready && (
        <div className="absolute inset-0 animate-pulse bg-gradient-to-br from-muted/60 to-muted" />
      )}

      {/* The scaled iframe — only mounted when scrolled into view */}
      {mounted && (
        <div className="absolute left-1/2 top-0 -translate-x-1/2">
          <iframe
            ref={iframeRef}
            src={note.contentPath}
            title={`${note.title} — cover`}
            loading="lazy"
            onLoad={handleLoad}
            className="pointer-events-none block border-0 bg-[#f5f1e8]"
            style={{ minHeight: "100px" }}
            tabIndex={-1}
            aria-hidden="true"
          />
        </div>
      )}

      {/* No-cover fallback badge (shown briefly until we know) */}
      {ready && !hasCover && (
        <div className="absolute left-2 top-2 rounded-full bg-amber-100 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wide text-amber-700">
          Page 1
        </div>
      )}

      {/* Click + Open overlay */}
      <button
        type="button"
        onClick={() => onOpen?.(note)}
        className="absolute inset-0 flex items-end justify-end bg-transparent p-3 text-left transition-colors hover:bg-emerald-950/10 focus:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 focus-visible:ring-offset-2"
        aria-label={`Open note: ${note.title}`}
      >
        <span className="flex items-center gap-1 rounded-full bg-white/90 px-2.5 py-1 text-xs font-medium text-emerald-700 opacity-0 shadow-sm backdrop-blur-sm transition-opacity group-hover/cover:opacity-100 dark:bg-slate-900/90 dark:text-emerald-300">
          Open note
          <ArrowUpRight className="size-3.5" />
        </span>
      </button>
    </div>
  );
}
