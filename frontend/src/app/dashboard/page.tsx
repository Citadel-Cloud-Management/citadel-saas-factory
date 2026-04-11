'use client'
import { useEffect, useState } from 'react'

interface UserData {
  email: string
  full_name: string
  role: string
}

const NAV = ['Home', 'Orders', 'Products', 'Customers', 'Marketing', 'Discounts', 'Content', 'Markets', 'Finance', 'Analytics']

export default function DashboardPage() {
  const [user, setUser] = useState<UserData | null>(null)
  const [active, setActive] = useState('Home')

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) { window.location.href = '/login'; return }
    fetch('/api/v1/users/me', {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then(r => r.ok ? r.json() : Promise.reject())
      .then(setUser)
      .catch(() => { localStorage.removeItem('token'); window.location.href = '/login' })
  }, [])

  if (!user) return <div className="min-h-screen flex items-center justify-center">Loading...</div>

  return (
    <div className="flex min-h-screen">
      {/* Sidebar */}
      <aside className="w-56 bg-gray-900 text-white p-4 space-y-1">
        <h2 className="text-lg font-bold mb-6 px-3">Citadel</h2>
        {NAV.map(item => (
          <button
            key={item}
            onClick={() => setActive(item)}
            className={`w-full text-left px-3 py-2 rounded-lg text-sm transition ${
              active === item ? 'bg-gray-700 text-white' : 'text-gray-400 hover:text-white hover:bg-gray-800'
            }`}
          >
            {item}
          </button>
        ))}
        <div className="pt-8 px-3 text-xs text-gray-500">
          {user.email}
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-2xl font-bold">{active}</h1>
          <button
            onClick={() => { localStorage.removeItem('token'); window.location.href = '/login' }}
            className="text-sm text-gray-500 hover:text-gray-900"
          >
            Sign Out
          </button>
        </div>

        {active === 'Home' && (
          <div className="grid grid-cols-4 gap-4">
            <div className="p-6 bg-white rounded-xl shadow-sm">
              <p className="text-sm text-gray-500">Total Revenue</p>
              <p className="text-3xl font-bold mt-1">$0.00</p>
            </div>
            <div className="p-6 bg-white rounded-xl shadow-sm">
              <p className="text-sm text-gray-500">Orders</p>
              <p className="text-3xl font-bold mt-1">0</p>
            </div>
            <div className="p-6 bg-white rounded-xl shadow-sm">
              <p className="text-sm text-gray-500">Customers</p>
              <p className="text-3xl font-bold mt-1">0</p>
            </div>
            <div className="p-6 bg-white rounded-xl shadow-sm">
              <p className="text-sm text-gray-500">Products</p>
              <p className="text-3xl font-bold mt-1">0</p>
            </div>
          </div>
        )}

        {active !== 'Home' && (
          <div className="bg-white rounded-xl shadow-sm p-12 text-center text-gray-400">
            <p className="text-lg">{active}</p>
            <p className="text-sm mt-2">Coming soon</p>
          </div>
        )}
      </main>
    </div>
  )
}
