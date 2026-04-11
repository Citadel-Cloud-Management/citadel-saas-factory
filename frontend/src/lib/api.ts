const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function fetchAPI<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;
  const headers: Record<string, string> = { "Content-Type": "application/json", ...options.headers as Record<string, string> };
  if (token) headers["Authorization"] = `Bearer ${token}`;
  const res = await fetch(`${API_BASE}${endpoint}`, { ...options, headers });
  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(error.detail || "API Error");
  }
  return res.json();
}

export const api = {
  auth: {
    login: (email: string, password: string) => fetchAPI<{ access_token: string }>("/auth/login", { method: "POST", body: JSON.stringify({ email, password }) }),
    register: (data: { email: string; password: string; first_name: string; last_name: string }) => fetchAPI<{ access_token: string }>("/auth/register", { method: "POST", body: JSON.stringify(data) }),
    me: () => fetchAPI<import("./types").User>("/auth/me"),
  },
  products: {
    list: (params?: { collection?: string; page?: number }) => fetchAPI<{ products: import("./types").Product[]; total: number }>(`/products?${new URLSearchParams(params as any)}`),
    get: (slug: string) => fetchAPI<import("./types").Product>(`/products/${slug}`),
  },
  courses: {
    list: () => fetchAPI<import("./types").Course[]>("/courses"),
    get: (slug: string) => fetchAPI<import("./types").Course>(`/courses/${slug}`),
    enroll: (slug: string) => fetchAPI<{ message: string }>(`/courses/${slug}/enroll`, { method: "POST" }),
  },
  orders: {
    list: () => fetchAPI<import("./types").Order[]>("/orders"),
    create: (items: { product_id: string; quantity: number }[]) => fetchAPI<import("./types").Order>("/orders", { method: "POST", body: JSON.stringify({ items }) }),
  },
};
