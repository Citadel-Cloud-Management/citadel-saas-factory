import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Citadel SaaS Factory',
  description: 'Universal Full-Stack SaaS Production Framework',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-gray-50 text-gray-900 min-h-screen">{children}</body>
    </html>
  )
}
