"use client";

import * as React from "react";
import { Loader2 } from "lucide-react";

import { SiteHeader } from "@/components/site-header";
import { SiteFooter } from "@/components/site-footer";
import { AdminLoginDialog } from "@/components/views/admin-login";
import { AdminDashboard } from "@/components/views/admin-dashboard";
import { PublicHome } from "@/components/views/public-home";
import { NoteViewer } from "@/components/views/note-viewer";
import { SearchResults } from "@/components/views/search-results";
import { UploadNoteDialog } from "@/components/views/upload-note";
import { SearchModal } from "@/components/search-modal";
import { useAppStore } from "@/lib/store";
import type { ViewKey } from "@/lib/types";

export default function Home() {
  const view = useAppStore((s) => s.view);
  const bootstrap = useAppStore((s) => s.bootstrap);
  const authLoading = useAppStore((s) => s.authLoading);
  const user = useAppStore((s) => s.user);
  const openLoginModal = useAppStore((s) => s.openLoginModal);
  const openSearchModal = useAppStore((s) => s.openSearchModal);
  const bootedRef = React.useRef(false);

  React.useEffect(() => {
    if (bootedRef.current) return;
    bootedRef.current = true;
    void bootstrap();
  }, [bootstrap]);

  // Hidden keyboard shortcut: Ctrl+Shift+A to open admin login
  React.useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.ctrlKey && e.shiftKey && e.key === "A") {
        e.preventDefault();
        if (!useAppStore.getState().user) {
          openLoginModal();
        }
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [openLoginModal]);

  // Cmd/Ctrl+K opens the global search window
  React.useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && (e.key === "k" || e.key === "K")) {
        e.preventDefault();
        openSearchModal();
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [openSearchModal]);

  // Admin-only views: bounce back to public if not signed in.
  const effectiveView: ViewKey =
    view === "admin-dashboard" && !user ? "public-home" : view;

  return (
    <div className="flex min-h-screen flex-col bg-background text-foreground">
      {/* Hide global header/footer when in note-viewer (reader has its own top bar) */}
      {effectiveView !== "note-viewer" && <SiteHeader />}

      <main className="flex flex-1 flex-col">
        {authLoading ? (
          <div className="flex flex-1 items-center justify-center p-12 text-muted-foreground">
            <Loader2 className="mr-2 size-5 animate-spin" />
            Loading…
          </div>
        ) : (
          <>
            {effectiveView === "public-home" && <PublicHome />}
            {effectiveView === "admin-dashboard" && <AdminDashboard />}
            {effectiveView === "note-viewer" && <NoteViewer />}
            {effectiveView === "search-results" && <SearchResults />}
          </>
        )}
      </main>

      {effectiveView !== "note-viewer" && <SiteFooter />}

      {/* Admin login dialog — always mounted (accessible via Ctrl+Shift+A) */}
      <AdminLoginDialog />

      {/* Upload dialog — only when admin is authenticated */}
      {user && <UploadNoteDialog />}

      {/* Global search window — accessible everywhere via Cmd/Ctrl+K */}
      <SearchModal />
    </div>
  );
}
