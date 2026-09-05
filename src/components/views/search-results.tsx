"use client";

import * as React from "react";
import {
  ArrowLeft,
  Filter,
  FolderTree,
  Loader2,
  Search as SearchIcon,
  SearchX,
  Tag,
} from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { NoteCard, NoteCardSkeleton } from "@/components/note-card";
import { useAppStore } from "@/lib/store";
import { formatDate } from "@/lib/format";

export function SearchResults() {
  const searchQuery = useAppStore((s) => s.searchQuery);
  const searchResults = useAppStore((s) => s.searchResults);
  const searching = useAppStore((s) => s.searching);
  const setSearchQuery = useAppStore((s) => s.setSearchQuery);
  const runSearch = useAppStore((s) => s.runSearch);
  const categories = useAppStore((s) => s.categories);
  const categoryFilter = useAppStore((s) => s.searchCategoryFilter);
  const setCategoryFilter = useAppStore((s) => s.setSearchCategoryFilter);
  const openNote = useAppStore((s) => s.openNote);
  const goHome = useAppStore((s) => s.goHome);

  const [localQuery, setLocalQuery] = React.useState(searchQuery);
  React.useEffect(() => setLocalQuery(searchQuery), [searchQuery]);

  const filtered = React.useMemo(() => {
    if (!categoryFilter) return searchResults;
    return searchResults.filter(
      (n) =>
        n.categoryId === categoryFilter ||
        n.category?.parentId === categoryFilter,
    );
  }, [searchResults, categoryFilter]);

  const onSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    runSearch(localQuery);
  };

  const topLevelCategories = React.useMemo(
    () => categories.filter((c) => !c.parentId),
    [categories],
  );

  return (
    <div className="mx-auto w-full max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
      <div className="mb-4">
        <Button
          variant="ghost"
          size="sm"
          onClick={goHome}
          className="gap-1 text-muted-foreground"
        >
          <ArrowLeft className="size-4" />
          Back to home
        </Button>
      </div>

      {/* Search bar */}
      <form onSubmit={onSubmit} className="mb-4">
        <div className="relative">
          <SearchIcon className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            value={localQuery}
            onChange={(e) => setLocalQuery(e.target.value)}
            placeholder="Search notes, tags, descriptions…"
            className="h-11 pl-9"
            aria-label="Search the knowledge base"
          />
        </div>
      </form>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-[220px_1fr]">
        {/* Filters */}
        <aside className="lg:sticky lg:top-20 lg:self-start">
          <Card>
            <CardContent className="flex flex-col gap-3 p-4">
              <div className="flex items-center gap-2 text-sm font-medium">
                <Filter className="size-4 text-emerald-600 dark:text-emerald-400" />
                Filters
              </div>
              <div className="flex flex-col gap-1.5">
                <span className="text-xs text-muted-foreground">Category</span>
                <Select
                  value={categoryFilter ?? "ALL"}
                  onValueChange={(v) =>
                    setCategoryFilter(v === "ALL" ? null : v)
                  }
                >
                  <SelectTrigger className="w-full">
                    <SelectValue placeholder="All categories" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="ALL">All categories</SelectItem>
                    {topLevelCategories.map((c) => (
                      <SelectItem key={c.id} value={c.id}>
                        {c.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {topLevelCategories.length > 0 && (
                <div className="flex flex-col gap-1.5">
                  <span className="text-xs text-muted-foreground">
                    Quick filter
                  </span>
                  <div className="flex flex-wrap gap-1.5">
                    {topLevelCategories.map((c) => (
                      <button
                        key={c.id}
                        onClick={() =>
                          setCategoryFilter(
                            categoryFilter === c.id ? null : c.id,
                          )
                        }
                        className={
                          "rounded-full border px-2 py-0.5 text-xs transition-colors " +
                          (categoryFilter === c.id
                            ? "border-emerald-500/40 bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300"
                            : "border-border/60 text-muted-foreground hover:text-foreground")
                        }
                      >
                        {c.name}
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </aside>

        {/* Results */}
        <div className="min-w-0">
          <div className="mb-4 flex flex-wrap items-center justify-between gap-2">
            <div>
              <h1 className="text-xl font-semibold tracking-tight">
                {searching ? (
                  <span className="flex items-center gap-2">
                    <Loader2 className="size-4 animate-spin" />
                    Searching…
                  </span>
                ) : searchQuery ? (
                  <>Results for “{searchQuery}”</>
                ) : (
                  <>All notes</>
                )}
              </h1>
              <p className="text-sm text-muted-foreground">
                {searching
                  ? "Searching across titles, descriptions, and tags."
                  : `${filtered.length} ${
                      filtered.length === 1 ? "note" : "notes"
                    } found`}
              </p>
            </div>
          </div>

          {searching ? (
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3">
              {Array.from({ length: 6 }).map((_, i) => (
                <NoteCardSkeleton key={i} />
              ))}
            </div>
          ) : filtered.length === 0 ? (
            <EmptyResults />
          ) : (
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3">
              {filtered.map((note) => (
                <NoteCard
                  key={note.id}
                  note={note}
                  onOpen={(n) => openNote(n)}
                />
              ))}
            </div>
          )}

          {/* List view fallback (denser) */}
          {!searching && filtered.length > 0 && (
            <Card className="mt-6">
              <CardContent className="px-0 pb-0">
                <div className="border-b border-border/60 px-6 py-3 text-sm font-medium">
                  Compact list
                </div>
                <ul className="divide-y divide-border/60">
                  {filtered.map((note) => (
                    <li key={note.id}>
                      <button
                        onClick={() => openNote(note)}
                        className="flex w-full items-start gap-3 px-6 py-3 text-left transition-colors hover:bg-muted/40"
                      >
                        <span className="mt-0.5 flex size-8 shrink-0 items-center justify-center rounded-md bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300">
                          {note.tags?.[0] ? (
                            <Tag className="size-3.5" />
                          ) : (
                            <FolderTree className="size-3.5" />
                          )}
                        </span>
                        <div className="min-w-0 flex-1">
                          <div className="flex flex-wrap items-center gap-2">
                            <span className="text-sm font-medium">
                              {note.title}
                            </span>
                            {note.category && (
                              <Badge
                                variant="outline"
                                className="font-normal text-muted-foreground"
                              >
                                {note.category.name}
                              </Badge>
                            )}
                          </div>
                          <p className="line-clamp-1 text-xs text-muted-foreground">
                            {note.description ?? "No description provided."}
                          </p>
                          <p className="mt-1 text-[11px] text-muted-foreground">
                            Updated {formatDate(note.updatedAt)}
                          </p>
                        </div>
                      </button>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}

function EmptyResults() {
  const runSearch = useAppStore((s) => s.runSearch);
  return (
    <Card className="border-dashed">
      <CardContent className="flex flex-col items-center justify-center gap-3 p-12 text-center">
        <span className="flex size-12 items-center justify-center rounded-full bg-muted text-muted-foreground">
          <SearchX className="size-6" />
        </span>
        <div>
          <p className="text-sm font-medium">No matching notes</p>
          <p className="text-xs text-muted-foreground">
            Try a different search term or remove filters.
          </p>
        </div>
        <Button
          variant="outline"
          size="sm"
          onClick={() => runSearch("")}
          className="gap-1"
        >
          Show all notes
        </Button>
      </CardContent>
    </Card>
  );
}
