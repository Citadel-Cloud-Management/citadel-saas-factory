"use client";

import { useState, type FormEvent } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { useAuth } from "@/lib/providers";

export default function LoginPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { login } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      await login(email, password);
      const redirect = searchParams.get("redirect") || "/dashboard";
      router.push(redirect);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center px-4">
      <Card className="w-full max-w-md">
        <div className="p-8">
          <h1 className="mb-2 text-2xl font-bold text-white">Sign In</h1>
          <p className="mb-6 text-sm text-zinc-400">
            Welcome back to Citadel
          </p>

          {error && (
            <div className="mb-4 rounded-lg bg-red-500/10 border border-red-500/20 px-4 py-3 text-sm text-red-400">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <Input
              label="Email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@company.com"
              required
            />
            <Input
              label="Password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
            />
            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? "Signing in..." : "Sign In"}
            </Button>
          </form>

          <div className="my-6 flex items-center gap-3">
            <div className="h-px flex-1 bg-zinc-800" />
            <span className="text-xs text-zinc-500">or</span>
            <div className="h-px flex-1 bg-zinc-800" />
          </div>

          <Button variant="outline" className="w-full">
            Sign in with SSO
          </Button>

          <p className="mt-6 text-center text-sm text-zinc-400">
            Don&apos;t have an account?{" "}
            <Link href="/signup" className="text-indigo-400 hover:underline">
              Sign up
            </Link>
          </p>
        </div>
      </Card>
    </div>
  );
}
