"use client";

import * as React from "react";
import { CalendarClock, Loader2, XCircle } from "lucide-react";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
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
import { StatusBadge } from "@/components/status-badge";
import { useAppStore } from "@/lib/store";
import type { Note, ScheduledPublish } from "@/lib/types";
import { cn } from "@/lib/utils";
import { formatDateTime, fromNow } from "@/lib/format";

interface SchedulePublishDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  note: Note | null;
  /** Pending schedules from the store — used to detect an existing schedule. */
  pendingSchedules: ScheduledPublish[];
}

/** Convert a Date to the value expected by <input type="datetime-local">. */
function toDateTimeLocalValue(d: Date): string {
  // Build YYYY-MM-DDTHH:mm in the user's local timezone.
  const pad = (n: number) => String(n).padStart(2, "0");
  return (
    `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}` +
    `T${pad(d.getHours())}:${pad(d.getMinutes())}`
  );
}

const QUICK_PRESETS: { label: string; get: () => Date }[] = [
  {
    label: "in 1 hour",
    get: () => new Date(Date.now() + 60 * 60 * 1000),
  },
  {
    label: "tomorrow at 9 AM",
    get: () => {
      const d = new Date();
      d.setDate(d.getDate() + 1);
      d.setHours(9, 0, 0, 0);
      return d;
    },
  },
  {
    label: "in 1 week",
    get: () => new Date(Date.now() + 7 * 24 * 60 * 60 * 1000),
  },
];

