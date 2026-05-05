"use client";

import { useQuery } from "@tanstack/react-query";
import { DataTable } from "@/components/ui/data-table";
import { StatusBadge, autoVariant } from "@/components/ui/status-badge";
import { KPICard } from "@/components/ui/kpi-card";
import { transactionsApi, type Transaction } from "@/lib/fintech-api";

export default function TransactionsPage() {
  const { data: txnRes, isLoading } = useQuery({
    queryKey: ["transactions", 1],
    queryFn: () => transactionsApi.list(1, 50),
  });

  const transactions = (txnRes?.data ?? []) as Transaction[];

  const totalVolume = transactions
    .filter((t) => t.status === "completed")
    .reduce((sum, t) => sum + parseFloat(t.amount), 0);

  const completedCount = transactions.filter((t) => t.status === "completed").length;
  const failedCount = transactions.filter((t) => t.status === "failed").length;
  const successRate = transactions.length > 0
    ? ((completedCount / transactions.length) * 100).toFixed(1)
    : "0";

  const columns = [
    {
      key: "reference_id" as keyof Transaction,
      label: "Reference",
      render: (val: unknown) => (
        <span className="font-mono text-xs text-zinc-300">{String(val)}</span>
      ),
    },
    {
      key: "transaction_type" as keyof Transaction,
      label: "Type",
      render: (val: unknown) => (
        <span className="capitalize">{String(val)}</span>
      ),
    },
    {
      key: "amount" as keyof Transaction,
      label: "Amount",
      align: "right" as const,
      render: (val: unknown, row: Transaction) => (
        <span className="font-medium text-white">
          ${parseFloat(String(val)).toLocaleString("en-US", { minimumFractionDigits: 2 })}
          <span className="ml-1 text-xs text-zinc-500">{row.currency}</span>
        </span>
      ),
    },
    {
      key: "status" as keyof Transaction,
      label: "Status",
      render: (val: unknown) => (
        <StatusBadge label={String(val)} variant={autoVariant(String(val))} />
      ),
    },
    {
      key: "created_at" as keyof Transaction,
      label: "Date",
      render: (val: unknown) => (
        <span className="text-xs text-zinc-400">
          {new Date(String(val)).toLocaleDateString("en-US", {
            month: "short", day: "numeric", hour: "2-digit", minute: "2-digit",
          })}
        </span>
      ),
    },
  ];

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white">Transactions</h1>
        <p className="mt-1 text-zinc-400">
          Real-time transaction monitoring with compliance screening.
        </p>
      </div>

      {/* KPIs */}
      <div className="mb-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <KPICard
          title="Total Volume"
          value={`$${totalVolume.toLocaleString("en-US", { minimumFractionDigits: 2 })}`}
          subtitle="All completed transactions"
        />
        <KPICard
          title="Transactions"
          value={String(transactions.length)}
          subtitle="This period"
        />
        <KPICard
          title="Success Rate"
          value={`${successRate}%`}
          trend={parseFloat(successRate) > 95 ? "up" : "down"}
          change={failedCount > 0 ? `${failedCount} failed` : "All passing"}
        />
        <KPICard
          title="Avg. Amount"
          value={transactions.length > 0
            ? `$${(totalVolume / Math.max(completedCount, 1)).toFixed(2)}`
            : "$0"
          }
          subtitle="Per transaction"
        />
      </div>

      {/* Transaction Table */}
      {isLoading ? (
        <div className="flex items-center justify-center rounded-xl border border-zinc-800 bg-zinc-900/50 py-20">
          <div className="text-sm text-zinc-500">Loading transactions...</div>
        </div>
      ) : (
        <DataTable
          columns={columns}
          data={transactions}
          emptyMessage="No transactions yet. Make your first transfer to get started."
        />
      )}
    </div>
  );
}
