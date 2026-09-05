import type { NoteStatus } from "@/lib/types";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

interface StatusBadgeProps {
  status: NoteStatus;
  className?: string;
}

const STATUS_META: Record<
  NoteStatus,
  { label: string; className: string }
> = {
  PUBLISHED: {
    label: "Published",
    className:
      "border-transparent bg-emerald-100 text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-300",
  },
  DRAFT: {
    label: "Draft",
    className:
      "border-transparent bg-amber-100 text-amber-700 dark:bg-amber-950/60 dark:text-amber-300",
  },
  UNPUBLISHED: {
    label: "Unpublished",
    className:
      "border-transparent bg-slate-200 text-slate-600 dark:bg-slate-800 dark:text-slate-300",
  },
};

export function StatusBadge({ status, className }: StatusBadgeProps) {
  const meta = STATUS_META[status];
  return (
    <Badge variant="outline" className={cn(meta.className, className)}>
      <span
        className="mr-1 inline-block size-1.5 rounded-full"
        style={{ backgroundColor: "currentColor" }}
      />
      {meta.label}
    </Badge>
  );
}
