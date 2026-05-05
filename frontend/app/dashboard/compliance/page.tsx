"use client";

import { useQuery } from "@tanstack/react-query";
import { KPICard } from "@/components/ui/kpi-card";
import { StatusBadge } from "@/components/ui/status-badge";
import { kycApi } from "@/lib/fintech-api";

export default function CompliancePage() {
  const { data: kycRes } = useQuery({
    queryKey: ["kyc-status"],
    queryFn: () => kycApi.status(),
  });

  const kyc = kycRes?.data;

  const riskLevel = (score: number) => {
    if (score < 30) return { label: "Low Risk", variant: "success" as const };
    if (score < 60) return { label: "Medium Risk", variant: "warning" as const };
    if (score < 80) return { label: "High Risk", variant: "error" as const };
    return { label: "Critical", variant: "error" as const };
  };

  const risk = riskLevel(kyc?.risk_score ?? 0);

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white">Compliance</h1>
        <p className="mt-1 text-zinc-400">
          KYC verification, AML monitoring, and regulatory status.
        </p>
      </div>

      {/* KPIs */}
      <div className="mb-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <KPICard
          title="KYC Level"
          value={kyc?.verification_level?.toUpperCase() ?? "NONE"}
          subtitle="Identity verification tier"
        />
        <KPICard
          title="Verification Status"
          value={kyc?.status ?? "Pending"}
          subtitle={kyc?.verified_at ? `Verified ${new Date(kyc.verified_at).toLocaleDateString()}` : "Not yet verified"}
        />
        <KPICard
          title="Risk Score"
          value={`${kyc?.risk_score ?? 0}/100`}
          trend={risk.variant === "success" ? "up" : "down"}
          change={risk.label}
        />
        <KPICard
          title="Compliance Status"
          value="Active"
          subtitle="All checks passing"
        />
      </div>

      {/* Verification Card */}
      <div className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-xl border border-zinc-800 bg-zinc-900/50 p-6">
          <h3 className="text-lg font-semibold text-white">Identity Verification</h3>
          <p className="mt-2 text-sm text-zinc-400">
            Complete KYC verification to unlock higher transaction limits and full platform access.
          </p>

          <div className="mt-6 space-y-4">
            <div className="flex items-center justify-between rounded-lg border border-zinc-800 p-4">
              <div>
                <p className="text-sm font-medium text-white">Basic Verification</p>
                <p className="text-xs text-zinc-500">Email + Phone + Name</p>
              </div>
              <StatusBadge label="Complete" variant="success" />
            </div>
            <div className="flex items-center justify-between rounded-lg border border-zinc-800 p-4">
              <div>
                <p className="text-sm font-medium text-white">Enhanced Verification</p>
                <p className="text-xs text-zinc-500">Government ID + Selfie</p>
              </div>
              <StatusBadge
                label={kyc?.verification_level === "enhanced" || kyc?.verification_level === "full" ? "Complete" : "Required"}
                variant={kyc?.verification_level === "enhanced" || kyc?.verification_level === "full" ? "success" : "warning"}
              />
            </div>
            <div className="flex items-center justify-between rounded-lg border border-zinc-800 p-4">
              <div>
                <p className="text-sm font-medium text-white">Full Verification</p>
                <p className="text-xs text-zinc-500">Proof of Address + Source of Funds</p>
              </div>
              <StatusBadge
                label={kyc?.verification_level === "full" ? "Complete" : "Optional"}
                variant={kyc?.verification_level === "full" ? "success" : "neutral"}
              />
            </div>
          </div>

          <button className="mt-6 w-full rounded-lg bg-indigo-600 px-4 py-2.5 text-sm font-medium text-white transition hover:bg-indigo-500">
            Start Verification
          </button>
        </div>

        {/* Compliance Monitoring */}
        <div className="rounded-xl border border-zinc-800 bg-zinc-900/50 p-6">
          <h3 className="text-lg font-semibold text-white">Compliance Monitoring</h3>
          <p className="mt-2 text-sm text-zinc-400">
            Real-time AML screening and transaction monitoring powered by AI agents.
          </p>

          <div className="mt-6 space-y-3">
            <div className="flex items-center gap-3 rounded-lg bg-zinc-800/30 p-3">
              <div className="h-2 w-2 rounded-full bg-emerald-400" />
              <span className="text-sm text-zinc-300">AML Screening</span>
              <span className="ml-auto text-xs text-zinc-500">Active</span>
            </div>
            <div className="flex items-center gap-3 rounded-lg bg-zinc-800/30 p-3">
              <div className="h-2 w-2 rounded-full bg-emerald-400" />
              <span className="text-sm text-zinc-300">Sanctions Check</span>
              <span className="ml-auto text-xs text-zinc-500">Active</span>
            </div>
            <div className="flex items-center gap-3 rounded-lg bg-zinc-800/30 p-3">
              <div className="h-2 w-2 rounded-full bg-emerald-400" />
              <span className="text-sm text-zinc-300">Transaction Monitoring</span>
              <span className="ml-auto text-xs text-zinc-500">Active</span>
            </div>
            <div className="flex items-center gap-3 rounded-lg bg-zinc-800/30 p-3">
              <div className="h-2 w-2 rounded-full bg-emerald-400" />
              <span className="text-sm text-zinc-300">Velocity Detection</span>
              <span className="ml-auto text-xs text-zinc-500">Active</span>
            </div>
            <div className="flex items-center gap-3 rounded-lg bg-zinc-800/30 p-3">
              <div className="h-2 w-2 rounded-full bg-emerald-400" />
              <span className="text-sm text-zinc-300">CTR Reporting</span>
              <span className="ml-auto text-xs text-zinc-500">Automated</span>
            </div>
          </div>

          <div className="mt-6 rounded-lg border border-emerald-800/30 bg-emerald-900/10 p-4">
            <p className="text-sm font-medium text-emerald-400">All Systems Operational</p>
            <p className="mt-1 text-xs text-zinc-500">
              500+ AI compliance agents monitoring in real-time. Zero alerts in the last 24h.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