export function SchedulePublishDialog({
  open,
  onOpenChange,
  note,
  pendingSchedules,
}: SchedulePublishDialogProps) {
  const schedulePublish = useAppStore((s) => s.schedulePublish);
  const cancelSchedule = useAppStore((s) => s.cancelSchedule);

  // Default to "tomorrow 9am" the first time the dialog opens for a note.
  const [value, setValue] = React.useState<string>("");
  const [busy, setBusy] = React.useState(false);
  const [confirmCancel, setConfirmCancel] = React.useState(false);
  const noteId = note?.id;
  const existing = React.useMemo(
    () =>
      noteId
        ? pendingSchedules.find((s) => s.noteId === noteId && s.status === "PENDING")
        : undefined,
    [pendingSchedules, noteId],
  );

  // (Re)initialise the input value when opening for a new note.
  React.useEffect(() => {
    if (open && noteId) {
      setValue(
        existing
          ? toDateTimeLocalValue(new Date(existing.publishAt))
          : toDateTimeLocalValue(QUICK_PRESETS[1].get()),
      );
    }
  }, [open, noteId, existing]);

  const parsedDate = React.useMemo(() => {
    if (!value) return null;
    const d = new Date(value);
    return Number.isNaN(d.getTime()) ? null : d;
  }, [value]);

  const handleSchedule = React.useCallback(async () => {
    if (!note || !parsedDate) return;
    setBusy(true);
    try {
      await schedulePublish(note.id, parsedDate);
      toast.success("Publish scheduled", {
        description: `${note.title} — ${formatDateTime(parsedDate.toISOString())}`,
      });
      onOpenChange(false);
    } catch (err) {
      toast.error("Failed to schedule publish", {
        description: err instanceof Error ? err.message : "Try again later.",
      });
    } finally {
      setBusy(false);
    }
  }, [note, parsedDate, schedulePublish, onOpenChange]);

  const handleCancel = React.useCallback(async () => {
    if (!note) return;
    setBusy(true);
    try {
      await cancelSchedule(note.id);
      toast.success("Scheduled publish cancelled", {
        description: note.title,
      });
      onOpenChange(false);
    } catch (err) {
      toast.error("Failed to cancel schedule", {
        description: err instanceof Error ? err.message : "Try again later.",
      });
    } finally {
      setBusy(false);
    }
  }, [note, cancelSchedule, onOpenChange]);

  return (
    <>
      <Dialog open={open} onOpenChange={onOpenChange}>
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <CalendarClock className="size-4 text-emerald-600 dark:text-emerald-400" />
              Schedule publish
            </DialogTitle>
            <DialogDescription>
              {note ? (
                <>
                  Choose when{" "}
                  <strong className="text-foreground">{note.title}</strong> will
                  be automatically published.
                </>
              ) : (
                "Choose when this note will be automatically published."
              )}
            </DialogDescription>
          </DialogHeader>

          {existing && (
            <div className="flex items-center justify-between gap-2 rounded-lg border border-emerald-200 bg-emerald-50 p-3 text-xs dark:border-emerald-900/60 dark:bg-emerald-950/40">
              <div className="min-w-0 flex-col gap-0.5">
                <span className="font-medium text-emerald-800 dark:text-emerald-200">
                  Already scheduled
                </span>
                <span className="block text-emerald-700/80 dark:text-emerald-300/80">
                  {formatDateTime(existing.publishAt)} ({fromNow(existing.publishAt)})
                </span>
              </div>
              <StatusBadge status={note?.status ?? "DRAFT"} />
            </div>
          )}

          <div className="flex flex-col gap-2">
            <label htmlFor="schedule-dt" className="text-sm font-medium">
              Publish at
            </label>
            <Input
              id="schedule-dt"
              type="datetime-local"
              value={value}
              onChange={(e) => setValue(e.target.value)}
              disabled={busy}
            />
            <div className="flex flex-wrap gap-1.5">
              {QUICK_PRESETS.map((p) => (
                <Button
                  key={p.label}
                  type="button"
                  size="sm"
                  variant="outline"
                  className="h-7 px-2 text-xs"
                  disabled={busy}
                  onClick={() => setValue(toDateTimeLocalValue(p.get()))}
                >
                  {p.label}
                </Button>
              ))}
            </div>
            {parsedDate && parsedDate.getTime() < Date.now() && (
              <p className="text-xs text-amber-700 dark:text-amber-300">
                That time is in the past — pick a future time.
              </p>
            )}
          </div>

          <DialogFooter className="flex-row items-center justify-between gap-2 sm:justify-between">
            {existing ? (
              <Button
                type="button"
                variant="outline"
                className={cn(
                  "gap-1.5 border-destructive/40 text-destructive hover:bg-destructive/10 hover:text-destructive",
                )}
                disabled={busy}
                onClick={() => setConfirmCancel(true)}
              >
                <XCircle className="size-3.5" />
                Cancel schedule
              </Button>
            ) : (
              <span className="text-xs text-muted-foreground" />
            )}
            <div className="flex items-center gap-2">
              <Button
                type="button"
                variant="ghost"
                disabled={busy}
                onClick={() => onOpenChange(false)}
              >
                Close
              </Button>
              <Button
                type="button"
                className="gap-1.5 bg-emerald-600 text-white hover:bg-emerald-700 dark:bg-emerald-500 dark:hover:bg-emerald-600"
                disabled={busy || !parsedDate || parsedDate.getTime() < Date.now()}
                onClick={handleSchedule}
              >
                {busy ? (
                  <Loader2 className="size-3.5 animate-spin" />
                ) : (
                  <CalendarClock className="size-3.5" />
                )}
                {existing ? "Update schedule" : "Schedule"}
              </Button>
            </div>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      <AlertDialog
        open={confirmCancel}
        onOpenChange={(o) => !o && setConfirmCancel(false)}
      >
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Cancel scheduled publish?</AlertDialogTitle>
            <AlertDialogDescription>
              <span className="block">
                This will cancel the pending publish for{" "}
                <strong>{note?.title}</strong>.
              </span>
              <span className="mt-1 block">
                You can re-schedule it at any time.
              </span>
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel disabled={busy}>Keep schedule</AlertDialogCancel>
            <AlertDialogAction
              disabled={busy}
              onClick={(e) => {
                e.preventDefault();
                void handleCancel().then(() => setConfirmCancel(false));
              }}
              className="bg-destructive text-white hover:bg-destructive/90 dark:bg-destructive/60"
            >
              {busy ? <Loader2 className="mr-2 size-4 animate-spin" /> : null}
              Cancel schedule
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </>
  );
}
