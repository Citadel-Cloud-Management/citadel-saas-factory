'use client'
import { useState } from 'react'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      const res = await fetch('/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      })
      if (!res.ok) {
        const data = await res.json()
        setError(data.detail || 'Login failed')
        return
      }
      const data = await res.json()
      localStorage.setItem('token', data.access_token)
      window.location.href = '/dashboard'
    } catch {
      setError('Network error')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center">
      <form onSubmit={handleSubmit} className="w-full max-w-sm space-y-4 p-8 bg-white rounded-xl shadow">
        <h1 className="text-2xl font-bold text-center">Sign In</h1>
        {error && <p className="text-red-500 text-sm text-center">{error}</p>}
        <input
          type="email" placeholder="Email" value={email}
          onChange={e => setEmail(e.target.value)} required
          className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-black"
        />
        <input
          type="password" placeholder="Password" value={password}
          onChange={e => setPassword(e.target.value)} required
          className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-black"
        />
        <button
          type="submit" disabled={loading}
          className="w-full py-2 bg-black text-white rounded-lg hover:bg-gray-800 disabled:opacity-50"
        >
          {loading ? 'Signing in...' : 'Sign In'}
        </button>
        <p className="text-sm text-center text-gray-500">
          No account? <a href="/register" className="text-black underline">Register</a>
        </p>
      </form>
    </div>
  )
}
