"use client";

import { QueryClient, QueryClientProvider, useQueryClient } from "@tanstack/react-query";
import { createContext, useContext, useEffect, useRef, useState, type ReactNode } from "react";

// ─── Query Client ──────────────────────────────────────────────────────

function makeQueryClient(): QueryClient {
  return new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 30_000,
        retry: 1,
        refetchOnWindowFocus: false,
      },
    },
  });
}

// ─── Auth Context ──────────────────────────────────────────────────────

interface User {
  readonly id: string;
  readonly email: string;
  readonly role: string;
  readonly full_name: string;
}

interface AuthContextValue {
  readonly user: User | null;
  readonly token: string | null;
  readonly isAuthenticated: boolean;
  readonly isLoading: boolean;
  readonly login: (email: string, password: string) => Promise<void>;
  readonly signup: (data: { email: string; password: string; full_name: string }) => Promise<void>;
  readonly logout: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Sync token to both localStorage (for API client) and a cookie (for middleware).
 * The cookie is NOT httpOnly since it's set client-side — it exists solely for
 * Next.js middleware route protection. The actual auth header uses localStorage.
 */
function persistToken(accessToken: string): void {
  localStorage.setItem("access_token", accessToken);
  document.cookie = `access_token=${encodeURIComponent(accessToken)}; path=/; max-age=${60 * 60 * 24 * 7}; SameSite=Strict; Secure`;
}

function clearToken(): void {
  localStorage.removeItem("access_token");
  document.cookie = "access_token=; path=/; max-age=0";
}

function AuthProvider({ children }: { children: ReactNode }) {
  const queryClient = useQueryClient();
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const isMounted = useRef(true);

  useEffect(() => {
    isMounted.current = true;
    const stored = localStorage.getItem("access_token");
    if (stored) {
      setToken(stored);
      fetchUser(stored);
    } else {
      setIsLoading(false);
    }
    return () => {
      isMounted.current = false;
    };
  }, []);

  async function fetchUser(accessToken: string): Promise<void> {
    try {
      const res = await fetch(`${API_BASE}/api/v1/users/me`, {
        headers: { Authorization: `Bearer ${accessToken}` },
      });
      if (!isMounted.current) return;
      if (res.ok) {
        const data: unknown = await res.json();
        const parsed = data as { data?: User } & Partial<User>;
        setUser(parsed.data ?? (parsed as User));
      } else {
        clearToken();
        setToken(null);
      }
    } catch {
      // Network error — keep token, will retry on next mount
    } finally {
      if (isMounted.current) {
        setIsLoading(false);
      }
    }
  }

  async function login(email: string, password: string): Promise<void> {
    const res = await fetch(`${API_BASE}/api/v1/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    if (!res.ok) {
      const err: { detail?: string } = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Login failed");
    }

    const data = await res.json() as { access_token?: string; data?: { access_token?: string } };
    const accessToken = data.access_token ?? data.data?.access_token;

    if (!accessToken) {
      throw new Error("No access token received from server");
    }

    persistToken(accessToken);
    setToken(accessToken);
    await fetchUser(accessToken);
  }

  async function signup(signupData: { email: string; password: string; full_name: string }): Promise<void> {
    const res = await fetch(`${API_BASE}/api/v1/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(signupData),
    });

    if (!res.ok) {
      const err: { detail?: string } = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Signup failed");
    }

    // Auto-login after signup
    await login(signupData.email, signupData.password);
  }

  function logout(): void {
    clearToken();
    setToken(null);
    setUser(null);
    queryClient.clear();
    window.location.href = "/login";
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated: !!user,
        isLoading,
        login,
        signup,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within Providers");
  return ctx;
}

// ─── Combined Providers ────────────────────────────────────────────────

export function Providers({ children }: { children: ReactNode }) {
  // Create QueryClient once per component instance (safe for SSR)
  const queryClientRef = useRef<QueryClient | null>(null);
  if (!queryClientRef.current) {
    queryClientRef.current = makeQueryClient();
  }

  return (
    <QueryClientProvider client={queryClientRef.current}>
      <AuthProvider>{children}</AuthProvider>
    </QueryClientProvider>
  );
}
