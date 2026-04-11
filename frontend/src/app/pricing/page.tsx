const tiers = [
  {
    name: "Free", price: "$0", period: "forever", highlight: false,
    features: ["17 free courses", "Community access", "6 skill tracks", "Free resources"],
    cta: "Start Free", href: "/register",
  },
  {
    name: "Starter", price: "$29", period: "/month", highlight: false,
    features: ["Individual toolkits", "Basic support", "Curated resources", "Email support"],
    cta: "Get Starter", href: "https://buy.stripe.com/fZu9AU7VD1OydmVfTS0co03",
  },
  {
    name: "Professional", price: "$79", period: "/month", highlight: true,
    features: ["Full catalog (320+)", "Priority support", "All courses + tracks", "New releases first"],
    cta: "Go Professional", href: "https://buy.stripe.com/fZueVe5NvgJs4Qp3760co04",
  },
  {
    name: "Enterprise", price: "$297", period: "/month", highlight: false,
    features: ["Team licenses", "Custom content", "Dedicated support", "SLA-backed"],
    cta: "Contact Sales", href: "https://buy.stripe.com/eVqdRa0tb1Oy96F4ba0co05",
  },
];

export default function PricingPage() {
  return (
    <main className="min-h-screen bg-ink py-20">
      <div className="text-center mb-16">
        <h1 className="font-syne text-4xl md:text-5xl font-bold bg-gradient-to-r from-white to-cyan bg-clip-text text-transparent mb-4">
          Simple, Transparent Pricing
        </h1>
        <p className="text-gray2 text-lg">Start free. Scale when you are ready.</p>
      </div>
      <div className="max-w-6xl mx-auto px-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {tiers.map((tier) => (
          <div
            key={tier.name}
            className={`bg-card rounded-lg p-8 flex flex-col ${
              tier.highlight ? "border-2 border-cyan relative" : "border border-edge"
            }`}
          >
            {tier.highlight && (
              <span className="absolute -top-3 left-1/2 -translate-x-1/2 bg-cyan text-ink text-xs font-bold px-3 py-1 rounded-full">
                MOST POPULAR
              </span>
            )}
            <h3 className="text-white text-xl font-semibold mb-2">{tier.name}</h3>
            <div className="mb-6">
              <span className="text-4xl font-bold text-yellow">{tier.price}</span>
              <span className="text-gray text-sm">{tier.period}</span>
            </div>
            <ul className="space-y-3 mb-8 flex-1">
              {tier.features.map((f) => (
                <li key={f} className="text-gray2 text-sm flex items-center gap-2">
                  <span className="text-green">&#10003;</span>
                  {f}
                </li>
              ))}
            </ul>
            <a
              href={tier.href}
              className={`block text-center py-3 rounded-md font-semibold text-sm transition-all ${
                tier.highlight
                  ? "bg-cyan text-ink hover:opacity-90"
                  : "border border-edge text-white hover:border-edge2"
              }`}
            >
              {tier.cta}
            </a>
          </div>
        ))}
      </div>
    </main>
  );
}
