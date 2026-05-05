"use client";

import type { ReactNode } from "react";

interface Column<T> {
  readonly key: keyof T;
  readonly label: string;
  readonly align?: "left" | "right" | "center";
  readonly render?: (value: T[keyof T], row: T) => ReactNode;
}

interface DataTableProps<T> {
  readonly columns: ReadonlyArray<Column<T>>;
  readonly data: ReadonlyArray<T>;
  readonly emptyMessage?: string;
}

export function DataTable<T extends { readonly id: string }>({
  columns,
  data,
  emptyMessage = "No data available",
}: DataTableProps<T>) {
  if (data.length === 0) {
    return (
      <div
        className="flex items-center justify-center rounded-xl border border-zinc-800 bg-zinc-900/50 px-6 py-12"
        role="status"
        aria-label={emptyMessage}
      >
        <p className="text-sm text-zinc-500">{emptyMessage}</p>
      </div>
    );
  }

  return (
    <div className="overflow-hidden rounded-xl border border-zinc-800 bg-zinc-900/50">
      <div className="overflow-x-auto">
        <table className="w-full" role="table">
          <thead>
            <tr className="border-b border-zinc-800">
              {columns.map((col) => (
                <th
                  key={String(col.key)}
                  scope="col"
                  className={`px-6 py-3 text-xs font-medium uppercase tracking-wider text-zinc-400 ${
                    col.align === "right" ? "text-right" : col.align === "center" ? "text-center" : "text-left"
                  }`}
                >
                  {col.label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-zinc-800/50">
            {data.map((row) => (
              <tr key={row.id} className="transition hover:bg-zinc-800/30">
                {columns.map((col) => (
                  <td
                    key={String(col.key)}
                    className={`px-6 py-4 text-sm ${
                      col.align === "right" ? "text-right" : col.align === "center" ? "text-center" : "text-left"
                    } text-zinc-300`}
                  >
                    {col.render ? col.render(row[col.key], row) : String(row[col.key] ?? "")}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export type { Column, DataTableProps };
