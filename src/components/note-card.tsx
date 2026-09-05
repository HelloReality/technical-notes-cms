"use client";

import { ArrowUpRight, Calendar, FolderTree, Tag } from "lucide-react";

import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import type { Category, Note } from "@/lib/types";
import { formatDate } from "@/lib/format";
import { cn } from "@/lib/utils";

interface NoteCardProps {
  note: Note;
  category?: Category | null;
  className?: string;
  onOpen?: (note: Note) => void;
}

export function NoteCard({ note, category, className, onOpen }: NoteCardProps) {
  const cat = category ?? note.category ?? null;
  const subcategory =
    note.subcategory ?? (cat?.parentId ? cat : null) ?? null;
  const topCategory = cat?.parentId ? null : cat;

  return (
    <Card
      className={cn(
        "group relative gap-0 overflow-hidden py-0 transition-all hover:-translate-y-0.5 hover:border-emerald-500/40 hover:shadow-md",
        className,
      )}
    >
      <div className="h-1 w-full bg-gradient-to-r from-emerald-500 to-teal-400" />
      <CardContent className="flex flex-col gap-3 p-5">
        <div className="flex flex-wrap items-center gap-2 text-xs text-muted-foreground">
          {topCategory && (
            <Badge
              variant="outline"
              className="border-emerald-500/30 bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300"
            >
              <FolderTree className="size-3" />
              {topCategory.name}
            </Badge>
          )}
          {subcategory && subcategory.id !== topCategory?.id && (
            <Badge variant="secondary" className="font-normal">
              {subcategory.name}
            </Badge>
          )}
        </div>

        <button
          onClick={() => onOpen?.(note)}
          className="text-left text-base font-semibold leading-snug tracking-tight group-hover:text-emerald-700 dark:group-hover:text-emerald-300"
        >
          {note.title}
        </button>

        <p className="line-clamp-3 text-sm text-muted-foreground">
          {note.description ?? "No description provided."}
        </p>

        {note.tags && note.tags.length > 0 && (
          <div className="flex flex-wrap gap-1.5">
            {note.tags.slice(0, 3).map((tag) => (
              <Badge
                key={tag.id}
                variant="outline"
                className="gap-1 font-normal text-muted-foreground"
              >
                <Tag className="size-2.5" />
                {tag.name}
              </Badge>
            ))}
            {note.tags.length > 3 && (
              <span className="text-xs text-muted-foreground">
                +{note.tags.length - 3} more
              </span>
            )}
          </div>
        )}

        <div className="mt-2 flex items-center justify-between border-t border-border/60 pt-3">
          <div className="flex items-center gap-1.5 text-xs text-muted-foreground">
            <Calendar className="size-3.5" />
            {formatDate(note.updatedAt)}
          </div>
          <Button
            size="sm"
            variant="ghost"
            className="gap-1 px-2 text-emerald-700 hover:bg-emerald-50 hover:text-emerald-700 dark:text-emerald-300 dark:hover:bg-emerald-950/40"
            onClick={() => onOpen?.(note)}
          >
            Read
            <ArrowUpRight className="size-3.5" />
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}

export function NoteCardSkeleton() {
  return (
    <Card className="overflow-hidden py-0">
      <div className="h-1 w-full bg-muted" />
      <CardContent className="flex flex-col gap-3 p-5">
        <div className="h-5 w-24 animate-pulse rounded bg-muted" />
        <div className="h-5 w-3/4 animate-pulse rounded bg-muted" />
        <div className="h-4 w-full animate-pulse rounded bg-muted" />
        <div className="h-4 w-5/6 animate-pulse rounded bg-muted" />
        <div className="mt-2 flex justify-between border-t border-border/60 pt-3">
          <div className="h-4 w-24 animate-pulse rounded bg-muted" />
          <div className="h-7 w-16 animate-pulse rounded bg-muted" />
        </div>
      </CardContent>
    </Card>
  );
}
