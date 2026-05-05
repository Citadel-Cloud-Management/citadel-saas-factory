import Link from "next/link";

const navItems = [
  { label: "Overview", href: "/dashboard", icon: "O" },
  { label: "Accounts", href: "/dashboard/accounts", icon: "A" },
  { label: "Transactions", href: "/dashboard/transactions", icon: "T" },
  { label: "Compliance", href: "/dashboard/compliance", icon: "C" },
  { label: "Agents", href: "/dashboard/agents", icon: "G" },
  { label: "Models", href: "/dashboard/models", icon: "M" },
  { label: "Settings", href: "/dashboard/settings", icon: "S" },
];

export default function DashboardLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <div className="flex min-h-screen bg-zinc-950">
      {/* Sidebar */}
      <aside className="flex w-64 flex-col border-r border-zinc-800 bg-zinc-900/50">
        <div className="border-b border-zinc-800 px-6 py-5">
          <Link href="/" className="text-lg font-bold tracking-tight text-white">
            Citadel
          </Link>
          <p className="mt-0.5 text-[10px] uppercase tracking-widest text-zinc-500">
            Fintech Platform
          </p>
        </div>
        <nav className="flex-1 space-y-0.5 p-3">
          {navItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm text-zinc-400 transition hover:bg-zinc-800/50 hover:text-white"
            >
              <span className="flex h-6 w-6 items-center justify-center rounded-md bg-zinc-800 text-[10px] font-bold text-zinc-400">
                {item.icon}
              </span>
              {item.label}
            </Link>
          ))}
        </nav>

        {/* System Status */}
        <div className="border-t border-zinc-800 p-4">
          <div className="rounded-lg bg-zinc-800/30 p-3">
            <div className="flex items-center gap-2">
              <div className="h-2 w-2 rounded-full bg-emerald-400" />
              <span className="text-xs font-medium text-zinc-300">All Systems Operational</span>
            </div>
            <p className="mt-1 text-[10px] text-zinc-500">500+ agents active</p>
          </div>
        </div>

        <div className="border-t border-zinc-800 p-4">
          <Link
            href="/login"
            className="flex items-center gap-3 rounded-lg px-3 py-2 text-sm text-zinc-500 transition hover:text-white"
          >
            Sign Out
          </Link>
        </div>
      </aside>

      {/* Main content */}
      <main className="flex-1 overflow-y-auto bg-zinc-950">{children}</main>
    </div>
  );
}
