"use client";

interface KPICardProps {
  readonly title: string;
  readonly value: string;
  readonly change?: string;
  readonly trend?: "up" | "down" | "neutral";
  readonly subtitle?: string;
}

export function KPICard({ title, value, change, trend = "neutral", subtitle }: KPICardProps) {
  const trendColors = {
    up: "text-emerald-400",
    down: "text-red-400",
    neutral: "text-zinc-400",
  };

  const trendIcons = {
    up: "+",
    down: "-",
    neutral: "",
  };

  return (
    <div className="rounded-xl border border-zinc-800 bg-zinc-900/50 p-6 backdrop-blur-sm transition hover:border-zinc-700">
      <p className="text-sm font-medium text-zinc-400">{title}</p>
      <div className="mt-2 flex items-baseline gap-2">
        <p className="text-3xl font-bold tracking-tight text-white">{value}</p>
        {change && (
          <span className={`text-sm font-medium ${trendColors[trend]}`}>
            {trendIcons[trend]}{change}
          </span>
        )}
      </div>
      {subtitle && (
        <p className="mt-1 text-xs text-zinc-500">{subtitle}</p>
      )}
    </div>
  );
}
