'use client'
import { useState } from 'react'

export default function RegisterPage() {
  const [form, setForm] = useState({ email: '', password: '', full_name: '', tenant_name: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      const res = await fetch('/api/v1/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      })
      if (!res.ok) {
        const data = await res.json()
        setError(data.detail || 'Registration failed')
        return
      }
      window.location.href = '/login'
    } catch {
      setError('Network error')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center">
      <form onSubmit={handleSubmit} className="w-full max-w-sm space-y-4 p-8 bg-white rounded-xl shadow">
        <h1 className="text-2xl font-bold text-center">Create Account</h1>
        {error && <p className="text-red-500 text-sm text-center">{error}</p>}
        <input
          type="text" placeholder="Full Name" value={form.full_name}
          onChange={e => setForm({ ...form, full_name: e.target.value })}
          className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-black"
        />
        <input
          type="email" placeholder="Email" value={form.email}
          onChange={e => setForm({ ...form, email: e.target.value })} required
          className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-black"
        />
        <input
          type="password" placeholder="Password" value={form.password}
          onChange={e => setForm({ ...form, password: e.target.value })} required
          className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-black"
        />
        <input
          type="text" placeholder="Organization Name" value={form.tenant_name}
          onChange={e => setForm({ ...form, tenant_name: e.target.value })}
          className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-black"
        />
        <button
          type="submit" disabled={loading}
          className="w-full py-2 bg-black text-white rounded-lg hover:bg-gray-800 disabled:opacity-50"
        >
          {loading ? 'Creating...' : 'Create Account'}
        </button>
        <p className="text-sm text-center text-gray-500">
          Have an account? <a href="/login" className="text-black underline">Sign in</a>
        </p>
      </form>
    </div>
  )
}
