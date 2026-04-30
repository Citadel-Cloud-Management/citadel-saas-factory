import Link from "next/link";
import { Card } from "@/components/ui/card";

interface AgentDomain {
  readonly name: string;
  readonly slug: string;
  readonly count: number;
  readonly icon: string;
}

const domains: readonly AgentDomain[] = [
  { name: "Executive & Strategy", slug: "executive", count: 18, icon: "C" },
  { name: "Marketing & Growth", slug: "marketing", count: 28, icon: "M" },
  { name: "Sales & Revenue", slug: "sales", count: 24, icon: "S" },
  { name: "Customer Success", slug: "customer-success", count: 20, icon: "CS" },
  { name: "Product & UI/UX", slug: "product-design", count: 26, icon: "P" },
  { name: "Engineering", slug: "engineering", count: 35, icon: "E" },
  { name: "Frontend", slug: "frontend", count: 24, icon: "FE" },
  { name: "DevOps", slug: "devops", count: 34, icon: "DO" },
  { name: "Security", slug: "security", count: 28, icon: "Sc" },
  { name: "Data & Analytics", slug: "data-analytics", count: 24, icon: "DA" },
  { name: "QA & Testing", slug: "qa-testing", count: 28, icon: "QA" },
  { name: "HR & People", slug: "hr-people", count: 16, icon: "HR" },
  { name: "Finance & Billing", slug: "finance", count: 20, icon: "Fi" },
  { name: "Legal & Governance", slug: "legal", count: 14, icon: "Le" },
  { name: "Content & Comms", slug: "content", count: 16, icon: "Co" },
];

const totalAgents = domains.reduce((sum, d) => sum + d.count, 0);

export default function AgentsPage() {
  return (
    <div className="p-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white">Agent Browser</h1>
        <p className="mt-1 text-[var(--muted)]">
          {totalAgents} agents across {domains.length} domains.
        </p>
      </div>

      {/* Search bar (visual placeholder — static in server component) */}
      <div className="mb-6">
        <input
          type="text"
          placeholder="Search domains..."
          readOnly
          className="w-full max-w-md rounded-lg border border-[var(--card-border)] bg-[var(--background)] px-4 py-2.5 text-sm text-[var(--foreground)] placeholder:text-[var(--muted)] focus:outline-none focus:ring-2 focus:ring-[var(--accent)]"
        />
      </div>

      {/* Domain Grid */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {domains.map((domain) => (
          <Link
            key={domain.slug}
            href={`/dashboard/agents/${domain.slug}`}
          >
            <Card className="transition hover:border-[var(--accent)]">
              <div className="flex items-center gap-4 p-6">
                <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-lg bg-[var(--accent)]/10 text-sm font-bold text-[var(--accent)]">
                  {domain.icon}
                </div>
                <div className="min-w-0">
                  <p className="truncate text-sm font-medium text-white">
                    {domain.name}
                  </p>
                  <p className="text-xs text-[var(--muted)]">
                    {domain.count} agents
                  </p>
                </div>
              </div>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
