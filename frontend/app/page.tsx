import Link from "next/link";

const features = [
  {
    title: "AI-Powered Compliance",
    description:
      "Autonomous AML screening, KYC verification, and CTR/SAR detection powered by 500+ specialized agents.",
  },
  {
    title: "Double-Entry Ledger",
    description:
      "Enterprise-grade financial ledger with immutable audit trail, idempotent transactions, and real-time balance tracking.",
  },
  {
    title: "Multi-Tenant Security",
    description:
      "Row-level isolation, KMS encryption at rest, mTLS in transit, WAF protection, and SOC 2 ready infrastructure.",
  },
  {
    title: "Global Payments",
    description:
      "Multi-currency accounts, cross-border remittance, Stripe billing, and Plaid bank linking out of the box.",
  },
  {
    title: "Self-Healing Infrastructure",
    description:
      "L4 autonomous operations — auto-scaling, auto-remediation, rollback on failure, and event-driven agent coordination.",
  },
  {
    title: "Zero Vendor Lock-in",
    description:
      "AWS-native but portable. 12 AI model providers, GitOps deployment, and infrastructure-as-code throughout.",
  },
];

const plans = [
  {
    name: "Free",
    price: "$0",
    period: "/month",
    description: "For exploration and testing",
    features: ["100 transactions/mo", "2 accounts", "5 KYC checks", "Community support"],
    cta: "Get Started",
    highlighted: false,
  },
  {
    name: "Starter",
    price: "$49",
    period: "/month",
    description: "For early-stage fintechs",
    features: ["5,000 transactions/mo", "10 accounts", "50 KYC checks", "Email support", "API access (read)"],
    cta: "Start Free Trial",
    highlighted: false,
  },
  {
    name: "Pro",
    price: "$199",
    period: "/month",
    description: "For growing platforms",
    features: ["50,000 transactions/mo", "50 accounts", "500 KYC checks", "Priority support", "Full API access", "100 AI agents"],
    cta: "Start Free Trial",
    highlighted: true,
  },
  {
    name: "Enterprise",
    price: "$999",
    period: "/month",
    description: "For regulated institutions",
    features: ["Unlimited transactions", "Unlimited accounts", "Unlimited KYC", "Dedicated CSM", "Custom compliance rules", "500+ AI agents", "99.99% SLA"],
    cta: "Contact Sales",
    highlighted: false,
  },
];

