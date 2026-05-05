"use client";

interface Column<T> {
  readonly key: keyof T;
  readonly label: string;
  readonly align?: "left" | "right" | "center";
  readonly render?: (value: T[keyof T], row: T) => React.ReactNode;
}

interface DataTableProps<T> {
  readonly columns: Column<T>[];
  readonly data: T[];
  readonly emptyMessage?: string;
}

export function DataTable<T extends { id: string }>({
  columns,
  data,
  emptyMessage = "No data available",
}: DataTableProps<T>) {
  if (data.length === 0) {
    return (
      <div className="flex items-center justify-center rounded-xl border border-zinc-800 bg-zinc-900/50 px-6 py-12">
        <p className="text-sm text-zinc-500">{emptyMessage}</p>
      </div>
    );
  }

  return (
    <div className="overflow-hidden rounded-xl border border-zinc-800 bg-zinc-900/50">
      <table className="w-full">
        <thead>
          <tr className="border-b border-zinc-800">
            {columns.map((col) => (
              <th
                key={String(col.key)}
                className={`px-6 py-3 text-xs font-medium uppercase tracking-wider text-zinc-400 ${
                  col.align === "right" ? "text-right" : "text-left"
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
                    col.align === "right" ? "text-right" : "text-left"
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
  );
}
