"use client";

import { useQuery } from "@tanstack/react-query";
import { Card } from "@/components/ui/card";
import { accountsApi, transactionsApi, kycApi } from "@/lib/fintech-api";

export default function DashboardPage() {
  const {
    data: accountsRes,
    isLoading: accountsLoading,
    isError: accountsError,
  } = useQuery({
    queryKey: ["accounts"],
    queryFn: () => accountsApi.list(),
  });

  const {
    data: txnRes,
    isLoading: txnLoading,
  } = useQuery({
    queryKey: ["transactions", "recent"],
    queryFn: () => transactionsApi.list(1, 5),
  });

  const { data: kycRes } = useQuery({
    queryKey: ["kyc-status"],
    queryFn: () => kycApi.status(),
  });

  const accounts = accountsRes?.data ?? [];
  const transactions = txnRes?.data ?? [];
  const kycStatus = kycRes?.data;

  const totalBalance = accounts.reduce(
    (sum, a) => sum + parseFloat(a.balance || "0"),
    0,
  );

  const stats = [
    {
      label: "Total Balance",
      value: `$${totalBalance.toLocaleString("en-US", { minimumFractionDigits: 2 })}`,
      change: `${accounts.length} account${accounts.length !== 1 ? "s" : ""}`,
    },
    {
      label: "KYC Status",
      value: kycStatus?.verification_level?.toUpperCase() ?? "NONE",
      change: kycStatus?.status ?? "pending",
    },
    {
      label: "Transactions",
      value: String(transactions.length),
      change: "Last 5 shown",
    },
    {
      label: "Risk Score",
      value: kycStatus?.risk_score != null ? `${kycStatus.risk_score}/100` : "N/A",
      change: (kycStatus?.risk_score ?? 0) < 30 ? "Low risk" : "Review needed",
    },
  ];

  const isLoading = accountsLoading || txnLoading;

  return (
    <main className="p-8" aria-label="Dashboard overview">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white">Dashboard</h1>
        <p className="mt-1 text-[var(--muted)]">
          Your financial overview at a glance.
        </p>
      </div>

      {/* Error state */}
      {accountsError && (
        <div
          role="alert"
          className="mb-6 rounded-lg border border-red-800/30 bg-red-900/10 p-4 text-sm text-red-400"
        >
          Failed to load account data. Please try again later.
        </div>
      )}

      {/* Stats */}
      <section aria-label="Key metrics" className="mb-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {isLoading
          ? Array.from({ length: 4 }).map((_, i) => (
              <Card key={i}>
                <div className="animate-pulse p-6">
                  <div className="h-4 w-24 rounded bg-zinc-800" />
                  <div className="mt-4 h-8 w-32 rounded bg-zinc-800" />
                  <div className="mt-2 h-3 w-16 rounded bg-zinc-800" />
                </div>
              </Card>
            ))
          : stats.map((stat) => (
              <Card key={stat.label}>
                <div className="p-6">
                  <p className="text-sm text-[var(--muted)]">{stat.label}</p>
                  <p className="mt-2 text-3xl font-bold text-white">{stat.value}</p>
                  <p className="mt-1 text-xs text-[var(--muted)]">{stat.change}</p>
                </div>
              </Card>
            ))}
      </section>

      {/* Accounts */}
      <section aria-label="Accounts summary" className="mb-8">
        <Card>
          <div className="border-b border-[var(--card-border)] px-6 py-4">
            <h2 className="text-lg font-semibold text-white">Accounts</h2>
          </div>
          <div className="divide-y divide-[var(--card-border)]">
            {accounts.length === 0 ? (
              <div className="px-6 py-8 text-center text-[var(--muted)]">
                No accounts yet. Create your first account to get started.
              </div>
            ) : (
              accounts.map((account) => (
                <div key={account.id} className="flex items-center justify-between px-6 py-4">
                  <div>
                    <p className="text-sm font-medium text-white">
                      {account.account_type.toUpperCase()} — {account.currency}
                    </p>
                    <p className="text-xs text-[var(--muted)]">{account.account_number}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-bold text-white">
                      ${parseFloat(account.balance).toLocaleString("en-US", { minimumFractionDigits: 2 })}
                    </p>
                    <span
                      className={`text-xs ${account.status === "active" ? "text-green-400" : "text-yellow-400"}`}
                      aria-label={`Account status: ${account.status}`}
                    >
                      {account.status}
                    </span>
                  </div>
                </div>
              ))
            )}
          </div>
        </Card>
      </section>

      {/* Recent Transactions */}
      <section aria-label="Recent transactions">
        <Card>
          <div className="border-b border-[var(--card-border)] px-6 py-4">
            <h2 className="text-lg font-semibold text-white">Recent Transactions</h2>
          </div>
          <div className="divide-y divide-[var(--card-border)]">
            {transactions.length === 0 ? (
              <div className="px-6 py-8 text-center text-[var(--muted)]">
                No transactions yet.
              </div>
            ) : (
              transactions.map((txn) => (
                <div key={txn.id} className="flex items-center justify-between px-6 py-4">
                  <div>
                    <p className="text-sm font-medium text-white">
                      {txn.transaction_type.toUpperCase()}
                    </p>
                    <p className="text-xs text-[var(--muted)]">
                      {txn.description ?? txn.reference_id}
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-bold text-white">
                      ${parseFloat(txn.amount).toLocaleString("en-US", { minimumFractionDigits: 2 })}
                    </p>
                    <span
                      className={`text-xs ${
                        txn.status === "completed" ? "text-green-400" :
                        txn.status === "failed" ? "text-red-400" : "text-yellow-400"
                      }`}
                      aria-label={`Transaction status: ${txn.status}`}
                    >
                      {txn.status}
                    </span>
                  </div>
                </div>
              ))
            )}
          </div>
        </Card>
      </section>
    </main>
  );
}
