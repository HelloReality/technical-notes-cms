"use client";

import * as React from "react";
import { CheckCircle2, Loader2, Trash2, X, XCircle } from "lucide-react";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
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
import { useAppStore } from "@/lib/store";
import type { BulkAction } from "@/lib/types";

interface BulkActionBarProps {
  /** Currently selected note IDs. */
  selectedIds: string[];
  /** Clears the current selection. */
  onClear: () => void;
}

const ACTION_LABEL: Record<BulkAction, { verb: string; noun: string }> = {
  PUBLISH: { verb: "Published", noun: "notes" },
  UNPUBLISH: { verb: "Unpublished", noun: "notes" },
  DELETE: { verb: "Deleted", noun: "notes" },
};

/**
 * Floating toolbar shown above the notes table when 1+ notes are selected.
 * Offers Publish / Unpublish / Delete (with confirmation) and a Clear-selection
 * button. After each action the selection is cleared.
 */
export function BulkActionBar({ selectedIds, onClear }: BulkActionBarProps) {
  const bulkAction = useAppStore((s) => s.bulkAction);
  const [busy, setBusy] = React.useState<BulkAction | null>(null);
  const [confirmDelete, setConfirmDelete] = React.useState(false);

  const selectedCount = selectedIds.length;
  const idsRef = React.useRef<string[]>(selectedIds);
  React.useEffect(() => {
    idsRef.current = selectedIds;
  }, [selectedIds]);

  const run = React.useCallback(
    async (action: BulkAction) => {
      const ids = idsRef.current;
      if (ids.length === 0) return;
      setBusy(action);
      try {
        const result = await bulkAction(action, ids);
        const meta = ACTION_LABEL[action];
        toast.success(`${meta.verb} ${result.succeeded} ${meta.noun}`, {
          description:
            result.failed > 0
              ? `${result.failed} failed. ${result.errors[0] ?? ""}`.trim()
              : undefined,
        });
        onClear();
      } catch (err) {
        toast.error("Bulk action failed", {
          description: err instanceof Error ? err.message : "Try again later.",
        });
      } finally {
        setBusy(null);
      }
    },
    [bulkAction, onClear],
  );

  if (selectedCount === 0) return null;

  return (
    <>
      <div className="sticky top-0 z-20 -mt-px flex flex-wrap items-center gap-2 border-b border-border/60 bg-emerald-50/80 px-4 py-2 backdrop-blur dark:bg-emerald-950/30 sm:px-6">
        <span className="mr-2 inline-flex items-center gap-1.5 text-sm font-medium text-emerald-800 dark:text-emerald-200">
          <CheckCircle2 className="size-4" />
          {selectedCount} selected
        </span>
        <div className="flex flex-wrap items-center gap-2">
          <Button
            type="button"
            size="sm"
            className="gap-1.5 bg-emerald-600 text-white hover:bg-emerald-700 dark:bg-emerald-500 dark:hover:bg-emerald-600"
            disabled={busy !== null}
            onClick={() => run("PUBLISH")}
          >
            {busy === "PUBLISH" ? (
              <Loader2 className="size-3.5 animate-spin" />
            ) : (
              <CheckCircle2 className="size-3.5" />
            )}
            Publish
          </Button>
          <Button
            type="button"
            size="sm"
            variant="outline"
            className="gap-1.5"
            disabled={busy !== null}
            onClick={() => run("UNPUBLISH")}
          >
            {busy === "UNPUBLISH" ? (
              <Loader2 className="size-3.5 animate-spin" />
            ) : (
              <XCircle className="size-3.5" />
            )}
            Unpublish
          </Button>
          <Button
            type="button"
            size="sm"
            variant="outline"
            className="gap-1.5 border-destructive/40 text-destructive hover:bg-destructive/10 hover:text-destructive"
            disabled={busy !== null}
            onClick={() => setConfirmDelete(true)}
          >
            {busy === "DELETE" ? (
              <Loader2 className="size-3.5 animate-spin" />
            ) : (
              <Trash2 className="size-3.5" />
            )}
            Delete
          </Button>
          <Button
            type="button"
            size="sm"
            variant="ghost"
            className="gap-1.5"
            disabled={busy !== null}
            onClick={onClear}
          >
            <X className="size-3.5" />
            Clear
          </Button>
        </div>
      </div>

      <AlertDialog
        open={confirmDelete}
        onOpenChange={(o) => !o && setConfirmDelete(false)}
      >
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Delete {selectedCount} notes?</AlertDialogTitle>
            <AlertDialogDescription>
              <span className="block">
                You are about to permanently delete{" "}
                <strong>{selectedCount}</strong>{" "}
                {selectedCount === 1 ? "note" : "notes"}.
              </span>
              <span className="mt-1 block">
                This action cannot be undone.
              </span>
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel disabled={busy !== null}>Cancel</AlertDialogCancel>
            <AlertDialogAction
              disabled={busy !== null}
              onClick={(e) => {
                e.preventDefault();
                void run("DELETE").then(() => setConfirmDelete(false));
              }}
              className="bg-destructive text-white hover:bg-destructive/90 dark:bg-destructive/60"
            >
              {busy === "DELETE" ? (
                <Loader2 className="mr-2 size-4 animate-spin" />
              ) : null}
              Delete
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </>
  );
}
