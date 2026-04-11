import Link from "next/link";

const collections = [
  { name: "AI / ML Toolkits", handle: "ai-ml-toolkits", count: 60, color: "bg-cyan" },
  { name: "Architecture Blueprints", handle: "architecture-blueprints", count: 80, color: "bg-orange" },
  { name: "Cybersecurity Frameworks", handle: "cybersecurity-frameworks", count: 40, color: "bg-red" },
  { name: "DevOps Pipelines", handle: "devops-pipelines", count: 40, color: "bg-yellow" },
  { name: "Career Development", handle: "career-development", count: 30, color: "bg-green" },
  { name: "Career Intelligence", handle: "career-intelligence", count: 20, color: "bg-purple" },
  { name: "Leadership & Management", handle: "leadership-management", count: 20, color: "bg-purple" },
  { name: "Multi-Industry AI", handle: "multi-industry-ai", count: 30, color: "bg-cyan" },
];

export default function ProductsPage() {
  return (
    <main className="min-h-screen bg-ink">
      <section className="py-20 text-center">
        <h1 className="font-syne text-4xl md:text-5xl font-bold bg-gradient-to-r from-white to-cyan bg-clip-text text-transparent mb-4">
          320+ Cloud Toolkits
        </h1>
        <p className="text-gray2 text-lg max-w-2xl mx-auto">
          Production-ready templates, blueprints, and frameworks built by enterprise practitioners.
        </p>
      </section>
      <section className="max-w-7xl mx-auto px-4 pb-20 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {collections.map((c) => (
          <Link
            key={c.handle}
            href={`/products?collection=${c.handle}`}
            className="bg-card border border-edge rounded-lg p-6 hover:border-edge2 hover:-translate-y-1 transition-all group"
          >
            <div className={`w-3 h-3 rounded-full ${c.color} mb-4`} />
            <h3 className="text-white text-lg font-semibold mb-2 group-hover:text-cyan transition-colors">
              {c.name}
            </h3>
            <p className="text-gray text-sm">{c.count}+ products</p>
          </Link>
        ))}
      </section>
    </main>
  );
}
