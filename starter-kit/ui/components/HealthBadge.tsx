const apiBaseUrl =
  process.env.INTERNAL_API_BASE_URL ||
  process.env.NEXT_PUBLIC_API_BASE_URL ||
  'http://api:8000'

export async function HealthBadge() {
  let status = 'unknown'

  try {
    const res = await fetch(`${apiBaseUrl}/health`, { cache: 'no-store' })
    if (res.ok) {
      const data = await res.json()
      status = data.status
    }
  } catch {
    status = 'down'
  }

  return <span>API status: {status}</span>
}