export default function HomePage() {
  return (
    <div className="flex min-h-screen flex-col">
      {/* Nav */}
      <nav className="flex items-center justify-between border-b border-[var(--card-border)] px-6 py-4">
        <span className="text-xl font-bold tracking-tight text-white">
          Citadel
        </span>
        <div className="flex gap-4">
          <Link
            href="/login"
            className="text-sm text-[var(--muted)] transition hover:text-white"
          >
            Sign In
          </Link>
          <Link
            href="/signup"
            className="rounded-lg bg-[var(--accent)] px-4 py-1.5 text-sm font-medium text-white transition hover:bg-[var(--accent-hover)]"
          >
            Get Started
          </Link>
        </div>
      </nav>

      {/* Hero */}
      <main className="flex flex-1 flex-col items-center justify-center px-6 py-24 text-center">
        <div className="mb-4 inline-flex items-center rounded-full border border-[var(--card-border)] px-4 py-1 text-xs text-[var(--muted)]">
          AI-Native Fintech Infrastructure
        </div>
        <h1 className="max-w-4xl text-5xl font-extrabold leading-tight tracking-tight text-white sm:text-6xl">
          Compliance Intelligence
          <br />
          <span className="text-[var(--accent)]">That Never Sleeps</span>
        </h1>
        <p className="mt-6 max-w-2xl text-lg text-[var(--muted)]">
          Autonomous AML screening, real-time transaction monitoring, and
          AI-powered KYC verification. Deploy enterprise-grade financial
          infrastructure in minutes, not months.
        </p>
        <div className="mt-10 flex gap-4">
          <Link
            href="/signup"
            className="rounded-lg bg-[var(--accent)] px-6 py-3 font-semibold text-white transition hover:bg-[var(--accent-hover)]"
          >
            Start Free Trial
          </Link>
          <Link
            href="#pricing"
            className="rounded-lg border border-[var(--card-border)] px-6 py-3 font-semibold text-[var(--foreground)] transition hover:border-[var(--muted)]"
          >
            View Pricing
          </Link>
        </div>
        <p className="mt-4 text-xs text-[var(--muted)]">
          No credit card required. SOC 2 compliant. AWS-hosted.
        </p>
      </main>

      {/* Features */}
      <section className="border-t border-[var(--card-border)] px-6 py-20">
        <div className="mx-auto max-w-5xl text-center">
          <h2 className="text-3xl font-bold text-white">
            Everything You Need to Build Compliant Financial Products
          </h2>
          <p className="mt-4 text-[var(--muted)]">
            From transaction processing to regulatory reporting — all powered by autonomous AI agents.
          </p>
        </div>
        <div className="mx-auto mt-12 grid max-w-5xl gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {features.map((feature) => (
            <div
              key={feature.title}
              className="rounded-xl border border-[var(--card-border)] bg-[var(--card)] p-6 transition hover:border-[var(--accent)]"
            >
              <h3 className="mb-2 text-lg font-semibold text-white">
                {feature.title}
              </h3>
              <p className="text-sm leading-relaxed text-[var(--muted)]">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* Pricing */}
      <section id="pricing" className="border-t border-[var(--card-border)] px-6 py-20">
        <div className="mx-auto max-w-5xl text-center">
          <h2 className="text-3xl font-bold text-white">Simple, Transparent Pricing</h2>
          <p className="mt-4 text-[var(--muted)]">
            Start free. Scale as you grow. Enterprise when you need it.
          </p>
        </div>
        <div className="mx-auto mt-12 grid max-w-6xl gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {plans.map((plan) => (
            <div
              key={plan.name}
              className={`rounded-xl border p-6 ${
                plan.highlighted
                  ? "border-[var(--accent)] bg-[var(--accent)]/5"
                  : "border-[var(--card-border)] bg-[var(--card)]"
              }`}
            >
              {plan.highlighted && (
                <div className="mb-3 text-xs font-semibold uppercase text-[var(--accent)]">
                  Most Popular
                </div>
              )}
              <h3 className="text-lg font-semibold text-white">{plan.name}</h3>
              <p className="mt-1 text-xs text-[var(--muted)]">{plan.description}</p>
              <div className="mt-4">
                <span className="text-3xl font-bold text-white">{plan.price}</span>
                <span className="text-sm text-[var(--muted)]">{plan.period}</span>
              </div>
              <ul className="mt-6 space-y-2">
                {plan.features.map((f) => (
                  <li key={f} className="flex items-start gap-2 text-sm text-[var(--muted)]">
                    <span className="mt-0.5 text-green-400">+</span>
                    {f}
                  </li>
                ))}
              </ul>
              <Link
                href="/signup"
                className={`mt-6 block rounded-lg px-4 py-2 text-center text-sm font-medium transition ${
                  plan.highlighted
                    ? "bg-[var(--accent)] text-white hover:bg-[var(--accent-hover)]"
                    : "border border-[var(--card-border)] text-white hover:border-[var(--muted)]"
                }`}
              >
                {plan.cta}
              </Link>
            </div>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-[var(--card-border)] px-6 py-6 text-center text-sm text-[var(--muted)]">
        <p>
          &copy; {new Date().getFullYear()} Citadel Cloud Management. All rights reserved.
        </p>
        <div className="mt-2 flex justify-center gap-4">
          <Link href="/privacy" className="transition hover:text-white">
            Privacy Policy
          </Link>
          <Link href="/terms" className="transition hover:text-white">
            Terms of Service
          </Link>
        </div>
      </footer>
    </div>
  );
}
