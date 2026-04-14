import { HealthBadge } from '../../components/HealthBadge'

export default async function DashboardPage() {
  return (
    <div>
      <h1>Dashboard Template</h1>
      <p>Reusable analytics shell for any SaaS project.</p>
      <div style={{ marginTop: 16 }}>
        <HealthBadge />
      </div>
    </div>
  )
}
