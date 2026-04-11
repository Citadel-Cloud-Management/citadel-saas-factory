export default function Home() {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center space-y-6 max-w-2xl px-4">
        <h1 className="text-5xl font-bold tracking-tight">Citadel SaaS Factory</h1>
        <p className="text-xl text-gray-600">
          Universal Full-Stack SaaS Production Framework
        </p>
        <div className="flex gap-4 justify-center">
          <a
            href="/login"
            className="px-6 py-3 bg-black text-white rounded-lg hover:bg-gray-800 transition"
          >
            Sign In
          </a>
          <a
            href="/register"
            className="px-6 py-3 border border-gray-300 rounded-lg hover:bg-gray-100 transition"
          >
            Get Started
          </a>
        </div>
        <div className="grid grid-cols-3 gap-4 mt-12 text-left">
          <div className="p-4 bg-white rounded-lg shadow-sm">
            <h3 className="font-semibold">265 AI Agents</h3>
            <p className="text-sm text-gray-500">Autonomous business operations</p>
          </div>
          <div className="p-4 bg-white rounded-lg shadow-sm">
            <h3 className="font-semibold">Multi-Tenant</h3>
            <p className="text-sm text-gray-500">Isolated data, shared infra</p>
          </div>
          <div className="p-4 bg-white rounded-lg shadow-sm">
            <h3 className="font-semibold">Production Ready</h3>
            <p className="text-sm text-gray-500">K8s, monitoring, security</p>
          </div>
        </div>
      </div>
    </div>
  )
}
