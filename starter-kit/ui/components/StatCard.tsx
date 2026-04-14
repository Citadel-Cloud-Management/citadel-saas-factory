export function StatCard({ title, value }: { title: string; value: string }) {
  return (
    <div style={{ border: '1px solid #1f2937', borderRadius: 12, padding: 16, minWidth: 200 }}>
      <div style={{ color: '#9ca3af', fontSize: 14 }}>{title}</div>
      <div style={{ fontSize: 28, fontWeight: 700, marginTop: 8 }}>{value}</div>
    </div>
  )
}
