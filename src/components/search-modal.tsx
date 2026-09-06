"use client";

import * as React from "react";
import {
  CornerDownLeft,
  FileText,
  FolderTree,
  Hash,
  Search,
  SearchX,
  Tag,
} from "lucide-react";

import {
  Dialog,
  DialogContent,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { useAppStore } from "@/lib/store";
import { fromNow, formatDate } from "@/lib/format";
import type { Note } from "@/lib/types";
import { cn } from "@/lib/utils";

/**
 * Global search modal — a command-palette style window that lists every note
 * matching the query, with title, description, category breadcrumb, tags and
 * updated time so the user can pick the right one.
 */
export function SearchModal() {
  const open = useAppStore((s) => s.searchModalOpen);
  const closeSearchModal = useAppStore((s) => s.closeSearchModal);
  const notes = useAppStore((s) => s.notes);
  const categories = useAppStore((s) => s.categories);
  const openNote = useAppStore((s) => s.openNote);
  const goSearch = useAppStore((s) => s.goSearch);

  const [query, setQuery] = React.useState("");
  const [activeIndex, setActiveIndex] = React.useState(0);
  const inputRef = React.useRef<HTMLInputElement>(null);
  const listRef = React.useRef<HTMLDivElement>(null);

  // Reset query whenever the modal opens
  React.useEffect(() => {
    if (open) {
      setQuery("");
      setActiveIndex(0);
      const t = setTimeout(() => inputRef.current?.focus(), 50);
      return () => clearTimeout(t);
    }
  }, [open]);

  // ─── Live filtering across title / description / category / tags ───────
  const results = React.useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return notes;
    return notes.filter((n) => {
      const inTitle = n.title.toLowerCase().includes(q);
      const inDesc = n.description?.toLowerCase().includes(q);
      const inCat = n.category?.name.toLowerCase().includes(q);
      const inSubcat = n.subcategory?.name?.toLowerCase().includes(q);
      const inTags = n.tags?.some((t) => t.name.toLowerCase().includes(q));
      return inTitle || inDesc || inCat || inSubcat || inTags;
    });
  }, [query, notes]);

  // Keep activeIndex in range when results shrink
  React.useEffect(() => {
    if (activeIndex >= results.length) setActiveIndex(0);
  }, [results.length, activeIndex]);

  // Scroll active item into view
  React.useEffect(() => {
    const el = listRef.current?.querySelector<HTMLElement>(
      `[data-result-index="${activeIndex}"]`,
    );
    el?.scrollIntoView({ block: "nearest" });
  }, [activeIndex]);

  const handleSelect = React.useCallback(
    (note: Note) => {
      closeSearchModal();
      openNote(note);
    },
    [closeSearchModal, openNote],
  );

  const onKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setActiveIndex((i) => Math.min(i + 1, results.length - 1));
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setActiveIndex((i) => Math.max(i - 1, 0));
    } else if (e.key === "Enter") {
      e.preventDefault();
      const picked = results[activeIndex];
      if (picked) handleSelect(picked);
    }
  };

  // Quick category buckets for the left rail (top-level categories)
  const topCategories = React.useMemo(
    () => categories.filter((c) => !c.parentId),
    [categories],
  );

  return (
    <Dialog open={open} onOpenChange={(o) => (o ? null : closeSearchModal())}>
      <DialogContent
        className="grid gap-0 overflow-hidden p-0 sm:max-w-2xl"
        onKeyDown={onKeyDown}
      >
        <DialogTitle className="sr-only">Search notes</DialogTitle>
        <DialogDescription className="sr-only">
          Search across all notes by title, description, category or tag. Use
          arrow keys to navigate and Enter to open.
        </DialogDescription>

        {/* Search input */}
        <div className="flex items-center gap-2 border-b border-border/60 px-4 py-3">
          <Search className="size-4 shrink-0 text-muted-foreground" />
          <input
            ref={inputRef}
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
              setActiveIndex(0);
            }}
            placeholder="Search notes, tags, topics…"
            className="flex-1 bg-transparent text-sm outline-none placeholder:text-muted-foreground"
            aria-label="Search notes"
          />
          <kbd className="hidden shrink-0 rounded border border-border/60 bg-muted px-1.5 py-0.5 text-[10px] font-mono text-muted-foreground sm:inline">
            ESC
          </kbd>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-[180px_1fr]">
          {/* Left rail: quick category buckets */}
          <aside className="hidden flex-col border-r border-border/60 bg-muted/30 p-2 sm:flex">
            <div className="px-2 py-1.5 text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">
              Categories
            </div>
            <ScrollArea className="h-[420px]">
              <div className="space-y-0.5 pr-2">
                <button
                  onClick={() => setQuery("")}
                  className={cn(
                    "flex w-full items-center gap-2 rounded-md px-2 py-1.5 text-left text-xs transition-colors",
                    query.trim() === ""
                      ? "bg-emerald-50 font-medium text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300"
                      : "text-muted-foreground hover:bg-muted hover:text-foreground",
                  )}
                >
                  <FolderTree className="size-3.5" />
                  All notes
                  <span className="ml-auto text-[10px] text-muted-foreground">
                    {notes.length}
                  </span>
                </button>
                {topCategories.map((c) => {
                  const count = notes.filter(
                    (n) =>
                      n.categoryId === c.id ||
                      n.category?.parentId === c.id,
                  ).length;
                  if (count === 0) return null;
                  return (
                    <button
                      key={c.id}
                      onClick={() => setQuery(c.name)}
                      className={cn(
                        "flex w-full items-center gap-2 rounded-md px-2 py-1.5 text-left text-xs transition-colors",
                        query.trim().toLowerCase() ===
                          c.name.toLowerCase()
                          ? "bg-emerald-50 font-medium text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300"
                          : "text-muted-foreground hover:bg-muted hover:text-foreground",
                      )}
                    >
                      <Hash className="size-3.5" />
                      <span className="truncate">{c.name}</span>
                      <span className="ml-auto text-[10px] text-muted-foreground">
                        {count}
                      </span>
                    </button>
                  );
                })}
              </div>
            </ScrollArea>
          </aside>

          {/* Results list */}
          <div className="min-h-0">
            <div className="flex items-center justify-between border-b border-border/60 px-4 py-2 text-xs text-muted-foreground">
              <span>
                {query.trim() ? (
                  <>
                    {results.length} result
                    {results.length === 1 ? "" : "s"} for{" "}
                    <span className="font-medium text-foreground">
                      “{query}”
                    </span>
                  </>
                ) : (
                  <>All notes ({results.length})</>
                )}
              </span>
              {results.length > 0 && (
                <span className="hidden items-center gap-1 sm:flex">
                  <kbd className="rounded border border-border/60 bg-muted px-1 py-0.5 text-[10px] font-mono">
                    ↑↓
                  </kbd>
                  navigate
                  <kbd className="ml-2 rounded border border-border/60 bg-muted px-1 py-0.5 text-[10px] font-mono">
                    ↵
                  </kbd>
                  open
                </span>
              )}
            </div>

            <ScrollArea className="h-[420px]">
              {results.length === 0 ? (
                <EmptyState query={query} />
              ) : (
                <div ref={listRef} className="p-2">
                  {results.map((note, idx) => (
                    <ResultRow
                      key={note.id}
                      note={note}
                      index={idx}
                      active={idx === activeIndex}
                      onSelect={handleSelect}
                      onHover={() => setActiveIndex(idx)}
                    />
                  ))}
                </div>
              )}
            </ScrollArea>
          </div>
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between border-t border-border/60 bg-muted/30 px-4 py-2 text-[11px] text-muted-foreground">
          <span className="flex items-center gap-1.5">
            <CornerDownLeft className="size-3" /> to open
          </span>
          <button
            onClick={() => {
              closeSearchModal();
              goSearch(query);
            }}
            className="font-medium text-emerald-600 hover:underline dark:text-emerald-400"
          >
            Open full search page →
          </button>
        </div>
      </DialogContent>
    </Dialog>
  );
}

