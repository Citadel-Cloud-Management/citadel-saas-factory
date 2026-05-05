"use client";

type BadgeVariant = "success" | "warning" | "error" | "info" | "neutral";

interface StatusBadgeProps {
  readonly label: string;
  readonly variant?: BadgeVariant;
}

const variantStyles: Record<BadgeVariant, string> = {
  success: "bg-emerald-400/10 text-emerald-400 border-emerald-400/20",
  warning: "bg-amber-400/10 text-amber-400 border-amber-400/20",
  error: "bg-red-400/10 text-red-400 border-red-400/20",
  info: "bg-blue-400/10 text-blue-400 border-blue-400/20",
  neutral: "bg-zinc-400/10 text-zinc-400 border-zinc-400/20",
};

export function StatusBadge({ label, variant = "neutral" }: StatusBadgeProps) {
  return (
    <span
      className={`inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-medium ${variantStyles[variant]}`}
    >
      {label}
    </span>
  );
}

/** Map common statuses to badge variants automatically */
export function autoVariant(status: string): BadgeVariant {
  const map: Record<string, BadgeVariant> = {
    active: "success",
    completed: "success",
    approved: "success",
    verified: "success",
    pending: "warning",
    processing: "warning",
    in_review: "warning",
    frozen: "warning",
    failed: "error",
    rejected: "error",
    cancelled: "error",
    reversed: "error",
    closed: "neutral",
    expired: "neutral",
  };
  return map[status.toLowerCase()] ?? "neutral";
}
