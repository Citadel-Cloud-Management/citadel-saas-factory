import Link from "next/link";
import { Card } from "@/components/ui/card";

interface Agent {
  readonly id: string;
  readonly name: string;
  readonly description: string;
  readonly model: "opus" | "sonnet" | "haiku";
}

interface DomainInfo {
  readonly label: string;
  readonly agents: readonly Agent[];
}

const MODEL_BADGES: Record<string, { label: string; color: string }> = {
  opus: { label: "Opus 4.7", color: "bg-purple-600" },
  sonnet: { label: "Sonnet 4.6", color: "bg-blue-600" },
  haiku: { label: "Haiku 4.5", color: "bg-teal-600" },
};

const domainData: Record<string, DomainInfo> = {
  executive: {
    label: "Executive & Strategy",
    agents: [
      { id: "ceo-strategist", name: "CEO Strategist", description: "Strategic planning, OKR alignment, and board preparation", model: "opus" },
      { id: "cto-advisor", name: "CTO Advisor", description: "Technology strategy, architecture decisions, and engineering culture", model: "opus" },
      { id: "cfo-advisor", name: "CFO Advisor", description: "Financial modeling, runway analysis, and investor reporting", model: "sonnet" },
      { id: "okr-tracker", name: "OKR Tracker", description: "Objective tracking, key result measurement, and alignment checks", model: "haiku" },
    ],
  },
  engineering: {
    label: "Engineering",
    agents: [
      { id: "api-designer", name: "API Designer", description: "RESTful API design, OpenAPI specs, and versioning strategy", model: "sonnet" },
      { id: "code-reviewer", name: "Code Reviewer", description: "Automated code review with security and quality checks", model: "sonnet" },
      { id: "db-architect", name: "Database Architect", description: "Schema design, migration planning, and query optimization", model: "sonnet" },
      { id: "tdd-guide", name: "TDD Guide", description: "Test-driven development coaching and test generation", model: "haiku" },
    ],
  },
  security: {
    label: "Security",
    agents: [
      { id: "security-auditor", name: "Security Auditor", description: "Vulnerability scanning, SAST/DAST, and compliance checks", model: "opus" },
      { id: "threat-modeler", name: "Threat Modeler", description: "STRIDE analysis, attack surface mapping, and risk assessment", model: "sonnet" },
      { id: "incident-responder", name: "Incident Responder", description: "Security incident triage, containment, and remediation", model: "sonnet" },
    ],
  },
};

function getFallbackDomain(slug: string): DomainInfo {
  const label = slug
    .split("-")
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(" ");

  return {
    label,
    agents: [
      { id: `${slug}-lead`, name: `${label} Lead`, description: `Lead agent for the ${label} domain`, model: "sonnet" },
      { id: `${slug}-analyst`, name: `${label} Analyst`, description: `Analysis and reporting for ${label}`, model: "haiku" },
    ],
  };
}

export default async function AgentDomainPage({
  params,
}: {
  readonly params: Promise<{ domain: string }>;
}) {
  const { domain } = await params;
  const info = domainData[domain] ?? getFallbackDomain(domain);

  return (
    <div className="p-8">
      {/* Back + Header */}
      <div className="mb-8">
        <Link
          href="/dashboard/agents"
          className="mb-4 inline-flex items-center gap-1 text-sm text-[var(--muted)] transition hover:text-white"
        >
          &larr; Back to Agents
        </Link>
        <h1 className="text-3xl font-bold text-white">{info.label}</h1>
        <p className="mt-1 text-[var(--muted)]">
          {info.agents.length} agents in this domain.
        </p>
      </div>

      {/* Agent List */}
      <Card>
        <div className="divide-y divide-[var(--card-border)]">
          {info.agents.map((agent) => {
            const badge = MODEL_BADGES[agent.model];
            return (
              <div
                key={agent.id}
                className="flex items-center justify-between px-6 py-4"
              >
                <div className="min-w-0">
                  <p className="text-sm font-medium text-white">
                    {agent.name}
                  </p>
                  <p className="truncate text-sm text-[var(--muted)]">
                    {agent.description}
                  </p>
                </div>
                <span
                  className={`ml-4 shrink-0 rounded-full px-3 py-1 text-xs font-medium text-white ${badge.color}`}
                >
                  {badge.label}
                </span>
              </div>
            );
          })}
        </div>
      </Card>
    </div>
  );
}
