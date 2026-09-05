import { BookOpen, Github, Rss, Twitter } from "lucide-react";

export function SiteFooter() {
  return (
    <footer className="mt-auto border-t border-border/60 bg-muted/30">
      <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        <div className="flex flex-col items-start justify-between gap-6 md:flex-row md:items-center">
          <div className="flex items-center gap-2">
            <span className="flex size-8 items-center justify-center rounded-md bg-emerald-600 text-white">
              <BookOpen className="size-4" />
            </span>
            <div className="flex flex-col leading-tight">
              <span className="text-sm font-semibold">Technical Notes</span>
              <span className="text-xs text-muted-foreground">
                A self-hosted knowledge base for engineers.
              </span>
            </div>
          </div>

          <nav
            aria-label="Footer"
            className="flex flex-wrap items-center gap-x-5 gap-y-2 text-sm text-muted-foreground"
          >
            <a className="hover:text-foreground" href="#">
              About
            </a>
            <a className="hover:text-foreground" href="#">
              Categories
            </a>
            <a className="hover:text-foreground" href="#">
              RSS
            </a>
            <a className="hover:text-foreground" href="#">
              Privacy
            </a>
          </nav>

          <div className="flex items-center gap-2 text-muted-foreground">
            <a
              aria-label="GitHub"
              href="#"
              className="rounded-md p-2 hover:bg-accent hover:text-foreground"
            >
              <Github className="size-4" />
            </a>
            <a
              aria-label="Twitter"
              href="#"
              className="rounded-md p-2 hover:bg-accent hover:text-foreground"
            >
              <Twitter className="size-4" />
            </a>
            <a
              aria-label="RSS"
              href="#"
              className="rounded-md p-2 hover:bg-accent hover:text-foreground"
            >
              <Rss className="size-4" />
            </a>
          </div>
        </div>

        <div className="mt-6 border-t border-border/60 pt-4 text-xs text-muted-foreground">
          <p>
            © {new Date().getFullYear()} Technical Notes. Built with Next.js,
            Tailwind CSS, and shadcn/ui.
          </p>
        </div>
      </div>
    </footer>
  );
}
