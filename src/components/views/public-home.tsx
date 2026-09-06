"use client";

import * as React from "react";
import {
  ArrowRight,
  BookOpen,
  Cloud,
  Code2,
  Database,
  FolderTree,
  Network,
  Search,
  Server,
  ShieldCheck,
  Sparkles,
} from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  NoteCard,
  NoteCardSkeleton,
} from "@/components/note-card";
import { useAppStore } from "@/lib/store";
import { DEFAULT_CATEGORY_PILLS, type Note } from "@/lib/types";
import { cn } from "@/lib/utils";

const PILL_ICONS: Record<string, React.ElementType> = {
  cybersecurity: ShieldCheck,
  development: Code2,
  devops: Server,
  cloud: Cloud,
  networking: Network,
  databases: Database,
  "ai-ml": Sparkles,
  web: BookOpen,
};

export function PublicHome() {
  const notes = useAppStore((s) => s.notes);
  const dataLoading = useAppStore((s) => s.dataLoading);
  const categories = useAppStore((s) => s.categories);
  const runSearch = useAppStore((s) => s.runSearch);
  const setSearchQuery = useAppStore((s) => s.setSearchQuery);
  const openNote = useAppStore((s) => s.openNote);

  const [heroSearch, setHeroSearch] = React.useState("");

  const onSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSearchQuery(heroSearch);
    runSearch(heroSearch);
  };

  const latestNotes = React.useMemo(() => {
    return [...notes]
      .sort(
        (a, b) =>
          new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime(),
      )
      .slice(0, 6);
  }, [notes]);

  // Merge curated pills with categories that came from the API.
  const pills = React.useMemo(() => {
    const map = new Map<string, { name: string; slug: string }>();
    for (const p of DEFAULT_CATEGORY_PILLS) map.set(p.slug, p);
    for (const c of categories) {
      if (!c.parentId) map.set(c.slug, { name: c.name, slug: c.slug });
    }
    return Array.from(map.values()).slice(0, 8);
  }, [categories]);

  return (
    <div className="flex flex-col">
      {/* Hero */}
      <section className="relative overflow-hidden border-b border-border/60">
        <div className="absolute inset-0 -z-10 bg-gradient-to-b from-emerald-50 via-background to-background dark:from-emerald-950/20" />
        <div
          aria-hidden
          className="absolute inset-0 -z-10 opacity-[0.04] dark:opacity-[0.07]"
          style={{
            backgroundImage:
              "radial-gradient(circle at 1px 1px, currentColor 1px, transparent 0)",
            backgroundSize: "32px 32px",
          }}
        />
        <div className="mx-auto max-w-7xl px-4 py-16 sm:px-6 sm:py-20 lg:px-8 lg:py-24">
          <div className="mx-auto max-w-3xl text-center">
            <Badge
              variant="outline"
              className="mb-4 gap-1.5 border-emerald-500/30 bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300"
            >
              <Sparkles className="size-3" />
              Self-hosted knowledge base
            </Badge>
            <h1 className="text-balance text-4xl font-bold tracking-tight sm:text-5xl">
              Technical Notes &{" "}
              <span className="accent-text">Knowledge</span>
            </h1>
            <p className="mx-auto mt-4 max-w-2xl text-pretty text-base text-muted-foreground sm:text-lg">
              A curated, searchable archive of cybersecurity, development,
              DevOps, cloud, and networking notes — written by engineers, for
              engineers.
            </p>

            <form
              onSubmit={onSubmit}
              className="mx-auto mt-8 flex w-full max-w-xl items-center gap-2"
            >
              <div className="relative flex-1">
                <Search className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
                <Input
                  value={heroSearch}
                  onChange={(e) => setHeroSearch(e.target.value)}
                  placeholder="Search for hardening guides, container patterns, packet captures…"
                  className="h-11 pl-9"
                  aria-label="Search the knowledge base"
                />
              </div>
              <Button
                type="submit"
                size="lg"
                className="h-11 bg-emerald-600 text-white hover:bg-emerald-700 dark:bg-emerald-500 dark:hover:bg-emerald-600"
              >
                Search
                <ArrowRight className="size-4" />
              </Button>
            </form>

            <div className="mt-3 flex flex-wrap items-center justify-center gap-1.5 text-xs text-muted-foreground">
              <span>Popular:</span>
              {["SELinux", "Next.js", "Kubernetes", "AWS S3", "TCP"].map(
                (term) => (
                  <button
                    key={term}
                    onClick={() => {
                      setHeroSearch(term);
                      setSearchQuery(term);
                      runSearch(term);
                    }}
                    className="rounded-full border border-border/60 bg-background px-2 py-0.5 transition-colors hover:border-emerald-500/40 hover:text-emerald-700 dark:hover:text-emerald-300"
                  >
                    {term}
                  </button>
                ),
              )}
            </div>
          </div>
        </div>
      </section>

      {/* Categories */}
      <section className="mx-auto w-full max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
        <div className="mb-5 flex flex-wrap items-end justify-between gap-2">
          <div>
            <h2 className="flex items-center gap-2 text-lg font-semibold">
              <FolderTree className="size-4 text-emerald-600 dark:text-emerald-400" />
              Browse by category
            </h2>
            <p className="text-sm text-muted-foreground">
              Jump straight to the area you care about.
            </p>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4">
          {pills.map((pill) => {
            const Icon = PILL_ICONS[pill.slug] ?? BookOpen;
            const count =
              categories.find((c) => c.slug === pill.slug)?.noteCount ?? null;
            return (
              <button
                key={pill.slug}
                onClick={() => {
                  setSearchQuery(pill.name);
                  runSearch(pill.name);
                }}
                className={cn(
                  "group flex items-center gap-3 rounded-xl border border-border/60 bg-card p-4 text-left transition-all hover:-translate-y-0.5 hover:border-emerald-500/40 hover:shadow-sm",
                )}
              >
                <span className="flex size-10 items-center justify-center rounded-lg bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300">
                  <Icon className="size-5" />
                </span>
                <span className="flex flex-col">
                  <span className="text-sm font-medium">{pill.name}</span>
                  <span className="text-xs text-muted-foreground">
                    {count !== null ? `${count} notes` : "Browse notes"}
                  </span>
                </span>
              </button>
            );
          })}
        </div>
      </section>

      {/* Latest notes */}
      <section className="mx-auto w-full max-w-7xl px-4 pb-12 sm:px-6 lg:px-8">
        <div className="mb-5 flex flex-wrap items-end justify-between gap-2">
          <div>
            <h2 className="text-lg font-semibold">Latest notes</h2>
            <p className="text-sm text-muted-foreground">
              Recently updated across every category.
            </p>
          </div>
          <Button
            variant="outline"
            size="sm"
            onClick={() => runSearch("")}
            className="gap-1"
          >
            See all
            <ArrowRight className="size-3.5" />
          </Button>
        </div>

        {dataLoading ? (
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {Array.from({ length: 6 }).map((_, i) => (
              <NoteCardSkeleton key={i} />
            ))}
          </div>
        ) : latestNotes.length === 0 ? (
          <EmptyState />
        ) : (
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {latestNotes.map((note) => (
              <NoteCard
                key={note.id}
                note={note}
                onOpen={(n: Note) => openNote(n)}
              />
            ))}
          </div>
        )}
      </section>

      {/* Feature strip */}
      <section className="border-t border-border/60 bg-muted/30">
        <div className="mx-auto grid max-w-7xl grid-cols-1 gap-4 px-4 py-10 sm:grid-cols-3 sm:px-6 lg:px-8">
          {[
            {
              icon: ShieldCheck,
              title: "Security first",
              body: "Notes are served from your own infrastructure. No third-party trackers, no analytics.",
            },
            {
              icon: Code2,
              title: "Author-friendly",
              body: "Upload raw HTML or zipped bundles with assets. Metadata is added in a single form.",
            },
            {
              icon: Search,
              title: "Built to search",
              body: "Full-text search across titles, descriptions, and tags with category filters.",
            },
          ].map((f) => (
            <Card key={f.title} className="bg-card">
              <CardContent className="flex flex-col gap-2 p-5">
                <span className="flex size-9 items-center justify-center rounded-lg bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300">
                  <f.icon className="size-5" />
                </span>
                <h3 className="text-sm font-semibold">{f.title}</h3>
                <p className="text-sm text-muted-foreground">{f.body}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>
    </div>
  );
}

function EmptyState() {
  const runSearch = useAppStore((s) => s.runSearch);
  return (
    <Card className="border-dashed">
      <CardContent className="flex flex-col items-center justify-center gap-3 p-12 text-center">
        <span className="flex size-12 items-center justify-center rounded-full bg-muted text-muted-foreground">
          <BookOpen className="size-6" />
        </span>
        <div>
          <p className="text-sm font-medium">No notes published yet</p>
          <p className="text-xs text-muted-foreground">
            Once an admin uploads notes, they will appear here.
          </p>
        </div>
        <Button
          variant="outline"
          size="sm"
          onClick={() => runSearch("")}
          className="gap-1"
        >
          Refresh
        </Button>
      </CardContent>
    </Card>
  );
}