// ─── Result row ──────────────────────────────────────────────────
function ResultRow({
  note,
  index,
  active,
  onSelect,
  onHover,
}: {
  note: Note;
  index: number;
  active: boolean;
  onSelect: (n: Note) => void;
  onHover: () => void;
}) {
  const breadcrumb = [note.category?.name, note.subcategory?.name]
    .filter(Boolean)
    .join(" › ");

  return (
    <button
      data-result-index={index}
      onMouseMove={onHover}
      onClick={() => onSelect(note)}
      className={cn(
        "flex w-full items-start gap-3 rounded-lg border px-3 py-2.5 text-left transition-colors",
        active
          ? "border-emerald-500/40 bg-emerald-50 dark:bg-emerald-950/30"
          : "border-transparent hover:bg-muted/60",
      )}
    >
      <span
        className={cn(
          "mt-0.5 flex size-8 shrink-0 items-center justify-center rounded-md",
          active
            ? "bg-emerald-600 text-white"
            : "bg-muted text-muted-foreground",
        )}
      >
        <FileText className="size-4" />
      </span>
      <div className="min-w-0 flex-1">
        <div className="flex flex-wrap items-center gap-2">
          <span className="truncate text-sm font-medium">{note.title}</span>
          {note.tags?.slice(0, 3).map((t) => (
            <Badge
              key={t.id}
              variant="outline"
              className="gap-0.5 text-[10px] font-normal text-muted-foreground"
            >
              <Tag className="size-2.5" />
              {t.name}
            </Badge>
          ))}
        </div>
        <p className="mt-0.5 line-clamp-1 text-xs text-muted-foreground">
          {note.description?.trim() || "No description provided."}
        </p>
        <div className="mt-1 flex items-center gap-2 text-[11px] text-muted-foreground">
          {breadcrumb && (
            <span className="flex items-center gap-1">
              <FolderTree className="size-3" />
              {breadcrumb}
            </span>
          )}
          <span>·</span>
          <span>Updated {fromNow(note.updatedAt)}</span>
          <span className="hidden sm:inline">·</span>
          <span className="hidden sm:inline">{formatDate(note.updatedAt)}</span>
        </div>
      </div>
      {active && (
        <CornerDownLeft className="mt-1 size-3.5 shrink-0 text-emerald-600 dark:text-emerald-400" />
      )}
    </button>
  );
}

// ─── Empty state ─────────────────────────────────────────────────
function EmptyState({ query }: { query: string }) {
  return (
    <div className="flex flex-col items-center justify-center gap-2 px-6 py-12 text-center">
      <span className="flex size-10 items-center justify-center rounded-full bg-muted text-muted-foreground">
        <SearchX className="size-5" />
      </span>
      <div>
        <p className="text-sm font-medium">No matching notes</p>
        <p className="text-xs text-muted-foreground">
          {query.trim()
            ? `Nothing matched “${query}”. Try a different keyword.`
            : "There are no notes to display yet."}
        </p>
      </div>
    </div>
  );
}
