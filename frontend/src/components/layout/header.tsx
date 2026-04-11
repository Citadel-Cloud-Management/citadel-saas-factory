"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";

const navItems = [
  { label: "Courses", href: "/courses" },
  { label: "Products", href: "/products" },
  { label: "Pricing", href: "/pricing" },
  { label: "About", href: "/about" },
];

export function Header() {
  const pathname = usePathname();
  return (
    <header className="sticky top-0 z-50 backdrop-blur-xl bg-ink/85 border-b border-edge">
      <div className="max-w-7xl mx-auto px-4 flex items-center justify-between h-16">
        <Link href="/" className="flex items-center gap-2">
          <span className="w-8 h-8 bg-cyan rounded-md flex items-center justify-center text-ink font-bold text-sm">C</span>
          <span className="text-white font-semibold text-lg hidden sm:block">Citadel Cloud</span>
        </Link>
        <nav className="hidden md:flex items-center gap-6">
          {navItems.map((item) => (
            <Link key={item.href} href={item.href} className={`text-sm font-medium transition-colors ${pathname === item.href ? "text-cyan border-b-2 border-cyan pb-1" : "text-gray2 hover:text-white"}`}>
              {item.label}
            </Link>
          ))}
        </nav>
        <div className="flex items-center gap-3">
          <Link href="/login" className="text-sm text-gray2 hover:text-white transition-colors">Sign In</Link>
          <Link href="/register" className="bg-cyan text-ink px-4 py-2 rounded-md text-sm font-semibold hover:opacity-90 transition-opacity">Get Started</Link>
        </div>
      </div>
    </header>
  );
}
