"use client";

import * as React from "react";
import {
  CheckCircle2,
  FileCode2,
  FileUp,
  Loader2,
  Save,
  Send,
  Upload as UploadIcon,
  X,
} from "lucide-react";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@/components/ui/tabs";
import { ScrollArea } from "@/components/ui/scroll-area";
import { useAppStore } from "@/lib/store";
import { createNote, fetchNoteContent, uploadFile } from "@/lib/api";
import type { NoteInput, UploadResult } from "@/lib/types";
import { formatFileSize, slugify } from "@/lib/format";
import { cn } from "@/lib/utils";

type Step = "upload" | "metadata" | "preview";

const ACCEPTED_TYPES = [".html", ".htm", ".zip"];

export function UploadNoteDialog() {
  const open = useAppStore((s) => s.uploadModalOpen);
  const close = useAppStore((s) => s.closeUploadModal);
  const categories = useAppStore((s) => s.categories);
  const onNoteCreated = useAppStore((s) => s.onNoteCreated);

  const [step, setStep] = React.useState<Step>("upload");
  const [file, setFile] = React.useState<File | null>(null);
  const [uploading, setUploading] = React.useState(false);
  const [uploadProgress, setUploadProgress] = React.useState(0);
  const [uploadResult, setUploadResult] = React.useState<UploadResult | null>(
    null,
  );
  const [previewHtml, setPreviewHtml] = React.useState<string>("");
  const [previewLoading, setPreviewLoading] = React.useState(false);

  // metadata
  const [title, setTitle] = React.useState("");
  const [categoryId, setCategoryId] = React.useState("");
  const [subcategoryId, setSubcategoryId] = React.useState<string>("");
  const [tagsRaw, setTagsRaw] = React.useState("");
  const [description, setDescription] = React.useState("");
  const [slug, setSlug] = React.useState("");
  const [slugEdited, setSlugEdited] = React.useState(false);
  const [saving, setSaving] = React.useState(false);

  const reset = React.useCallback(() => {
    setStep("upload");
    setFile(null);
    setUploading(false);
    setUploadProgress(0);
    setUploadResult(null);
    setPreviewHtml("");
    setPreviewLoading(false);
    setTitle("");
    setCategoryId("");
    setSubcategoryId("");
    setTagsRaw("");
    setDescription("");
    setSlug("");
    setSlugEdited(false);
    setSaving(false);
  }, []);

  React.useEffect(() => {
    if (open) reset();
  }, [open, reset]);

  // Auto-generate slug from title (unless user edited it)
  React.useEffect(() => {
    if (!slugEdited) {
      setSlug(slugify(title));
    }
  }, [title, slugEdited]);

  // Auto-prefill title from filename
  React.useEffect(() => {
    if (file && !title) {
      const name = file.name.replace(/\.[^.]+$/, "");
      setTitle(name.replace(/[-_]+/g, " ").trim());
    }
  }, [file, title]);

  // Subcategory options for selected top-level category
  const subcategoryOptions = React.useMemo(() => {
    if (!categoryId) return [];
    return categories.filter((c) => c.parentId === categoryId);
  }, [categoryId, categories]);

  const topLevelCategories = React.useMemo(
    () => categories.filter((c) => !c.parentId),
    [categories],
  );

  const onDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    const dropped = e.dataTransfer.files?.[0];
    if (dropped) handleFile(dropped);
  };

  const handleFile = async (selected: File) => {
    const ext = selected.name.slice(selected.name.lastIndexOf(".")).toLowerCase();
    if (!ACCEPTED_TYPES.includes(ext)) {
      toast.error("Unsupported file type", {
        description: "Please upload an .html or .zip file.",
      });
      return;
    }
    setFile(selected);
    setUploading(true);
    setUploadProgress(0);

    // Simulate progress while uploading
    const interval = setInterval(() => {
      setUploadProgress((p) => Math.min(p + 10, 90));
    }, 120);

    try {
      const result = await uploadFile(selected);
      setUploadProgress(100);
      setUploadResult(result);
      toast.success("Upload complete", {
        description: `${result.fileName} (${formatFileSize(result.size)})`,
      });
      // Pre-load preview content
      setPreviewLoading(true);
      const html = await fetchNoteContent(result.contentPath);
      setPreviewHtml(html);
    } catch (err) {
      toast.error("Upload failed", {
        description: err instanceof Error ? err.message : "Try again later.",
      });
      setFile(null);
    } finally {
      clearInterval(interval);
      setUploading(false);
      setPreviewLoading(false);
    }
  };

  const canGoToMetadata = !!uploadResult && !uploading;
  const canSave =
    title.trim() && categoryId && slug.trim() && !!uploadResult;

  const handleSave = async (status: "DRAFT" | "PUBLISHED") => {
    if (!canSave) return;
    setSaving(true);
    const input: NoteInput = {
      title: title.trim(),
      slug: slug.trim(),
      description: description.trim() || undefined,
      categoryId: subcategoryId || categoryId,
      tags: tagsRaw
        .split(",")
        .map((t) => t.trim())
        .filter(Boolean),
      contentPath: uploadResult?.contentPath,
      status,
    };
    try {
      const created = await createNote(input);
      onNoteCreated(created);
      toast.success(
        status === "PUBLISHED" ? "Note published" : "Saved as draft",
        { description: created.title },
      );
      close();
    } catch (err) {
      toast.error("Save failed", {
        description: err instanceof Error ? err.message : "Try again later.",
      });
    } finally {
      setSaving(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={(o) => (!o ? close() : null)}>
      <DialogContent
        showCloseButton={false}
        className="max-h-[90vh] gap-0 overflow-hidden p-0 sm:max-w-3xl"
      >
        <DialogHeader className="border-b px-6 py-4">
          <DialogTitle className="flex items-center gap-2">
            <span className="flex size-8 items-center justify-center rounded-md bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300">
              <FileUp className="size-4" />
            </span>
            Upload a new note
          </DialogTitle>
          <DialogDescription>
            Upload HTML (or a zipped bundle of HTML + assets), then add metadata
            and choose whether to publish immediately.
          </DialogDescription>
        </DialogHeader>

        {/* Stepper */}
        <div className="flex items-center gap-2 border-b bg-muted/30 px-6 py-3 text-xs">
          <Stepper
            current={step}
            step="upload"
            label="Upload"
            index={1}
            onGo={() => setStep("upload")}
            disabled={!file}
          />
          <span className="h-px flex-1 bg-border" />
          <Stepper
            current={step}
            step="metadata"
            label="Metadata"
            index={2}
            onGo={() => canGoToMetadata && setStep("metadata")}
            disabled={!canGoToMetadata}
          />
          <span className="h-px flex-1 bg-border" />
          <Stepper
            current={step}
            step="preview"
            label="Preview & Save"
            index={3}
            onGo={() => canSave && setStep("preview")}
            disabled={!canSave}
          />
        </div>

        <div className="scroll-thin max-h-[60vh] overflow-y-auto px-6 py-5">
          {step === "upload" && (
            <div className="flex flex-col gap-4">
              <div
                onDragOver={(e) => e.preventDefault()}
                onDrop={onDrop}
                className={cn(
                  "flex flex-col items-center justify-center gap-3 rounded-xl border-2 border-dashed px-6 py-10 text-center transition-colors",
                  file
                    ? "border-emerald-500/50 bg-emerald-50/50 dark:bg-emerald-950/20"
                    : "border-border bg-muted/20 hover:border-emerald-500/40 hover:bg-emerald-50/30 dark:hover:bg-emerald-950/10",
                )}
              >
                {uploading ? (
                  <>
                    <Loader2 className="size-8 animate-spin text-emerald-600 dark:text-emerald-400" />
                    <div className="text-sm font-medium">Uploading…</div>
                    <Progress value={uploadProgress} className="h-1.5 w-48" />
                  </>
                ) : file ? (
                  <>
                    <span className="flex size-10 items-center justify-center rounded-md bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300">
                      <FileCode2 className="size-5" />
                    </span>
                    <div>
                      <p className="text-sm font-medium">{file.name}</p>
                      <p className="text-xs text-muted-foreground">
                        {formatFileSize(file.size)}
                      </p>
                    </div>
                    <Button
                      variant="ghost"
                      size="sm"
                      className="gap-1 text-muted-foreground"
                      onClick={() => {
                        setFile(null);
                        setUploadResult(null);
                        setUploadProgress(0);
                      }}
                    >
                      <X className="size-3.5" />
                      Remove
                    </Button>
                  </>
                ) : (
                  <>
                    <span className="flex size-10 items-center justify-center rounded-md bg-muted text-muted-foreground">
                      <UploadIcon className="size-5" />
                    </span>
                    <div>
                      <p className="text-sm font-medium">
                        Drag &amp; drop your file here
                      </p>
                      <p className="text-xs text-muted-foreground">
                        Accepts <code>.html</code> or <code>.zip</code> (HTML
                        + assets)
                      </p>
                    </div>
                    <label htmlFor="upload-input">
                      <Button
                        type="button"
                        size="sm"
                        className="gap-2 bg-emerald-600 text-white hover:bg-emerald-700 dark:bg-emerald-500 dark:hover:bg-emerald-600"
                        onClick={() =>
                          document.getElementById("upload-input")?.click()
                        }
                      >
                        <FileUp className="size-4" />
                        Choose file
                      </Button>
                      <input
                        id="upload-input"
                        type="file"
                        className="hidden"
                        accept={ACCEPTED_TYPES.join(",")}
                        onChange={(e) => {
                          const f = e.target.files?.[0];
                          if (f) handleFile(f);
                          e.currentTarget.value = "";
                        }}
                      />
                    </label>
                  </>
                )}
              </div>

              {uploadResult && (
                <div className="flex items-center gap-2 rounded-md border border-emerald-500/30 bg-emerald-50 px-3 py-2 text-xs text-emerald-800 dark:bg-emerald-950/30 dark:text-emerald-200">
                  <CheckCircle2 className="size-4" />
                  Uploaded to{" "}
                  <code className="rounded bg-background/80 px-1 py-0.5">
                    {uploadResult.contentPath}
                  </code>
                </div>
              )}

              <div className="flex items-center justify-between">
                <p className="text-xs text-muted-foreground">
                  Tip: zip files should contain an <code>index.html</code> at
                  their root.
                </p>
                <Button
                  disabled={!canGoToMetadata}
                  onClick={() => setStep("metadata")}
                  className="gap-2"
                >
                  Continue
                </Button>
              </div>
            </div>
          )}

          {step === "metadata" && (
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <div className="sm:col-span-2 flex flex-col gap-1.5">
                <Label htmlFor="meta-title">Title</Label>
                <Input
                  id="meta-title"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="A descriptive note title"
                />
              </div>

              <div className="flex flex-col gap-1.5">
                <Label htmlFor="meta-slug">Slug</Label>
                <Input
                  id="meta-slug"
                  value={slug}
                  onChange={(e) => {
                    setSlug(e.target.value);
                    setSlugEdited(true);
                  }}
                  placeholder="auto-generated-from-title"
                />
                <p className="text-xs text-muted-foreground">
                  URL-safe identifier used in viewer links.
                </p>
              </div>

              <div className="flex flex-col gap-1.5">
                <Label>Category</Label>
                <Select value={categoryId} onValueChange={(v) => {
                  setCategoryId(v);
                  setSubcategoryId("");
                }}>
                  <SelectTrigger className="w-full">
                    <SelectValue placeholder="Pick a top-level category" />
                  </SelectTrigger>
                  <SelectContent>
                    {topLevelCategories.map((c) => (
                      <SelectItem key={c.id} value={c.id}>
                        {c.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="flex flex-col gap-1.5">
                <Label>Subcategory</Label>
                <Select
                  value={subcategoryId}
                  onValueChange={setSubcategoryId}
                  disabled={subcategoryOptions.length === 0}
                >
                  <SelectTrigger className="w-full">
                    <SelectValue
                      placeholder={
                        subcategoryOptions.length === 0
                          ? "No subcategories"
                          : "Pick a subcategory (optional)"
                      }
                    />
                  </SelectTrigger>
                  <SelectContent>
                    {subcategoryOptions.map((c) => (
                      <SelectItem key={c.id} value={c.id}>
                        {c.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="flex flex-col gap-1.5">
                <Label htmlFor="meta-tags">Tags</Label>
                <Input
                  id="meta-tags"
                  value={tagsRaw}
                  onChange={(e) => setTagsRaw(e.target.value)}
                  placeholder="selinux, hardening, linux"
                />
                <p className="text-xs text-muted-foreground">
                  Comma-separated list of tags.
                </p>
              </div>

              <div className="sm:col-span-2 flex flex-col gap-1.5">
                <Label htmlFor="meta-desc">Description</Label>
                <Textarea
                  id="meta-desc"
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="A short summary shown on cards and search results."
                  rows={3}
                />
              </div>

              {tagsRaw.trim() && (
                <div className="sm:col-span-2 flex flex-wrap items-center gap-1.5">
                  <span className="text-xs text-muted-foreground">Tags:</span>
                  {tagsRaw
                    .split(",")
                    .map((t) => t.trim())
                    .filter(Boolean)
                    .map((t, i) => (
                      <Badge key={`${t}-${i}`} variant="outline">
                        {t}
                      </Badge>
                    ))}
                </div>
              )}

              <div className="sm:col-span-2 flex items-center justify-between">
                <Button variant="ghost" onClick={() => setStep("upload")}>
                  Back
                </Button>
                <Button
                  disabled={!canSave}
                  onClick={() => setStep("preview")}
                  className="gap-2"
                >
                  Preview
                </Button>
              </div>
            </div>
          )}

          {step === "preview" && (
            <div className="flex flex-col gap-4">
              <div className="rounded-lg border border-border/60 bg-muted/30 p-4 text-sm">
                <div className="grid grid-cols-2 gap-x-6 gap-y-2 sm:grid-cols-3">
                  <Field label="Title" value={title} />
                  <Field label="Slug" value={slug} />
                  <Field
                    label="Category"
                    value={
                      categories.find((c) => c.id === categoryId)?.name ?? "—"
                    }
                  />
                  <Field
                    label="Subcategory"
                    value={
                      categories.find((c) => c.id === subcategoryId)?.name ??
                      "—"
                    }
                  />
                  <Field
                    label="Tags"
                    value={
                      tagsRaw
                        .split(",")
                        .map((t) => t.trim())
                        .filter(Boolean)
                        .join(", ") || "—"
                    }
                  />
                  <Field
                    label="File"
                    value={uploadResult?.fileName ?? "—"}
                  />
                </div>
                {description && (
                  <div className="mt-3 border-t border-border/60 pt-3">
                    <p className="text-xs text-muted-foreground">Description</p>
                    <p className="mt-1 text-sm">{description}</p>
                  </div>
                )}
              </div>

              <Tabs defaultValue="render">
                <div className="flex items-center justify-between">
                  <TabsList>
                    <TabsTrigger value="render">Rendered</TabsTrigger>
                    <TabsTrigger value="source">Source</TabsTrigger>
                  </TabsList>
                  <span className="text-xs text-muted-foreground">
                    {uploadResult?.fileName ?? ""}
                  </span>
                </div>
                <TabsContent value="render">
                  <div className="overflow-hidden rounded-lg border border-border/60 bg-white">
                    {previewLoading ? (
                      <div className="flex h-64 items-center justify-center">
                        <Loader2 className="size-6 animate-spin text-muted-foreground" />
                      </div>
                    ) : (
                      <iframe
                        title="Note preview"
                        className="note-iframe h-[420px]"
                        srcDoc={previewHtml}
                        sandbox="allow-same-origin"
                      />
                    )}
                  </div>
                </TabsContent>
                <TabsContent value="source">
                  <ScrollArea className="h-[420px] rounded-lg border border-border/60 bg-muted/30 p-3">
                    <pre className="scroll-thin overflow-auto text-xs leading-relaxed">
                      <code>{previewHtml}</code>
                    </pre>
                  </ScrollArea>
                </TabsContent>
              </Tabs>

              <div className="flex flex-wrap items-center justify-between gap-2">
                <Button variant="ghost" onClick={() => setStep("metadata")}>
                  Back to metadata
                </Button>
                <div className="flex items-center gap-2">
                  <Button
                    variant="outline"
                    onClick={() => handleSave("DRAFT")}
                    disabled={saving}
                    className="gap-2"
                  >
                    {saving ? (
                      <Loader2 className="size-4 animate-spin" />
                    ) : (
                      <Save className="size-4" />
                    )}
                    Save as Draft
                  </Button>
                  <Button
                    onClick={() => handleSave("PUBLISHED")}
                    disabled={saving}
                    className="gap-2 bg-emerald-600 text-white hover:bg-emerald-700 dark:bg-emerald-500 dark:hover:bg-emerald-600"
                  >
                    {saving ? (
                      <Loader2 className="size-4 animate-spin" />
                    ) : (
                      <Send className="size-4" />
                    )}
                    Publish
                  </Button>
                </div>
              </div>
            </div>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
}

interface StepperProps {
  current: Step;
  step: Step;
  label: string;
  index: number;
  onGo: () => void;
  disabled?: boolean;
}

function Stepper({ current, step, label, index, onGo, disabled }: StepperProps) {
  const active = current === step;
  const done =
    (current === "metadata" && step === "upload") ||
    (current === "preview" && (step === "upload" || step === "metadata"));
  return (
    <button
      type="button"
      onClick={() => !disabled && onGo()}
      disabled={disabled}
      className={cn(
        "flex items-center gap-2 rounded-full px-2 py-1 transition-colors",
        active && "bg-emerald-100 text-emerald-800 dark:bg-emerald-950/40 dark:text-emerald-200",
        !active && !done && "text-muted-foreground",
        done && "text-emerald-700 dark:text-emerald-300",
        disabled && "cursor-not-allowed opacity-60",
      )}
    >
      <span
        className={cn(
          "flex size-5 items-center justify-center rounded-full border text-[10px] font-semibold",
          active
            ? "border-emerald-500 bg-emerald-500 text-white"
            : done
              ? "border-emerald-500 text-emerald-700 dark:text-emerald-300"
              : "border-border text-muted-foreground",
        )}
      >
        {done ? <CheckCircle2 className="size-3.5" /> : index}
      </span>
      <span className="hidden font-medium sm:inline">{label}</span>
    </button>
  );
}

function Field({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="text-xs text-muted-foreground">{label}</p>
      <p className="truncate text-sm font-medium" title={value}>
        {value || "—"}
      </p>
    </div>
  );
}
