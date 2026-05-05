import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { Providers } from "@/lib/providers";
import Analytics from "../components/analytics";
import CookieConsent from "../components/cookie-consent";
import "./globals.css";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });

export const metadata: Metadata = {
  title: "Citadel — AI-Native Fintech Platform",
  description:
    "Autonomous compliance intelligence, real-time transaction monitoring, and AI-powered KYC verification for financial services.",
  keywords: ["Fintech", "Compliance", "AML", "KYC", "AI Agents", "SaaS", "Payments"],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={inter.variable}>
      <body className="min-h-screen bg-zinc-950 font-sans text-white antialiased">
        <Providers>
          <Analytics />
          {children}
          <CookieConsent />
        </Providers>
      </body>
    </html>
  );
}
