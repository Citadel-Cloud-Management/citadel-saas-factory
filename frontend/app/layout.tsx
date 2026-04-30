import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });

export const metadata: Metadata = {
  title: "Citadel SaaS Factory",
  description:
    "Universal Full-Stack SaaS Production Framework — 500+ Autonomous Business Agents across 30 Domains",
  keywords: ["SaaS", "AI Agents", "Enterprise", "Autonomous", "Multi-Model"],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={inter.variable}>
      <body className="min-h-screen bg-[var(--background)] font-sans antialiased">
        {children}
      </body>
    </html>
  );
}
