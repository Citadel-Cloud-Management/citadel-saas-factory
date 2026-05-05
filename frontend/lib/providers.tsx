"use client";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { createContext, useContext, useEffect, useState, type ReactNode } from "react";

// ─── Query Client ──────────────────────────────────────────────────────

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 30_000,
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

// ─── Auth Context ──────────────────────────────────────────────────────

interface User {
  id: string;
  email: string;
  role: string;
  full_name: string;
}

interface AuthContextValue {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  signup: (data: { email: string; password: string; full_name: string }) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const stored = localStorage.getItem("access_token");
    if (stored) {
      setToken(stored);
      fetchUser(stored);
    } else {
      setIsLoading(false);
    }
  }, []);

  async function fetchUser(accessToken: string) {
    try {
      const res = await fetch(`${API_BASE}/api/v1/users/me`, {
        headers: { Authorization: `Bearer ${accessToken}` },
      });
      if (res.ok) {
        const data = await res.json();
        setUser(data.data ?? data);
      } else {
        localStorage.removeItem("access_token");
        setToken(null);
      }
    } catch {
      // Network error — keep token, will retry
    } finally {
      setIsLoading(false);
    }
  }

  async function login(email: string, password: string) {
    const res = await fetch(`${API_BASE}/api/v1/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Login failed");
    }

    const data = await res.json();
    const accessToken = data.access_token ?? data.data?.access_token;
    localStorage.setItem("access_token", accessToken);
    setToken(accessToken);
    await fetchUser(accessToken);
  }

  async function signup(data: { email: string; password: string; full_name: string }) {
    const res = await fetch(`${API_BASE}/api/v1/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Signup failed");
    }

    // Auto-login after signup
    await login(data.email, data.password);
  }

  function logout() {
    localStorage.removeItem("access_token");
    setToken(null);
    setUser(null);
    queryClient.clear();
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

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within Providers");
  return ctx;
}

// ─── Combined Providers ────────────────────────────────────────────────

export function Providers({ children }: { children: ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>{children}</AuthProvider>
    </QueryClientProvider>
  );
}
