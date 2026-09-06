"use client";

import * as React from "react";
import { AlertCircle, KeyRound, Loader2, ShieldCheck } from "lucide-react";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { useAppStore } from "@/lib/store";

export function AdminLoginDialog() {
  const open = useAppStore((s) => s.loginModalOpen);
  const closeLoginModal = useAppStore((s) => s.closeLoginModal);
  const login = useAppStore((s) => s.login);
  const authLoading = useAppStore((s) => s.authLoading);

  const [email, setEmail] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [error, setError] = React.useState<string | null>(null);

  React.useEffect(() => {
    if (open) {
      setError(null);
    }
  }, [open]);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    if (!email || !password) {
      setError("Email and password are required.");
      return;
    }
    try {
      await login(email.trim(), password);
      toast.success("Welcome back", {
        description: "You are now signed in to the admin dashboard.",
      });
    } catch (err) {
      const message =
        err instanceof Error ? err.message : "Login failed. Please try again.";
      setError(message);
      toast.error("Login failed", { description: message });
    }
  };

  return (
    <Dialog open={open} onOpenChange={(o) => (!o ? closeLoginModal() : null)}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <div className="mb-2 flex size-11 items-center justify-center rounded-xl bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300">
            <ShieldCheck className="size-6" />
          </div>
          <DialogTitle className="text-xl">Admin sign in</DialogTitle>
          <DialogDescription>
            Sign in to manage notes, categories, and uploads. Use your CMS
            administrator credentials.
          </DialogDescription>
        </DialogHeader>

        <form onSubmit={onSubmit} className="flex flex-col gap-4">
          {error && (
            <Alert variant="destructive">
              <AlertCircle className="size-4" />
              <AlertTitle>Authentication error</AlertTitle>
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          <div className="flex flex-col gap-1.5">
            <Label htmlFor="login-email">Email</Label>
            <Input
              id="login-email"
              type="email"
              autoComplete="email"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="flex flex-col gap-1.5">
            <div className="flex items-center justify-between">
              <Label htmlFor="login-password">Password</Label>
              <a
                href="#"
                className="text-xs text-emerald-700 hover:underline dark:text-emerald-300"
                onClick={(e) => {
                  e.preventDefault();
                  toast.info("Password recovery is not enabled in demo mode.");
                }}
              >
                Forgot password?
              </a>
            </div>
            <Input
              id="login-password"
              type="password"
              autoComplete="current-password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <div className="rounded-md border border-dashed border-border/60 bg-muted/40 px-3 py-2 text-xs text-muted-foreground">
            <span className="font-medium text-foreground">Note:</span> Use the
            administrator credentials provisioned by the CMS-1 backend. If no
            admin user exists yet, ask the backend agent to seed one.
          </div>

          <Button
            type="submit"
            disabled={authLoading}
            className="gap-2 bg-emerald-600 text-white hover:bg-emerald-700 dark:bg-emerald-500 dark:hover:bg-emerald-600"
          >
            {authLoading ? (
              <Loader2 className="size-4 animate-spin" />
            ) : (
              <KeyRound className="size-4" />
            )}
            {authLoading ? "Signing in…" : "Sign in"}
          </Button>
        </form>
      </DialogContent>
    </Dialog>
  );
}
