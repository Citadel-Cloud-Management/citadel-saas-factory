import Link from 'next/link'
import { StatCard } from '../components/StatCard'

export default function HomePage() {
  return (
    <div>
      <h1>Clone-and-run SaaS factory</h1>
      <p>Reusable starter template for any project.</p>
      <div style={{ display: 'flex', gap: 16, marginTop: 24, flexWrap: 'wrap' }}>
        <StatCard title="UI" value="Next.js" />
        <StatCard title="API" value="FastAPI" />
        <StatCard title="DB" value="Postgres" />
        <StatCard title="Observability" value="Prometheus + Grafana" />
      </div>
      <div style={{ marginTop: 24 }}>
        <Link href="/dashboard">Open dashboard</Link>
      </div>
    </div>
  )
}
