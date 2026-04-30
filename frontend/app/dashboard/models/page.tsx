import { Card, CardHeader, CardContent } from "@/components/ui/card";

interface ModelTier {
  readonly tier: string;
  readonly primary: string;
  readonly fallbacks: string;
  readonly useCase: string;
  readonly maxTokens: string;
  readonly color: string;
}

const tiers: readonly ModelTier[] = [
  {
    tier: "Premium",
    primary: "Claude Opus 4.7",
    fallbacks: "GPT-4o, Gemini Ultra",
    useCase: "Architecture, complex reasoning, agentic workflows",
    maxTokens: "200K",
    color: "bg-purple-600",
  },
  {
    tier: "Default",
    primary: "Claude Sonnet 4.6",
    fallbacks: "GPT-4o-mini, Gemini Pro",
    useCase: "Standard coding tasks, orchestration",
    maxTokens: "200K",
    color: "bg-blue-600",
  },
  {
    tier: "Cheap",
    primary: "Claude Haiku 4.5",
    fallbacks: "GPT-4o-mini, Gemini Flash",
    useCase: "Classification, routing, extraction",
    maxTokens: "200K",
    color: "bg-teal-600",
  },
  {
    tier: "Reasoning Deep",
    primary: "o3 (OpenAI)",
    fallbacks: "Claude Opus 4.7",
    useCase: "Multi-step math, logic chains, formal proofs",
    maxTokens: "128K",
    color: "bg-amber-600",
  },
  {
    tier: "Reasoning Fast",
    primary: "o4-mini (OpenAI)",
    fallbacks: "Claude Sonnet 4.6",
    useCase: "Quick reasoning, code generation with chain-of-thought",
    maxTokens: "128K",
    color: "bg-orange-600",
  },
  {
    tier: "Vision",
    primary: "Claude Sonnet 4.6",
    fallbacks: "GPT-4o, Gemini Pro Vision",
    useCase: "Image analysis, screenshot interpretation, OCR",
    maxTokens: "200K",
    color: "bg-pink-600",
  },
  {
    tier: "Embedding",
    primary: "text-embedding-3-large",
    fallbacks: "voyage-3, Cohere embed-v4",
    useCase: "Semantic search, RAG, similarity matching",
    maxTokens: "8K",
    color: "bg-indigo-600",
  },
  {
    tier: "Local",
    primary: "Llama 3.3 70B (Ollama)",
    fallbacks: "Mistral, Qwen 2.5",
    useCase: "Offline development, air-gapped environments",
    maxTokens: "128K",
    color: "bg-gray-600",
  },
];

export default function ModelsPage() {
  return (
    <div className="p-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white">Model Catalog</h1>
        <p className="mt-1 text-[var(--muted)]">
          {tiers.length} model tiers across 12 providers.
        </p>
      </div>

      {/* Table */}
      <Card>
        <CardHeader>
          <h2 className="text-lg font-semibold text-white">
            Routing Configuration
          </h2>
        </CardHeader>
        <CardContent className="overflow-x-auto p-0">
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-[var(--card-border)] text-[var(--muted)]">
                <th className="px-6 py-3 font-medium">Tier</th>
                <th className="px-6 py-3 font-medium">Primary Model</th>
                <th className="px-6 py-3 font-medium">Fallbacks</th>
                <th className="px-6 py-3 font-medium">Use Case</th>
                <th className="px-6 py-3 font-medium">Max Tokens</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[var(--card-border)]">
              {tiers.map((tier) => (
                <tr key={tier.tier} className="text-[var(--foreground)]">
                  <td className="whitespace-nowrap px-6 py-4">
                    <span
                      className={`inline-flex rounded-full px-3 py-1 text-xs font-medium text-white ${tier.color}`}
                    >
                      {tier.tier}
                    </span>
                  </td>
                  <td className="whitespace-nowrap px-6 py-4 font-medium text-white">
                    {tier.primary}
                  </td>
                  <td className="px-6 py-4 text-[var(--muted)]">
                    {tier.fallbacks}
                  </td>
                  <td className="px-6 py-4">{tier.useCase}</td>
                  <td className="whitespace-nowrap px-6 py-4 text-[var(--muted)]">
                    {tier.maxTokens}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </CardContent>
      </Card>
    </div>
  );
}
