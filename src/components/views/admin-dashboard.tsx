"use client";

import * as React from "react";
import {
  BookOpen,
  CalendarClock,
  Eye,
  FileEdit,
  FilePlus2,
  FolderTree,
  History,
  LayoutDashboard,
  Loader2,
  MoreHorizontal,
  Search,
  Settings,
  ShieldCheck,
  Tag,
  Trash2,
  Upload,
  XCircle,
} from "lucide-react";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Checkbox } from "@/components/ui/checkbox";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Skeleton } from "@/components/ui/skeleton";
import { Badge } from "@/components/ui/badge";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
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
import { BulkActionBar } from "@/components/admin/bulk-action-bar";
import { SchedulePublishDialog } from "@/components/admin/schedule-publish-dialog";
import { VersionHistoryDialog } from "@/components/admin/version-history-dialog";
import { useAppStore } from "@/lib/store";
import type { Note, NoteStatus, ScheduledPublish } from "@/lib/types";
import { formatDateTime, fromNow } from "@/lib/format";
import { cn } from "@/lib/utils";

type SidebarKey = "dashboard" | "notes" | "categories" | "tags" | "settings";

const SIDEBAR_ITEMS: {
  key: SidebarKey;
  label: string;
  icon: React.ElementType;
}[] = [
  { key: "dashboard", label: "Dashboard", icon: LayoutDashboard },
  { key: "notes", label: "Notes", icon: BookOpen },
  { key: "categories", label: "Categories", icon: FolderTree },
  { key: "tags", label: "Tags", icon: Tag },
  { key: "settings", label: "Settings", icon: Settings },
];

