"use client";

import * as React from "react";
import {
  BookOpen,
  LayoutGrid,
  LogOut,
  Menu,
  Search,
  ShieldCheck,
  Tags,
} from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ModeToggle } from "@/components/mode-toggle";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import { useAppStore } from "@/lib/store";
import { cn } from "@/lib/utils";

export function SiteHeader() {
  const user = useAppStore((s) => s.user);
  const view = useAppStore((s) => s.view);
  const openLoginModal = useAppStore((s) => s.openLoginModal);
  const logout = useAppStore((s) => s.logout);
  const goHome = useAppStore((s) => s.goHome);
  const goSearch = useAppStore((s) => s.goSearch);
  const goToDashboard = useAppStore((s) => s.goToDashboard);
  const searchQuery = useAppStore((s) => s.searchQuery);
  const setSearchQuery = useAppStore((s) => s.setSearchQuery);
  const runSearch = useAppStore((s) => s.runSearch);
  const openUploadModal = useAppStore((s) => s.openUploadModal);

  const [localSearch, setLocalSearch] = React.useState(searchQuery);
  const [mobileOpen, setMobileOpen] = React.useState(false);
  React.useEffect(() => setLocalSearch(searchQuery), [searchQuery]);

  const onSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    runSearch(localSearch);
  };

  const navItems = [
    {
      label: "Notes",
      icon: BookOpen,
      action: () => {
        goHome();
        setMobileOpen(false);
      },
      active: view === "public-home",
    },
    {
      label: "Categories",
      icon: Tags,
      action: () => {
        goHome();
        setMobileOpen(false);
      },
      active: false,
    },
    {
      label: "Search",
      icon: Search,
      action: () => {
        goSearch(localSearch);
        setMobileOpen(false);
      },
      active: view === "search-results",
    },
  ];

  return (
    <header
      className={cn(
        "sticky top-0 z-40 w-full border-b border-border/60",
        "bg-background/80 backdrop-blur supports-[backdrop-filter]:bg-background/60",
      )}
    >
      <div className="mx-auto flex h-16 max-w-7xl items-center gap-3 px-4 sm:px-6 lg:px-8">
        <button
          onClick={goHome}
          className="flex items-center gap-2 outline-none"
          aria-label="Technical Notes home"
        >
          <span className="flex size-9 items-center justify-center rounded-lg bg-emerald-600 text-white shadow-sm dark:bg-emerald-500">
            <BookOpen className="size-5" />
          </span>
          <span className="hidden flex-col items-start leading-none sm:flex">
            <span className="text-sm font-semibold tracking-tight">
              Technical Notes
            </span>
            <span className="text-[11px] text-muted-foreground">
              Knowledge Base CMS
            </span>
          </span>
        </button>

        <nav
          aria-label="Primary"
          className="ml-2 hidden items-center gap-1 md:flex"
        >
          {navItems.map((item) => (
            <Button
              key={item.label}
              variant={item.active ? "secondary" : "ghost"}
              size="sm"
              onClick={item.action}
              className={cn(
                "text-muted-foreground",
                item.active && "text-foreground",
              )}
            >
              <item.icon className="size-4" />
              {item.label}
            </Button>
          ))}
        </nav>

        <form
          onSubmit={onSearchSubmit}
          className="ml-auto hidden flex-1 max-w-sm lg:flex"
        >
          <div className="relative w-full">
            <Search className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
            <Input
              value={localSearch}
              onChange={(e) => {
                setLocalSearch(e.target.value);
                setSearchQuery(e.target.value);
              }}
              placeholder="Search notes, tags, topics…"
              className="pl-9"
              aria-label="Search notes"
            />
          </div>
        </form>

        <div className="ml-auto flex items-center gap-1.5 lg:ml-2">
          <ModeToggle />

          {user ? (
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button size="sm" variant="outline" className="gap-2">
                  <ShieldCheck className="size-4 text-emerald-600 dark:text-emerald-400" />
                  <span className="hidden max-w-[10rem] truncate sm:inline">
                    {user.name ?? user.email}
                  </span>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-52">
                <DropdownMenuLabel>
                  <div className="flex flex-col">
                    <span className="text-sm font-medium">{user.name ?? "Admin"}</span>
                    <span className="text-xs font-normal text-muted-foreground">
                      {user.email}
                    </span>
                  </div>
                </DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={goToDashboard}>
                  <LayoutGrid className="size-4" />
                  Dashboard
                </DropdownMenuItem>
                <DropdownMenuItem onClick={openUploadModal}>
                  <BookOpen className="size-4" />
                  Upload Note
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem
                  variant="destructive"
                  onClick={() => {
                    void logout();
                  }}
                >
                  <LogOut className="size-4" />
                  Sign out
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          ) : (
            <Button
              size="sm"
              onClick={openLoginModal}
              className="bg-emerald-600 text-white hover:bg-emerald-700 dark:bg-emerald-500 dark:hover:bg-emerald-600"
            >
              <ShieldCheck className="size-4" />
              <span className="hidden sm:inline">Admin</span>
            </Button>
          )}

          <Sheet open={mobileOpen} onOpenChange={setMobileOpen}>
            <SheetTrigger asChild>
              <Button
                size="icon"
                variant="ghost"
                className="md:hidden"
                aria-label="Open menu"
              >
                <Menu className="size-5" />
              </Button>
            </SheetTrigger>
            <SheetContent side="right" className="w-[280px] p-0">
              <SheetHeader className="border-b px-4 py-3">
                <SheetTitle className="flex items-center gap-2 text-left">
                  <span className="flex size-7 items-center justify-center rounded-md bg-emerald-600 text-white">
                    <BookOpen className="size-4" />
                  </span>
                  Technical Notes
                </SheetTitle>
              </SheetHeader>
              <div className="flex flex-col gap-1 p-3">
                {navItems.map((item) => (
                  <Button
                    key={item.label}
                    variant={item.active ? "secondary" : "ghost"}
                    onClick={item.action}
                    className="justify-start"
                  >
                    <item.icon className="size-4" />
                    {item.label}
                  </Button>
                ))}
                <form
                  onSubmit={(e) => {
                    onSearchSubmit(e);
                    setMobileOpen(false);
                  }}
                  className="mt-2"
                >
                  <div className="relative">
                    <Search className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
                    <Input
                      value={localSearch}
                      onChange={(e) => {
                        setLocalSearch(e.target.value);
                        setSearchQuery(e.target.value);
                      }}
                      placeholder="Search…"
                      className="pl-9"
                    />
                  </div>
                </form>
                {user ? (
                  <>
                    <Button
                      variant="outline"
                      className="mt-2 justify-start"
                      onClick={() => {
                        goToDashboard();
                        setMobileOpen(false);
                      }}
                    >
                      <LayoutGrid className="size-4" />
                      Dashboard
                    </Button>
                    <Button
                      variant="destructive"
                      className="justify-start"
                      onClick={() => {
                        void logout();
                        setMobileOpen(false);
                      }}
                    >
                      <LogOut className="size-4" />
                      Sign out
                    </Button>
                  </>
                ) : (
                  <Button
                    className="mt-2 bg-emerald-600 text-white hover:bg-emerald-700"
                    onClick={() => {
                      openLoginModal();
                      setMobileOpen(false);
                    }}
                  >
                    <ShieldCheck className="size-4" />
                    Admin Login
                  </Button>
                )}
              </div>
            </SheetContent>
          </Sheet>
        </div>
      </div>
    </header>
  );
}
