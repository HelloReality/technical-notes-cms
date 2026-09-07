"use client";

import * as React from "react";
import { History, Loader2, RotateCcw } from "lucide-react";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import { Skeleton } from "@/components/ui/skeleton";
import { StatusBadge } from "@/components/status-badge";
import { useAppStore } from "@/lib/store";
import type { Note, NoteVersion } from "@/lib/types";
import { formatDateTime, fromNow } from "@/lib/format";

interface VersionHistoryDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  note: Note | null;
}

export function VersionHistoryDialog({
  open,
  onOpenChange,
  note,
}: VersionHistoryDialogProps) {
  const versions = useAppStore((s) => s.noteVersions);
  const versionsLoading = useAppStore((s) => s.versionsLoading);
  const loadNoteVersions = useAppStore((s) => s.loadNoteVersions);
  const restoreVersion = useAppStore((s) => s.restoreVersion);

  const [restoreTarget, setRestoreTarget] =
    React.useState<NoteVersion | null>(null);
  const [busy, setBusy] = React.useState(false);

  const noteId = note?.id;

  // Load versions when the dialog opens for a note.
  React.useEffect(() => {
    if (open && noteId) {
      void loadNoteVersions(noteId).catch(() => {
        /* swallow — store already clears versionsLoading */
      });
    }
  }, [open, noteId, loadNoteVersions]);

  const handleRestore = React.useCallback(async () => {
    if (!note || !restoreTarget) return;
    setBusy(true);
    try {
      await restoreVersion(note.id, restoreTarget.id);
      toast.success("Note restored", {
        description: `Restored to version from ${formatDateTime(
          restoreTarget.createdAt,
        )}`,
      });
      setRestoreTarget(null);
      onOpenChange(false);
    } catch (err) {
      toast.error("Restore failed", {
        description: err instanceof Error ? err.message : "Try again later.",
      });
    } finally {
      setBusy(false);
    }
  }, [note, restoreTarget, restoreVersion, onOpenChange]);

  return (
    <>
      <Dialog open={open} onOpenChange={onOpenChange}>
        <DialogContent className="sm:max-w-xl">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <History className="size-4 text-emerald-600 dark:text-emerald-400" />
              Version history
            </DialogTitle>
            <DialogDescription>
              {note ? (
                <>
                  Snapshots saved before each edit of{" "}
                  <strong className="text-foreground">{note.title}</strong>. You
                  can restore any earlier version.
                </>
              ) : (
                "Snapshots saved before each edit. You can restore any earlier version."
              )}
            </DialogDescription>
          </DialogHeader>

          <div className="scroll-thin max-h-80 overflow-y-auto">
            {versionsLoading ? (
              <div className="flex flex-col gap-2 px-1">
                {Array.from({ length: 4 }).map((_, i) => (
                  <Skeleton key={i} className="h-16 w-full" />
                ))}
              </div>
            ) : versions.length === 0 ? (
              <div className="flex flex-col items-center justify-center gap-2 px-6 py-10 text-center">
                <History className="size-6 text-muted-foreground" />
                <p className="text-sm font-medium">No saved versions</p>
                <p className="text-xs text-muted-foreground">
                  Versions are captured automatically before each edit.
                </p>
              </div>
            ) : (
              <ol className="flex flex-col gap-2 px-1">
                {versions.map((v, idx) => (
                  <li
                    key={v.id}
                    className="flex flex-col gap-2 rounded-lg border border-border/60 bg-card p-3 sm:flex-row sm:items-center sm:justify-between"
                  >
                    <div className="flex min-w-0 flex-col gap-1">
                      <div className="flex flex-wrap items-center gap-2">
                        <span className="text-sm font-medium">
                          {v.title || "Untitled"}
                        </span>
                        <StatusBadge status={v.status} />
                        {idx === 0 && (
                          <span className="rounded-full bg-emerald-100 px-2 py-0.5 text-[10px] font-medium uppercase tracking-wide text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-300">
                            Latest
                          </span>
                        )}
                      </div>
                      <div className="flex flex-wrap items-center gap-x-2 gap-y-0.5 text-xs text-muted-foreground">
                        <span>
                          {v.createdByName ?? "Unknown editor"}
                        </span>
                        <span aria-hidden>·</span>
                        <span title={formatDateTime(v.createdAt)}>
                          {fromNow(v.createdAt)}
                        </span>
                      </div>
                    </div>
                    <Button
                      type="button"
                      size="sm"
                      variant="outline"
                      className="gap-1.5 sm:shrink-0"
                      disabled={busy || idx === 0}
                      onClick={() => setRestoreTarget(v)}
                      title={
                        idx === 0
                          ? "This is already the latest version"
                          : "Restore this version"
                      }
                    >
                      <RotateCcw className="size-3.5" />
                      Restore
                    </Button>
                  </li>
                ))}
              </ol>
            )}
          </div>

          <DialogFooter>
            <Button
              type="button"
              variant="ghost"
              disabled={busy}
              onClick={() => onOpenChange(false)}
            >
              Close
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      <AlertDialog
        open={!!restoreTarget}
        onOpenChange={(o) => !o && setRestoreTarget(null)}
      >
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Restore this version?</AlertDialogTitle>
            <AlertDialogDescription>
              <span className="block">
                The note will be reverted to the version saved{" "}
                <strong>
                  {restoreTarget ? formatDateTime(restoreTarget.createdAt) : ""}
                </strong>
                .
              </span>
              <span className="mt-1 block">
                The current state will be saved as a new version first, so you
                can undo this restore later.
              </span>
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel disabled={busy}>Cancel</AlertDialogCancel>
            <AlertDialogAction
              disabled={busy}
              onClick={(e) => {
                e.preventDefault();
                void handleRestore();
              }}
              className="bg-emerald-600 text-white hover:bg-emerald-700 dark:bg-emerald-500 dark:hover:bg-emerald-600"
            >
              {busy ? <Loader2 className="mr-2 size-4 animate-spin" /> : null}
              Restore version
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </>
  );
}
