import { Card } from "@/components/ui/card";

const stats = [
  { label: "Total Agents", value: "500+", change: "+12 this week" },
  { label: "Active Models", value: "12", change: "3 providers" },
  { label: "Security Score", value: "A+", change: "All checks passing" },
  { label: "Uptime", value: "99.9%", change: "Last 30 days" },
];

const recentActivity = [
  {
    id: 1,
    action: "Agent deployed",
    detail: "marketing/seo-analyst updated to v2.3",
    time: "2 minutes ago",
  },
  {
    id: 2,
    action: "Security scan passed",
    detail: "Trivy container scan — 0 vulnerabilities",
    time: "15 minutes ago",
  },
  {
    id: 3,
    action: "Model route changed",
    detail: "Switched data-analytics to Claude Haiku 4.5",
    time: "1 hour ago",
  },
  {
    id: 4,
    action: "Pipeline completed",
    detail: "CI/CD pipeline #1247 — all stages green",
    time: "3 hours ago",
  },
  {
    id: 5,
    action: "Wiki updated",
    detail: "LLM Wiki ingested 3 new source documents",
    time: "5 hours ago",
  },
];

export default function DashboardPage() {
  return (
    <div className="p-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white">Dashboard</h1>
        <p className="mt-1 text-[var(--muted)]">
          Welcome back. Here&apos;s your system overview.
        </p>
      </div>

      {/* Stats */}
      <div className="mb-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <Card key={stat.label}>
            <div className="p-6">
              <p className="text-sm text-[var(--muted)]">{stat.label}</p>
              <p className="mt-2 text-3xl font-bold text-white">{stat.value}</p>
              <p className="mt-1 text-xs text-[var(--muted)]">{stat.change}</p>
            </div>
          </Card>
        ))}
      </div>

      {/* Recent Activity */}
      <Card>
        <div className="border-b border-[var(--card-border)] px-6 py-4">
          <h2 className="text-lg font-semibold text-white">Recent Activity</h2>
        </div>
        <div className="divide-y divide-[var(--card-border)]">
          {recentActivity.map((item) => (
            <div key={item.id} className="flex items-center justify-between px-6 py-4">
              <div>
                <p className="text-sm font-medium text-white">{item.action}</p>
                <p className="text-sm text-[var(--muted)]">{item.detail}</p>
              </div>
              <span className="shrink-0 text-xs text-[var(--muted)]">
                {item.time}
              </span>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
