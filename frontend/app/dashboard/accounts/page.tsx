"use client";

import { useQuery } from "@tanstack/react-query";
import { KPICard } from "@/components/ui/kpi-card";
import { StatusBadge, autoVariant } from "@/components/ui/status-badge";
import { accountsApi, type Account } from "@/lib/fintech-api";

export default function AccountsPage() {
  const { data: accountsRes, isLoading } = useQuery({
    queryKey: ["accounts"],
    queryFn: () => accountsApi.list(),
  });

  const accounts = (accountsRes?.data ?? []) as Account[];

  const totalBalance = accounts.reduce((sum, a) => sum + parseFloat(a.balance || "0"), 0);
  const totalAvailable = accounts.reduce((sum, a) => sum + parseFloat(a.available_balance || "0"), 0);
  const activeCount = accounts.filter((a) => a.status === "active").length;

  return (
    <div className="p-8">
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Accounts</h1>
          <p className="mt-1 text-zinc-400">
            Manage your financial accounts and balances.
          </p>
        </div>
        <button className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-indigo-500">
          + New Account
        </button>
      </div>

      {/* KPIs */}
      <div className="mb-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <KPICard
          title="Total Balance"
          value={`$${totalBalance.toLocaleString("en-US", { minimumFractionDigits: 2 })}`}
          trend="up"
          subtitle="Across all accounts"
        />
        <KPICard
          title="Available"
          value={`$${totalAvailable.toLocaleString("en-US", { minimumFractionDigits: 2 })}`}
          subtitle="Ready to transact"
        />
        <KPICard
          title="Accounts"
          value={String(accounts.length)}
          change={`${activeCount} active`}
          trend="neutral"
        />
        <KPICard
          title="Currencies"
          value={String(new Set(accounts.map((a) => a.currency)).size)}
          subtitle="Multi-currency enabled"
        />
      </div>

      {/* Account Cards */}
      {isLoading ? (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-48 animate-pulse rounded-xl border border-zinc-800 bg-zinc-900/50" />
          ))}
        </div>
      ) : accounts.length === 0 ? (
        <div className="flex flex-col items-center justify-center rounded-xl border border-dashed border-zinc-700 bg-zinc-900/30 py-16">
          <p className="text-lg font-medium text-zinc-300">No accounts yet</p>
          <p className="mt-2 text-sm text-zinc-500">Create your first account to start transacting.</p>
          <button className="mt-6 rounded-lg bg-indigo-600 px-6 py-2 text-sm font-medium text-white transition hover:bg-indigo-500">
            Create Account
          </button>
        </div>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {accounts.map((account) => (
            <div
              key={account.id}
              className="rounded-xl border border-zinc-800 bg-zinc-900/50 p-6 transition hover:border-zinc-700"
            >
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-sm font-medium uppercase tracking-wide text-zinc-400">
                    {account.account_type}
                  </p>
                  <p className="mt-1 font-mono text-xs text-zinc-500">
                    {account.account_number}
                  </p>
                </div>
                <StatusBadge label={account.status} variant={autoVariant(account.status)} />
              </div>

              <div className="mt-6">
                <p className="text-2xl font-bold text-white">
                  ${parseFloat(account.balance).toLocaleString("en-US", { minimumFractionDigits: 2 })}
                </p>
                <p className="mt-1 text-xs text-zinc-500">
                  Available: ${parseFloat(account.available_balance).toLocaleString("en-US", { minimumFractionDigits: 2 })} {account.currency}
                </p>
              </div>

              <div className="mt-6 flex gap-2">
                <button className="flex-1 rounded-lg border border-zinc-700 px-3 py-1.5 text-xs font-medium text-zinc-300 transition hover:border-zinc-500">
                  Send
                </button>
                <button className="flex-1 rounded-lg border border-zinc-700 px-3 py-1.5 text-xs font-medium text-zinc-300 transition hover:border-zinc-500">
                  Receive
                </button>
                <button className="flex-1 rounded-lg border border-zinc-700 px-3 py-1.5 text-xs font-medium text-zinc-300 transition hover:border-zinc-500">
                  Details
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
