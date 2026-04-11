export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  role: "free" | "starter" | "professional" | "enterprise" | "admin";
  is_active: boolean;
  subscription_status: string | null;
}

export interface Product {
  id: string;
  title: string;
  slug: string;
  description: string;
  price: number;
  compare_at_price: number | null;
  product_type: string;
  collection: string;
  tags: string[];
  download_url: string | null;
  is_active: boolean;
}

export interface Order {
  id: string;
  total: number;
  status: "pending" | "paid" | "refunded" | "cancelled";
  items: OrderItem[];
  created_at: string;
}

export interface OrderItem {
  id: string;
  product: Product;
  price: number;
  quantity: number;
}

export interface Course {
  id: string;
  title: string;
  slug: string;
  description: string;
  modules: Module[];
  is_free: boolean;
}

export interface Module {
  id: string;
  title: string;
  lessons: string[];
}

export interface Enrollment {
  id: string;
  course: Course;
  progress: Record<string, boolean>;
  enrolled_at: string;
}
