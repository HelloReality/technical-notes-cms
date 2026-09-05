import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Toaster } from "@/components/ui/toaster";
import { Toaster as SonnerToaster } from "@/components/ui/sonner";
import { ThemeProvider } from "@/components/theme-provider";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: {
    default: "Technical Notes — Knowledge Base",
    template: "%s | Technical Notes",
  },
  description:
    "A curated, searchable knowledge base of technical notes covering cybersecurity, development, DevOps, cloud, networking, databases, and system design.",
  keywords: [
    "technical notes",
    "knowledge base",
    "cybersecurity",
    "development",
    "devops",
    "cloud",
    "networking",
    "databases",
    "system design",
    "programming",
    "operating systems",
  ],
  authors: [{ name: "Technical Notes" }],
  openGraph: {
    type: "website",
    locale: "en_US",
    title: "Technical Notes — Knowledge Base",
    description:
      "A curated, searchable knowledge base of technical notes for engineers.",
    siteName: "Technical Notes",
  },
  twitter: {
    card: "summary_large_image",
    title: "Technical Notes — Knowledge Base",
    description:
      "A curated, searchable knowledge base of technical notes for engineers.",
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
    },
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased bg-background text-foreground`}
      >
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          {children}
          <Toaster />
          <SonnerToaster position="top-right" richColors />
        </ThemeProvider>
      </body>
    </html>
  );
}