export function AdminDashboard() {
  const notes = useAppStore((s) => s.notes);
  const dataLoading = useAppStore((s) => s.dataLoading);
  const categories = useAppStore((s) => s.categories);
  const openUploadModal = useAppStore((s) => s.openUploadModal);
  const openNote = useAppStore((s) => s.openNote);
  const publishNote = useAppStore((s) => s.publishNote);
  const unpublishNote = useAppStore((s) => s.unpublishNote);
  const deleteNote = useAppStore((s) => s.deleteNote);
  const pendingSchedules = useAppStore((s) => s.pendingSchedules);
  const loadPendingSchedules = useAppStore((s) => s.loadPendingSchedules);

  const [section, setSection] = React.useState<SidebarKey>("dashboard");
  const [search, setSearch] = React.useState("");
  const [statusFilter, setStatusFilter] = React.useState<NoteStatus | "ALL">(
    "ALL",
  );
  const [deleteTarget, setDeleteTarget] = React.useState<Note | null>(null);
  const [busyId, setBusyId] = React.useState<string | null>(null);

  // Bulk selection state (lifted into AdminDashboard so the bulk action bar
  // and the table share the same source of truth).
  const [selectedIds, setSelectedIds] = React.useState<Set<string>>(
    () => new Set(),
  );
  const toggleSelect = React.useCallback((id: string) => {
    setSelectedIds((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  }, []);
  const clearSelection = React.useCallback(() => setSelectedIds(new Set()), []);

  // Schedule-publish dialog state.
  const [scheduleTarget, setScheduleTarget] = React.useState<Note | null>(
    null,
  );
  const [scheduleOpen, setScheduleOpen] = React.useState(false);

  // Version-history dialog state.
  const [versionTarget, setVersionTarget] = React.useState<Note | null>(null);
  const [versionOpen, setVersionOpen] = React.useState(false);

  // Load pending schedules once on mount so the UI knows which notes are
  // already scheduled.
  React.useEffect(() => {
    void loadPendingSchedules();
  }, [loadPendingSchedules]);

  // Auto-clear selection when the user switches away from the notes section
  // or changes the filter — selection should never silently persist across
  // different filtered views.
  React.useEffect(() => {
    clearSelection();
  }, [section, statusFilter, search, clearSelection]);

  const stats = React.useMemo(() => {
    const total = notes.length;
    const published = notes.filter((n) => n.status === "PUBLISHED").length;
    const draft = notes.filter((n) => n.status === "DRAFT").length;
    const unpublished = notes.filter((n) => n.status === "UNPUBLISHED").length;
    return { total, published, draft, unpublished };
  }, [notes]);

  const filteredNotes = React.useMemo(() => {
    return notes.filter((n) => {
      if (statusFilter !== "ALL" && n.status !== statusFilter) return false;
      if (search.trim()) {
        const q = search.toLowerCase();
        return (
          n.title.toLowerCase().includes(q) ||
          n.description?.toLowerCase().includes(q) ||
          n.tags?.some((t) => t.name.toLowerCase().includes(q))
        );
      }
      return true;
    });
  }, [notes, search, statusFilter]);

  const recentNotes = React.useMemo(
    () =>
      [...notes]
        .sort(
          (a, b) =>
            new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime(),
        )
        .slice(0, 6),
    [notes],
  );

  const handleTogglePublish = async (note: Note) => {
    setBusyId(note.id);
    try {
      if (note.status === "PUBLISHED") {
        await unpublishNote(note.id);
        toast.success("Note unpublished", { description: note.title });
      } else {
        await publishNote(note.id);
        toast.success("Note published", { description: note.title });
      }
    } catch (err) {
      toast.error("Action failed", {
        description: err instanceof Error ? err.message : "Try again later.",
      });
    } finally {
      setBusyId(null);
    }
  };

  const handleDelete = async () => {
    if (!deleteTarget) return;
    const target = deleteTarget;
    setBusyId(target.id);
    try {
      await deleteNote(target.id);
      toast.success("Note deleted", { description: target.title });
      setDeleteTarget(null);
      // Make sure the note is removed from the bulk selection.
      setSelectedIds((prev) => {
        if (!prev.has(target.id)) return prev;
        const next = new Set(prev);
        next.delete(target.id);
        return next;
      });
    } catch (err) {
      toast.error("Delete failed", {
        description: err instanceof Error ? err.message : "Try again later.",
      });
    } finally {
      setBusyId(null);
    }
  };

  const handleOpenSchedule = React.useCallback((note: Note) => {
    setScheduleTarget(note);
    setScheduleOpen(true);
  }, []);

  const handleOpenVersions = React.useCallback((note: Note) => {
    setVersionTarget(note);
    setVersionOpen(true);
  }, []);

  const topCategories = React.useMemo(() => {
    return categories
      .filter((c) => !c.parentId)
      .slice(0, 5)
      .map((c) => ({
        ...c,
        count:
          notes.filter(
            (n) =>
              n.categoryId === c.id ||
              n.category?.parentId === c.id ||
              c.children?.some((ch) => n.categoryId === ch.id),
          ).length ?? 0,
      }))
      .sort((a, b) => b.count - a.count);
  }, [categories, notes]);

  // Look up the note title for a pending schedule (defensive — schedule may
  // exist for a note that was deleted in another session).
  const scheduleWithNotes = React.useMemo(() => {
    return pendingSchedules
      .filter((s) => s.status === "PENDING")
      .map((s) => ({
        schedule: s,
        note: notes.find((n) => n.id === s.noteId) ?? null,
      }))
      .sort(
        (a, b) =>
          new Date(a.schedule.publishAt).getTime() -
          new Date(b.schedule.publishAt).getTime(),
      );
  }, [pendingSchedules, notes]);

  return (
    <div className="mx-auto flex w-full max-w-7xl flex-col gap-6 px-4 py-6 sm:px-6 lg:flex-row lg:px-8">
      {/* Sidebar */}
      <aside className="lg:w-60 lg:shrink-0">
        <div className="sticky top-20 flex flex-col gap-2">
          <div className="mb-2 flex items-center gap-2 px-2 lg:hidden">
            <Select
              value={section}
              onValueChange={(v) => setSection(v as SidebarKey)}
            >
              <SelectTrigger className="w-full">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {SIDEBAR_ITEMS.map((item) => (
                  <SelectItem key={item.key} value={item.key}>
                    {item.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <nav
            aria-label="Admin sections"
            className="hidden flex-col gap-1 lg:flex"
          >
            {SIDEBAR_ITEMS.map((item) => (
              <Button
                key={item.key}
                variant={section === item.key ? "secondary" : "ghost"}
                className="justify-start"
                onClick={() => setSection(item.key)}
              >
                <item.icon className="size-4" />
                {item.label}
              </Button>
            ))}
          </nav>

          <div className="mt-4 hidden rounded-xl border border-border/60 bg-card p-4 lg:block">
            <div className="flex items-center gap-2 text-sm font-medium">
              <ShieldCheck className="size-4 text-emerald-600 dark:text-emerald-400" />
              Admin Console
            </div>
            <p className="mt-1 text-xs text-muted-foreground">
              Manage notes, categories, and tags from this panel.
            </p>
            <Button
              className="mt-3 w-full gap-2 bg-emerald-600 text-white hover:bg-emerald-700 dark:bg-emerald-500 dark:hover:bg-emerald-600"
              size="sm"
              onClick={openUploadModal}
            >
              <Upload className="size-4" />
              Upload Note
            </Button>
          </div>
        </div>
      </aside>

      {/* Main panel */}
      <main className="flex min-w-0 flex-1 flex-col gap-6">
        <div className="flex flex-wrap items-end justify-between gap-3">
          <div>
            <h1 className="text-2xl font-semibold tracking-tight">
              {SIDEBAR_ITEMS.find((i) => i.key === section)?.label}
            </h1>
            <p className="text-sm text-muted-foreground">
              Manage your technical knowledge base.
            </p>
          </div>
          <Button
            onClick={openUploadModal}
            className="gap-2 bg-emerald-600 text-white hover:bg-emerald-700 dark:bg-emerald-500 dark:hover:bg-emerald-600"
          >
            <FilePlus2 className="size-4" />
            Upload Note
          </Button>
        </div>

        {section === "dashboard" && (
          <>
            <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
              <StatCard
                label="Total Notes"
                value={stats.total}
                icon={BookOpen}
                loading={dataLoading}
              />
              <StatCard
                label="Published"
                value={stats.published}
                icon={Eye}
                accent="emerald"
                loading={dataLoading}
              />
              <StatCard
                label="Drafts"
                value={stats.draft}
                icon={FileEdit}
                accent="amber"
                loading={dataLoading}
              />
              <StatCard
                label="Unpublished"
                value={stats.unpublished}
                icon={ShieldCheck}
                loading={dataLoading}
              />
            </div>

            <ScheduledPublishesCard
              schedules={scheduleWithNotes}
              loading={false}
              onCancel={async (noteId) => {
                try {
                  await useAppStore.getState().cancelSchedule(noteId);
                  toast.success("Scheduled publish cancelled");
                } catch (err) {
                  toast.error("Failed to cancel schedule", {
                    description:
                      err instanceof Error ? err.message : "Try again later.",
                  });
                }
              }}
            />

            <Card>
              <CardHeader>
                <CardTitle className="text-base">Top categories</CardTitle>
                <CardDescription>
                  Distribution of notes across top-level categories.
                </CardDescription>
              </CardHeader>
              <CardContent>
                {dataLoading ? (
                  <div className="flex flex-col gap-3">
                    {Array.from({ length: 4 }).map((_, i) => (
                      <Skeleton key={i} className="h-8 w-full" />
                    ))}
                  </div>
                ) : topCategories.length === 0 ? (
                  <p className="text-sm text-muted-foreground">
                    No categories yet.
                  </p>
                ) : (
                  <div className="flex flex-col gap-2">
                    {topCategories.map((c) => {
                      const max = topCategories[0]?.count ?? 1;
                      const pct = max ? (c.count / max) * 100 : 0;
                      return (
                        <div key={c.id} className="flex items-center gap-3">
                          <div className="w-32 shrink-0 text-sm">{c.name}</div>
                          <div className="relative h-2.5 flex-1 overflow-hidden rounded-full bg-muted">
                            <div
                              className="absolute inset-y-0 left-0 rounded-full bg-emerald-500"
                              style={{ width: `${pct}%` }}
                            />
                          </div>
                          <div className="w-8 shrink-0 text-right text-xs text-muted-foreground">
                            {c.count}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                )}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-base">Recent notes</CardTitle>
                <CardDescription>
                  The most recently updated notes across all categories.
                </CardDescription>
              </CardHeader>
              <CardContent className="px-0 pb-0">
                <NotesTable
                  notes={recentNotes}
                  loading={dataLoading}
                  onOpen={openNote}
                  onTogglePublish={handleTogglePublish}
                  onDelete={setDeleteTarget}
                  onSchedulePublish={handleOpenSchedule}
                  onVersionHistory={handleOpenVersions}
                  busyId={busyId}
                  pendingSchedules={pendingSchedules}
                  enableSelection={false}
                />
              </CardContent>
            </Card>
          </>
        )}

        {section === "notes" && (
          <Card className="overflow-visible">
            <CardHeader>
              <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <CardTitle className="text-base">All notes</CardTitle>
                  <CardDescription>
                    Filter, publish, unpublish, or delete notes.
                  </CardDescription>
                </div>
                <div className="flex flex-wrap items-center gap-2">
                  <div className="relative">
                    <Search className="pointer-events-none absolute left-2.5 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
                    <Input
                      value={search}
                      onChange={(e) => setSearch(e.target.value)}
                      placeholder="Filter…"
                      className="h-9 w-full pl-8 sm:w-56"
                    />
                  </div>
                  <Select
                    value={statusFilter}
                    onValueChange={(v) =>
                      setStatusFilter(v as NoteStatus | "ALL")
                    }
                  >
                    <SelectTrigger className="h-9 w-[140px]">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="ALL">All statuses</SelectItem>
                      <SelectItem value="PUBLISHED">Published</SelectItem>
                      <SelectItem value="DRAFT">Draft</SelectItem>
                      <SelectItem value="UNPUBLISHED">Unpublished</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
            </CardHeader>
            <CardContent className="px-0 pb-0">
              <BulkActionBar
                selectedIds={[...selectedIds]}
                onClear={clearSelection}
              />
              <NotesTable
                notes={filteredNotes}
                loading={dataLoading}
                onOpen={openNote}
                onTogglePublish={handleTogglePublish}
                onDelete={setDeleteTarget}
                onSchedulePublish={handleOpenSchedule}
                onVersionHistory={handleOpenVersions}
                busyId={busyId}
                pendingSchedules={pendingSchedules}
                enableSelection
                selectedIds={selectedIds}
                onToggleSelect={toggleSelect}
                onSelectAll={(ids, checked) => {
                  setSelectedIds((prev) => {
                    const next = new Set(prev);
                    if (checked) {
                      for (const id of ids) next.add(id);
                    } else {
                      for (const id of ids) next.delete(id);
                    }
                    return next;
                  });
                }}
                onClearSelection={clearSelection}
              />
            </CardContent>
          </Card>
        )}

        {section === "categories" && (
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Categories</CardTitle>
              <CardDescription>
                Top-level categories and their subcategories.
              </CardDescription>
            </CardHeader>
            <CardContent>
              {categories.filter((c) => !c.parentId).length === 0 ? (
                <p className="text-sm text-muted-foreground">
                  No categories yet.
                </p>
              ) : (
                <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
                  {categories
                    .filter((c) => !c.parentId)
                    .map((c) => {
                      const subs = categories.filter(
                        (sub) => sub.parentId === c.id,
                      );
                      const count =
                        notes.filter(
                          (n) =>
                            n.categoryId === c.id ||
                            subs.some((s) => n.categoryId === s.id),
                        ).length ?? 0;
                      return (
                        <div
                          key={c.id}
                          className="rounded-xl border border-border/60 bg-card p-4"
                        >
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2">
                              <span className="flex size-8 items-center justify-center rounded-md bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300">
                                <FolderTree className="size-4" />
                              </span>
                              <span className="text-sm font-medium">
                                {c.name}
                              </span>
                            </div>
                            <Badge variant="secondary">{count}</Badge>
                          </div>
                          {subs.length > 0 && (
                            <div className="mt-3 flex flex-wrap gap-1.5">
                              {subs.map((s) => (
                                <Badge
                                  key={s.id}
                                  variant="outline"
                                  className="font-normal text-muted-foreground"
                                >
                                  {s.name}
                                </Badge>
                              ))}
                            </div>
                          )}
                          {c.description && (
                            <p className="mt-3 text-xs text-muted-foreground">
                              {c.description}
                            </p>
                          )}
                        </div>
                      );
                    })}
                </div>
              )}
            </CardContent>
          </Card>
        )}

        {section === "tags" && (
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Tags</CardTitle>
              <CardDescription>
                All tags currently in use across notes.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <TagsCloud notes={notes} />
            </CardContent>
          </Card>
        )}

        {section === "settings" && <SettingsPanel />}
      </main>

      <AlertDialog
        open={!!deleteTarget}
        onOpenChange={(o) => (!o ? setDeleteTarget(null) : null)}
      >
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Delete this note?</AlertDialogTitle>
            <AlertDialogDescription>
              <span className="block">
                You are about to permanently delete{" "}
                <strong>{deleteTarget?.title}</strong>.
              </span>
              <span className="mt-1 block">
                This action cannot be undone.
              </span>
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction
              onClick={handleDelete}
              className="bg-destructive text-white hover:bg-destructive/90 dark:bg-destructive/60"
            >
              Delete
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>

      <SchedulePublishDialog
        open={scheduleOpen}
        onOpenChange={setScheduleOpen}
        note={scheduleTarget}
        pendingSchedules={pendingSchedules}
      />

      <VersionHistoryDialog
        open={versionOpen}
        onOpenChange={setVersionOpen}
        note={versionTarget}
      />
    </div>
  );
}

// ---------- Sub-components ----------

interface StatCardProps {
  label: string;
  value: number;
  icon: React.ElementType;
  accent?: "default" | "emerald" | "amber";
  loading?: boolean;
}

function StatCard({ label, value, icon: Icon, accent = "default", loading }: StatCardProps) {
  const accentClass =
    accent === "emerald"
      ? "bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300"
      : accent === "amber"
        ? "bg-amber-50 text-amber-700 dark:bg-amber-950/40 dark:text-amber-300"
        : "bg-muted text-muted-foreground";
  return (
    <Card className="overflow-hidden">
      <CardContent className="flex items-center gap-3 p-4">
        <span
          className={cn(
            "flex size-10 items-center justify-center rounded-lg",
            accentClass,
          )}
        >
          <Icon className="size-5" />
        </span>
        <div className="flex flex-col">
          <span className="text-2xl font-semibold leading-none">
            {loading ? <Skeleton className="h-6 w-10" /> : value}
          </span>
          <span className="mt-1 text-xs text-muted-foreground">{label}</span>
        </div>
      </CardContent>
    </Card>
  );
}

interface ScheduledPublishesCardProps {
  schedules: { schedule: ScheduledPublish; note: Note | null }[];
  loading: boolean;
  onCancel: (noteId: string) => void | Promise<void>;
}

function ScheduledPublishesCard({
  schedules,
  loading,
  onCancel,
}: ScheduledPublishesCardProps) {
  const [busyId, setBusyId] = React.useState<string | null>(null);
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-base">
          <CalendarClock className="size-4 text-emerald-600 dark:text-emerald-400" />
          Scheduled publishes
        </CardTitle>
        <CardDescription>
          Notes queued to be published automatically by the cron job.
        </CardDescription>
      </CardHeader>
      <CardContent>
        {loading ? (
          <div className="flex flex-col gap-2">
            {Array.from({ length: 2 }).map((_, i) => (
              <Skeleton key={i} className="h-10 w-full" />
            ))}
          </div>
        ) : schedules.length === 0 ? (
          <p className="text-sm text-muted-foreground">
            No pending scheduled publishes. Use the row menu on a note to
            schedule one.
          </p>
        ) : (
          <ul className="flex flex-col gap-2">
            {schedules.map(({ schedule, note }) => (
              <li
                key={schedule.id}
                className="flex flex-wrap items-center justify-between gap-2 rounded-lg border border-border/60 bg-card p-3"
              >
                <div className="flex min-w-0 flex-col gap-0.5">
                  <span className="truncate text-sm font-medium">
                    {note?.title ?? "Unknown note"}
                  </span>
                  <span className="text-xs text-muted-foreground">
                    {formatDateTime(schedule.publishAt)} ·{" "}
                    {fromNow(schedule.publishAt)}
                  </span>
                </div>
                <Button
                  size="sm"
                  variant="outline"
                  className="gap-1.5 border-destructive/40 text-destructive hover:bg-destructive/10 hover:text-destructive"
                  disabled={busyId === schedule.noteId}
                  onClick={async () => {
                    setBusyId(schedule.noteId);
                    try {
                      await onCancel(schedule.noteId);
                    } finally {
                      setBusyId(null);
                    }
                  }}
                >
                  {busyId === schedule.noteId ? (
                    <Loader2 className="size-3.5 animate-spin" />
                  ) : (
                    <XCircle className="size-3.5" />
                  )}
                  Cancel
                </Button>
              </li>
            ))}
          </ul>
        )}
      </CardContent>
    </Card>
  );
}

interface NotesTableProps {
  notes: Note[];
  loading: boolean;
  onOpen: (note: Note) => void;
  onTogglePublish: (note: Note) => void;
  onDelete: (note: Note) => void;
  onSchedulePublish: (note: Note) => void;
  onVersionHistory: (note: Note) => void;
  busyId: string | null;
  pendingSchedules: ScheduledPublish[];
  enableSelection?: boolean;
  selectedIds?: Set<string>;
  onToggleSelect?: (id: string) => void;
  onSelectAll?: (ids: string[], checked: boolean) => void;
  onClearSelection?: () => void;
}

function NotesTable({
  notes,
  loading,
  onOpen,
  onTogglePublish,
  onDelete,
  onSchedulePublish,
  onVersionHistory,
  busyId,
  pendingSchedules,
  enableSelection = false,
  selectedIds,
  onToggleSelect,
  onSelectAll,
}: NotesTableProps) {
  const visibleIds = React.useMemo(() => notes.map((n) => n.id), [notes]);
  const selectedCount = selectedIds
    ? visibleIds.filter((id) => selectedIds.has(id)).length
    : 0;
  const headerChecked =
    enableSelection &&
    visibleIds.length > 0 &&
    selectedCount === visibleIds.length;
  const headerIndeterminate =
    enableSelection && selectedCount > 0 && selectedCount < visibleIds.length;

  if (loading) {
    return (
      <div className="flex flex-col gap-2 px-6 pb-4">
        {Array.from({ length: 4 }).map((_, i) => (
          <Skeleton key={i} className="h-10 w-full" />
        ))}
      </div>
    );
  }

  if (notes.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center gap-2 px-6 py-10 text-center">
        <BookOpen className="size-6 text-muted-foreground" />
        <p className="text-sm font-medium">No notes found</p>
        <p className="text-xs text-muted-foreground">
          Try changing the filters, or upload a new note.
        </p>
      </div>
    );
  }

  return (
    <div className="scroll-thin max-h-[420px] overflow-y-auto">
      <Table className="min-w-[560px] sm:min-w-0">
        <TableHeader className="sticky top-0 bg-card">
          <TableRow>
            {enableSelection && (
              <TableHead className="w-10 pl-3">
                <Checkbox
                  aria-label="Select all visible notes"
                  checked={
                    headerIndeterminate
                      ? "indeterminate"
                      : headerChecked
                  }
                  onCheckedChange={(checked) => {
                    onSelectAll?.(visibleIds, checked === true);
                  }}
                />
              </TableHead>
            )}
            <TableHead className={enableSelection ? "pl-0" : "pl-6"}>
              Title
            </TableHead>
            <TableHead className="hidden sm:table-cell">Category</TableHead>
            <TableHead>Status</TableHead>
            <TableHead className="hidden md:table-cell">Updated</TableHead>
            <TableHead className="pr-6 text-right">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {notes.map((note) => {
            const schedule = pendingSchedules.find(
              (s) => s.noteId === note.id && s.status === "PENDING",
            );
            const isSelected = selectedIds?.has(note.id) ?? false;
            return (
              <TableRow
                key={note.id}
                data-selected={isSelected ? "" : undefined}
                className={isSelected ? "bg-emerald-50/60 dark:bg-emerald-950/20" : undefined}
              >
                {enableSelection && (
                  <TableCell className="w-10 pl-3">
                    <Checkbox
                      aria-label={`Select ${note.title}`}
                      checked={isSelected}
                      onCheckedChange={() => onToggleSelect?.(note.id)}
                    />
                  </TableCell>
                )}
                <TableCell className={enableSelection ? "pl-0" : "pl-6"}>
                  <button
                    onClick={() => onOpen(note)}
                    className="flex flex-col items-start text-left"
                  >
                    <span className="text-sm font-medium hover:text-emerald-700 dark:hover:text-emerald-300">
                      {note.title}
                    </span>
                    {note.description && (
                      <span className="line-clamp-1 max-w-[36ch] text-xs text-muted-foreground">
                        {note.description}
                      </span>
                    )}
                  </button>
                </TableCell>
                <TableCell className="hidden sm:table-cell">
                  <span className="text-xs text-muted-foreground">
                    {note.category?.name ?? "—"}
                  </span>
                </TableCell>
                <TableCell>
                  <StatusBadge status={note.status} />
                </TableCell>
                <TableCell className="hidden md:table-cell text-xs text-muted-foreground">
                  {fromNow(note.updatedAt)}
                </TableCell>
                <TableCell className="pr-6 text-right">
                  <div className="flex items-center justify-end gap-1">
                    <Button
                      size="icon"
                      variant="ghost"
                      className="size-8"
                      onClick={() => onOpen(note)}
                      aria-label="View note"
                    >
                      <Eye className="size-4" />
                    </Button>
                    <Button
                      size="icon"
                      variant="ghost"
                      className="size-8"
                      onClick={() => onTogglePublish(note)}
                      disabled={busyId === note.id}
                      aria-label={
                        note.status === "PUBLISHED" ? "Unpublish" : "Publish"
                      }
                      title={
                        note.status === "PUBLISHED" ? "Unpublish" : "Publish"
                      }
                    >
                      {busyId === note.id ? (
                        <Loader2 className="size-4 animate-spin" />
                      ) : note.status === "PUBLISHED" ? (
                        <ShieldCheck className="size-4" />
                      ) : (
                        <FileEdit className="size-4" />
                      )}
                    </Button>
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button
                          size="icon"
                          variant="ghost"
                          className="size-8"
                          aria-label="More actions"
                        >
                          <MoreHorizontal className="size-4" />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end" className="w-52">
                        <DropdownMenuLabel>Actions</DropdownMenuLabel>
                        <DropdownMenuItem onClick={() => onOpen(note)}>
                          <Eye className="size-4" />
                          View
                        </DropdownMenuItem>
                        <DropdownMenuItem onClick={() => onTogglePublish(note)}>
                          {note.status === "PUBLISHED" ? (
                            <>
                              <ShieldCheck className="size-4" />
                              Unpublish
                            </>
                          ) : (
                            <>
                              <FileEdit className="size-4" />
                              Publish
                            </>
                          )}
                        </DropdownMenuItem>
                        <DropdownMenuSeparator />
                        {schedule ? (
                          <DropdownMenuItem
                            onClick={() => onSchedulePublish(note)}
                          >
                            <XCircle className="size-4" />
                            <span className="flex flex-col">
                              <span>Cancel scheduled publish</span>
                              <span className="text-[10px] text-muted-foreground">
                                {formatDateTime(schedule.publishAt)}
                              </span>
                            </span>
                          </DropdownMenuItem>
                        ) : (
                          <DropdownMenuItem
                            onClick={() => onSchedulePublish(note)}
                          >
                            <CalendarClock className="size-4" />
                            Schedule publish…
                          </DropdownMenuItem>
                        )}
                        <DropdownMenuItem
                          onClick={() => onVersionHistory(note)}
                        >
                          <History className="size-4" />
                          Version history…
                        </DropdownMenuItem>
                        <DropdownMenuSeparator />
                        <DropdownMenuItem
                          variant="destructive"
                          onClick={() => onDelete(note)}
                        >
                          <Trash2 className="size-4" />
                          Delete
                        </DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </div>
                </TableCell>
              </TableRow>
            );
          })}
        </TableBody>
      </Table>
    </div>
  );
}

function TagsCloud({ notes }: { notes: Note[] }) {
  const tagMap = React.useMemo(() => {
    const m = new Map<string, number>();
    for (const n of notes) {
      for (const t of n.tags ?? []) {
        m.set(t.name, (m.get(t.name) ?? 0) + 1);
      }
    }
    return Array.from(m.entries()).sort((a, b) => b[1] - a[1]);
  }, [notes]);

  if (tagMap.length === 0) {
    return (
      <p className="text-sm text-muted-foreground">No tags are in use yet.</p>
    );
  }
  return (
    <div className="flex flex-wrap gap-2">
      {tagMap.map(([name, count]) => (
        <Badge
          key={name}
          variant="outline"
          className="gap-1.5 py-1 font-normal"
        >
          <Tag className="size-3" />
          {name}
          <span className="text-xs text-muted-foreground">{count}</span>
        </Badge>
      ))}
    </div>
  );
}

function SettingsPanel() {
  const logout = useAppStore((s) => s.logout);
  const clearRecent = useAppStore((s) => s.clearRecent);
  const [clearing, setClearing] = React.useState(false);

  const handleClearRecent = async () => {
    setClearing(true);
    try {
      await clearRecent();
      toast.success("Reading history cleared");
    } catch (err) {
      toast.error("Failed to clear history", {
        description: err instanceof Error ? err.message : "Try again later.",
      });
    } finally {
      setClearing(false);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-base">Settings</CardTitle>
        <CardDescription>
          Manage your CMS administrator account and site preferences.
        </CardDescription>
      </CardHeader>
      <CardContent className="flex flex-col gap-4">
        <div className="rounded-lg border border-border/60 bg-muted/30 p-4">
          <p className="text-sm font-medium">Account</p>
          <p className="text-xs text-muted-foreground">
            You are signed in as an administrator. Sign out from this device.
          </p>
          <Button
            variant="outline"
            size="sm"
            className="mt-3 gap-2"
            onClick={() => logout()}
          >
            <ShieldCheck className="size-4" />
            Sign out
          </Button>
        </div>

        <div className="rounded-lg border border-border/60 bg-muted/30 p-4">
          <p className="text-sm font-medium">Privacy</p>
          <p className="text-xs text-muted-foreground">
            Clear the notes you have recently viewed from this device. This
            affects the &ldquo;Continue reading&rdquo; list in the reader.
          </p>
          <Button
            variant="outline"
            size="sm"
            className="mt-3 gap-2 border-destructive/40 text-destructive hover:bg-destructive/10 hover:text-destructive"
            disabled={clearing}
            onClick={handleClearRecent}
          >
            {clearing ? (
              <Loader2 className="size-4 animate-spin" />
            ) : (
              <Trash2 className="size-4" />
            )}
            Clear my reading history
          </Button>
        </div>

        <div className="rounded-lg border border-dashed border-border/60 p-4 text-xs text-muted-foreground">
          Additional settings (default category, upload size limit, public
          registration) will be available here once the backend is wired up.
        </div>
      </CardContent>
    </Card>
  );
}
