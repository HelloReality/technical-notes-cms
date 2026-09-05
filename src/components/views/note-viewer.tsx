"use client";

import * as React from "react";
import {
  ArrowLeft,
  Calendar,
  Clock,
  ExternalLink,
  Home,
  Tag,
} from "lucide-react";

import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  NoteCard,
} from "@/components/note-card";
import { useAppStore } from "@/lib/store";
import { formatDateTime, fromNow } from "@/lib/format";

export function NoteViewer() {
  const note = useAppStore((s) => s.selectedNote);
  const loading = useAppStore((s) => s.noteLoading);
  const allNotes = useAppStore((s) => s.notes);
  const openNote = useAppStore((s) => s.openNote);
  const goHome = useAppStore((s) => s.goHome);

  const relatedNotes = React.useMemo(() => {
    if (!note) return [];
    return allNotes
      .filter(
        (n) =>
          n.id !== note.id &&
          (n.categoryId === note.categoryId ||
            n.tags?.some((t) =>
              note.tags?.some((nt) => nt.id === t.id || nt.name === t.name),
            )),
      )
      .slice(0, 3);
  }, [allNotes, note]);

  const category = note?.category;
  const subcategory = note?.subcategory ?? (category?.parentId ? category : null);
  const topCategory =
    category && category.parentId ? null : category;

  return (
    <div className="mx-auto w-full max-w-5xl px-4 py-6 sm:px-6 lg:px-8">
      <div className="mb-4 flex items-center justify-between gap-3">
        <Button
          variant="ghost"
          size="sm"
          onClick={goHome}
          className="gap-1 text-muted-foreground"
        >
          <ArrowLeft className="size-4" />
          Back
        </Button>
        <Button variant="ghost" size="sm" asChild>
          <a
            href={note?.contentPath}
            target="_blank"
            rel="noopener noreferrer"
            className="gap-1 text-muted-foreground"
          >
            Open raw
            <ExternalLink className="size-3.5" />
          </a>
        </Button>
      </div>

      {/* Breadcrumb */}
      <Breadcrumb className="mb-4">
        <BreadcrumbList>
          <BreadcrumbItem>
            <BreadcrumbLink asChild>
              <button onClick={goHome} className="flex items-center gap-1">
                <Home className="size-3" />
                Home
              </button>
            </BreadcrumbLink>
          </BreadcrumbItem>
          {topCategory && (
            <>
              <BreadcrumbSeparator />
              <BreadcrumbItem>
                <BreadcrumbLink asChild>
                  <button onClick={goHome}>{topCategory.name}</button>
                </BreadcrumbLink>
              </BreadcrumbItem>
            </>
          )}
          {subcategory && subcategory.id !== topCategory?.id && (
            <>
              <BreadcrumbSeparator />
              <BreadcrumbItem>
                <BreadcrumbLink asChild>
                  <button onClick={goHome}>{subcategory.name}</button>
                </BreadcrumbLink>
              </BreadcrumbItem>
            </>
          )}
          <BreadcrumbSeparator />
          <BreadcrumbItem>
            <BreadcrumbPage className="line-clamp-1 max-w-[60ch]">
              {note?.title ?? "Note"}
            </BreadcrumbPage>
          </BreadcrumbItem>
        </BreadcrumbList>
      </Breadcrumb>

      {loading || !note ? (
        <ViewerSkeleton />
      ) : (
        <>
          <header className="mb-6 border-b border-border/60 pb-5">
            <div className="mb-2 flex flex-wrap items-center gap-2 text-xs text-muted-foreground">
              {topCategory && (
                <Badge
                  variant="outline"
                  className="border-emerald-500/30 bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300"
                >
                  {topCategory.name}
                </Badge>
              )}
              {subcategory && subcategory.id !== topCategory?.id && (
                <Badge variant="secondary">{subcategory.name}</Badge>
              )}
            </div>
            <h1 className="text-balance text-3xl font-bold tracking-tight sm:text-4xl">
              {note.title}
            </h1>
            {note.description && (
              <p className="mt-2 text-pretty text-muted-foreground">
                {note.description}
              </p>
            )}

            <div className="mt-4 flex flex-wrap items-center gap-x-5 gap-y-2 text-xs text-muted-foreground">
              <span className="flex items-center gap-1.5">
                <Clock className="size-3.5" />
                Updated {fromNow(note.updatedAt)}
              </span>
              <span className="flex items-center gap-1.5">
                <Calendar className="size-3.5" />
                {formatDateTime(note.updatedAt)}
              </span>
              {note.tags && note.tags.length > 0 && (
                <span className="flex flex-wrap items-center gap-1.5">
                  <Tag className="size-3.5" />
                  {note.tags.map((t) => (
                    <Badge
                      key={t.id}
                      variant="outline"
                      className="font-normal"
                    >
                      {t.name}
                    </Badge>
                  ))}
                </span>
              )}
            </div>
          </header>

          <div className="overflow-x-auto overflow-y-hidden rounded-xl border border-border/60 bg-white shadow-sm dark:bg-white">
            <iframe
              title={note.title}
              className="note-iframe min-h-[60vh]"
              src={note.contentPath}
              sandbox="allow-same-origin allow-popups"
              onLoad={(e) => {
                // Since we have allow-same-origin, we can access the iframe's
                // document to inject padding so the spiral binding ring
                // (which extends -30px outside the page) is not clipped.
                try {
                  const iframe = e.target as HTMLIFrameElement;
                  const doc = iframe.contentDocument;
                  if (!doc) return;
                  const style = doc.createElement("style");
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
                  // Auto-resize iframe height to fit content
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
              }}
            />
          </div>

          {/* Related notes */}
          {relatedNotes.length > 0 && (
            <section className="mt-10">
              <Card>
                <CardHeader>
                  <CardTitle className="text-base">Related notes</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
                    {relatedNotes.map((rel) => (
                      <NoteCard
                        key={rel.id}
                        note={rel}
                        onOpen={(n) => openNote(n)}
                      />
                    ))}
                  </div>
                </CardContent>
              </Card>
            </section>
          )}
        </>
      )}
    </div>
  );
}

function ViewerSkeleton() {
  return (
    <div className="flex flex-col gap-4">
      <div className="flex gap-2">
        <Skeleton className="h-5 w-24" />
        <Skeleton className="h-5 w-32" />
      </div>
      <Skeleton className="h-10 w-3/4" />
      <Skeleton className="h-4 w-full" />
      <Skeleton className="h-4 w-5/6" />
      <div className="flex gap-4">
        <Skeleton className="h-3 w-32" />
        <Skeleton className="h-3 w-40" />
      </div>
      <Skeleton className="h-[60vh] w-full rounded-xl" />
    </div>
  );
}
