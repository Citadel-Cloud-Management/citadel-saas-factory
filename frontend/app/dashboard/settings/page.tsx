"use client";

import { useQuery } from "@tanstack/react-query";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { StatusBadge } from "@/components/ui/status-badge";
import { billingApi } from "@/lib/fintech-api";
import { useAuth } from "@/lib/providers";

export default function SettingsPage() {
  const { user, logout } = useAuth();

  const { data: subRes } = useQuery({
    queryKey: ["subscription"],
    queryFn: () => billingApi.subscription(),
  });

  const subscription = subRes?.data;

  async function handleUpgrade(plan: string) {
    try {
      const res = await billingApi.checkout(plan);
      if (res.data?.checkout_url) {
        window.location.href = res.data.checkout_url;
      }
    } catch (err) {
      console.error("Checkout failed:", err);
    }
  }

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white">Settings</h1>
        <p className="mt-1 text-zinc-400">Manage your account, billing, and API keys.</p>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        {/* Account Info */}
        <Card>
          <div className="p-6">
            <h3 className="text-lg font-semibold text-white">Account</h3>
            <div className="mt-4 space-y-3">
              <div className="flex justify-between">
                <span className="text-sm text-zinc-400">Email</span>
                <span className="text-sm text-white">{user?.email ?? "—"}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-zinc-400">Name</span>
                <span className="text-sm text-white">{user?.full_name ?? "—"}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-zinc-400">Role</span>
                <StatusBadge label={user?.role ?? "member"} variant="info" />
              </div>
            </div>
            <div className="mt-6 flex gap-3">
              <Button variant="outline" className="flex-1">Edit Profile</Button>
              <Button variant="outline" className="flex-1">Change Password</Button>
            </div>
          </div>
        </Card>

        {/* Billing */}
        <Card>
          <div className="p-6">
            <h3 className="text-lg font-semibold text-white">Billing & Plan</h3>
            <div className="mt-4 space-y-3">
              <div className="flex justify-between">
                <span className="text-sm text-zinc-400">Current Plan</span>
                <StatusBadge label={subscription?.plan ?? "FREE"} variant="info" />
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-zinc-400">Status</span>
                <StatusBadge label={subscription?.status ?? "active"} variant="success" />
              </div>
            </div>
            <div className="mt-6 space-y-2">
              <Button className="w-full" onClick={() => handleUpgrade("pro")}>
                Upgrade to Pro — $199/mo
              </Button>
              <Button variant="outline" className="w-full">
                Manage Billing
              </Button>
            </div>
          </div>
        </Card>

        {/* API Keys */}
        <Card>
          <div className="p-6">
            <h3 className="text-lg font-semibold text-white">API Keys</h3>
            <p className="mt-2 text-sm text-zinc-400">
              Integrate Citadel into your applications.
            </p>
            <div className="mt-4 rounded-lg border border-zinc-800 bg-zinc-900 p-3">
              <code className="text-xs text-zinc-400">sk_live_••••••••••••••••</code>
            </div>
            <div className="mt-4 flex gap-3">
              <Button variant="outline" className="flex-1">Generate Key</Button>
              <Button variant="outline" className="flex-1">API Docs</Button>
            </div>
          </div>
        </Card>

        {/* Danger Zone */}
        <Card>
          <div className="p-6">
            <h3 className="text-lg font-semibold text-white">Account Actions</h3>
            <div className="mt-4 space-y-3">
              <button
                onClick={logout}
                className="w-full rounded-lg border border-zinc-700 px-4 py-2 text-sm text-zinc-300 transition hover:border-zinc-500"
              >
                Sign Out
              </button>
              <button className="w-full rounded-lg border border-red-800/50 px-4 py-2 text-sm text-red-400 transition hover:border-red-600">
                Delete Account
              </button>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}
