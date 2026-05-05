/**
 * Fintech API — domain-specific typed endpoints for accounts, transactions, KYC.
 * Built on top of the base api client.
 */

import { api } from "./api";

// ─── Types ─────────────────────────────────────────────────────────────

export interface Account {
  readonly id: string;
  readonly account_type: "checking" | "savings" | "wallet" | "escrow";
  readonly currency: string;
  readonly balance: string;
  readonly available_balance: string;
  readonly status: "active" | "frozen" | "closed" | "pending_verification";
  readonly account_number: string;
  readonly created_at: string;
}

export interface Transaction {
  readonly id: string;
  readonly reference_id: string;
  readonly amount: string;
  readonly currency: string;
  readonly transaction_type: "transfer" | "deposit" | "withdrawal" | "payment" | "refund" | "fee" | "remittance";
  readonly status: "pending" | "processing" | "completed" | "failed" | "reversed";
  readonly description: string | null;
  readonly created_at: string;
  readonly completed_at: string | null;
}

export interface KYCVerification {
  readonly id: string;
  readonly verification_level: "none" | "basic" | "enhanced" | "full";
  readonly status: "pending" | "in_review" | "approved" | "rejected" | "expired";
  readonly risk_score: number;
  readonly verified_at: string | null;
}

export interface Plan {
  readonly name: string;
  readonly price_monthly: number;
  readonly features: {
    readonly max_accounts: number;
    readonly max_transactions_monthly: number;
    readonly api_access: boolean;
    readonly priority_support: boolean;
  };
}

export interface TransferRequest {
  readonly debit_account_id: string;
  readonly credit_account_id: string;
  readonly amount: string;
  readonly currency: string;
  readonly description?: string;
  readonly idempotency_key: string;
}

// ─── API Functions ─────────────────────────────────────────────────────

export const accountsApi = {
  list: () => api.get<Account[]>("/api/v1/accounts"),
  get: (id: string) => api.get<Account>(`/api/v1/accounts/${id}`),
  create: (data: { account_type: string; currency: string }) =>
    api.post<Account>("/api/v1/accounts", data),
};

export const transactionsApi = {
  list: (page = 1, limit = 20) =>
    api.get<Transaction[]>("/api/v1/transactions", {
      params: { page: String(page), limit: String(limit) },
    }),
  get: (id: string) => api.get<Transaction>(`/api/v1/transactions/${id}`),
  transfer: (data: TransferRequest) =>
    api.post<Transaction>("/api/v1/transactions/transfer", data),
};

export const kycApi = {
  status: () => api.get<KYCVerification>("/api/v1/kyc/status"),
  initiate: (data: { level: string; document_type: string }) =>
    api.post<KYCVerification>("/api/v1/kyc/verify", data),
};

export const billingApi = {
  plans: () => api.get<Plan[]>("/api/v1/billing/plans"),
  subscription: () => api.get<{ plan: string; status: string }>("/api/v1/billing/subscription"),
  checkout: (plan: string) =>
    api.post<{ checkout_url: string }>("/api/v1/billing/checkout", {
      plan,
      success_url: `${typeof window !== "undefined" ? window.location.origin : ""}/dashboard?checkout=success`,
      cancel_url: `${typeof window !== "undefined" ? window.location.origin : ""}/dashboard/settings`,
    }),
};
