import Link from "next/link";

const navItems = [
  { label: "Dashboard", href: "/dashboard", icon: "📊" },
  { label: "Agents", href: "/dashboard/agents", icon: "🤖" },
  { label: "Models", href: "/dashboard/models", icon: "🧠" },
  { label: "Settings", href: "/dashboard/settings", icon: "⚙️" },
];

export default function DashboardLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <div className="flex min-h-screen">
      {/* Sidebar */}
      <aside className="flex w-64 flex-col border-r border-[var(--card-border)] bg-[var(--card)]">
        <div className="border-b border-[var(--card-border)] px-6 py-5">
          <Link href="/" className="text-lg font-bold tracking-tight text-white">
            Citadel
          </Link>
        </div>
        <nav className="flex-1 space-y-1 p-4">
          {navItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm text-[var(--muted)] transition hover:bg-[var(--background)] hover:text-white"
            >
              <span>{item.icon}</span>
              {item.label}
            </Link>
          ))}
        </nav>
        <div className="border-t border-[var(--card-border)] p-4">
          <Link
            href="/login"
            className="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm text-[var(--muted)] transition hover:text-white"
          >
            Sign Out
          </Link>
        </div>
      </aside>

      {/* Main content */}
      <main className="flex-1 overflow-y-auto">{children}</main>
    </div>
  );
}
