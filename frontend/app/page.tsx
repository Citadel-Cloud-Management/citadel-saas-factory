import Link from "next/link";

const features = [
  {
    title: "500+ Agents",
    description:
      "Autonomous business agents spanning 30 domains — from engineering to marketing to finance.",
    icon: "🤖",
  },
  {
    title: "Multi-Model AI",
    description:
      "Route tasks to the optimal model — Claude, GPT, Gemini, Llama, or local Ollama instances.",
    icon: "🧠",
  },
  {
    title: "Enterprise Security",
    description:
      "Guardrails, Vault secrets, mTLS service mesh, container scanning, and RBAC built in.",
    icon: "🛡️",
  },
  {
    title: "Zero Lock-in",
    description:
      "12 model providers, GitOps deployment, and infrastructure-agnostic design. Own your stack.",
    icon: "🔓",
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
        <h1 className="max-w-3xl text-5xl font-extrabold leading-tight tracking-tight text-white sm:text-6xl">
          Citadel SaaS Factory
        </h1>
        <p className="mt-6 max-w-2xl text-lg text-[var(--muted)]">
          The autonomous SaaS production framework. 500+ AI agents orchestrate
          your entire business — engineering, marketing, sales, security, and
          beyond — so you ship faster with fewer humans in the loop.
        </p>
        <div className="mt-10 flex gap-4">
          <Link
            href="/signup"
            className="rounded-lg bg-[var(--accent)] px-6 py-3 font-semibold text-white transition hover:bg-[var(--accent-hover)]"
          >
            Get Started
          </Link>
          <Link
            href="/dashboard"
            className="rounded-lg border border-[var(--card-border)] px-6 py-3 font-semibold text-[var(--foreground)] transition hover:border-[var(--muted)]"
          >
            View Dashboard
          </Link>
        </div>
      </main>

      {/* Features */}
      <section className="border-t border-[var(--card-border)] px-6 py-20">
        <div className="mx-auto grid max-w-5xl gap-8 sm:grid-cols-2 lg:grid-cols-4">
          {features.map((feature) => (
            <div
              key={feature.title}
              className="rounded-xl border border-[var(--card-border)] bg-[var(--card)] p-6 transition hover:border-[var(--accent)]"
            >
              <div className="mb-3 text-3xl">{feature.icon}</div>
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

      {/* Footer */}
      <footer className="border-t border-[var(--card-border)] px-6 py-6 text-center text-sm text-[var(--muted)]">
        <p>
          &copy; {new Date().getFullYear()} Citadel Cloud Management. All rights
          reserved.
        </p>
        <div className="mt-2 flex justify-center gap-4">
          <Link
            href="/privacy"
            className="transition hover:text-white"
          >
            Privacy Policy
          </Link>
          <Link
            href="/terms"
            className="transition hover:text-white"
          >
            Terms of Service
          </Link>
        </div>
      </footer>
    </div>
  );
}
