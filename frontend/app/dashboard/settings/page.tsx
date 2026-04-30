"use client";

import { useState } from "react";
import { Card, CardHeader, CardContent, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { api } from "@/lib/api";

interface NotificationPrefs {
  readonly securityAlerts: boolean;
  readonly billing: boolean;
  readonly weeklyReports: boolean;
}

function Toggle({
  label,
  checked,
  onChange,
}: {
  readonly label: string;
  readonly checked: boolean;
  readonly onChange: (value: boolean) => void;
}) {
  return (
    <label className="flex items-center justify-between py-3">
      <span className="text-sm text-[var(--foreground)]">{label}</span>
      <button
        type="button"
        role="switch"
        aria-checked={checked}
        onClick={() => onChange(!checked)}
        className={`relative inline-flex h-6 w-11 shrink-0 cursor-pointer rounded-full transition-colors ${
          checked ? "bg-[var(--accent)]" : "bg-[var(--card-border)]"
        }`}
      >
        <span
          className={`pointer-events-none inline-block h-5 w-5 translate-y-0.5 rounded-full bg-white shadow transition-transform ${
            checked ? "translate-x-[22px]" : "translate-x-0.5"
          }`}
        />
      </button>
    </label>
  );
}

export default function SettingsPage() {
  const [tenantName, setTenantName] = useState("My Organization");
  const [saving, setSaving] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [notifications, setNotifications] = useState<NotificationPrefs>({
    securityAlerts: true,
    billing: true,
    weeklyReports: false,
  });

  const handleSave = async () => {
    setSaving(true);
    try {
      await api.put("/api/v1/tenants/current", {
        name: tenantName,
        notifications,
      });
    } catch {
      // error handled by api layer
    } finally {
      setSaving(false);
    }
  };

  const handleNotificationChange = (
    key: keyof NotificationPrefs,
    value: boolean,
  ) => {
    setNotifications((prev) => ({ ...prev, [key]: value }));
  };

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white">Settings</h1>
        <p className="mt-1 text-[var(--muted)]">
          Manage your organization and preferences.
        </p>
      </div>

      <div className="max-w-2xl space-y-6">
        {/* General */}
        <Card>
          <CardHeader>
            <h2 className="text-lg font-semibold text-white">General</h2>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <Input
                label="Organization Name"
                value={tenantName}
                onChange={(e) => setTenantName(e.target.value)}
              />
              <Input
                label="Slug"
                value="my-organization"
                disabled
                readOnly
              />
              <div className="space-y-1.5">
                <span className="block text-sm font-medium text-[var(--foreground)]">
                  Plan
                </span>
                <span className="inline-flex items-center rounded-full bg-[var(--accent)] px-3 py-1 text-xs font-medium text-white">
                  Pro
                </span>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Notifications */}
        <Card>
          <CardHeader>
            <h2 className="text-lg font-semibold text-white">
              Notification Preferences
            </h2>
          </CardHeader>
          <CardContent>
            <div className="divide-y divide-[var(--card-border)]">
              <Toggle
                label="Security Alerts"
                checked={notifications.securityAlerts}
                onChange={(v) => handleNotificationChange("securityAlerts", v)}
              />
              <Toggle
                label="Billing Notifications"
                checked={notifications.billing}
                onChange={(v) => handleNotificationChange("billing", v)}
              />
              <Toggle
                label="Weekly Reports"
                checked={notifications.weeklyReports}
                onChange={(v) => handleNotificationChange("weeklyReports", v)}
              />
            </div>
          </CardContent>
        </Card>

        {/* Save */}
        <div className="flex justify-end">
          <Button onClick={handleSave} disabled={saving}>
            {saving ? "Saving..." : "Save Changes"}
          </Button>
        </div>

        {/* Danger Zone */}
        <Card className="border-[var(--danger)]">
          <CardHeader>
            <h2 className="text-lg font-semibold text-[var(--danger)]">
              Danger Zone
            </h2>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-[var(--muted)]">
              Permanently delete your account and all associated data. This
              action cannot be undone.
            </p>
            <div className="mt-4">
              {showDeleteConfirm ? (
                <div className="flex items-center gap-3">
                  <span className="text-sm text-[var(--danger)]">
                    Are you sure?
                  </span>
                  <Button
                    variant="outline"
                    size="sm"
                    className="border-[var(--danger)] text-[var(--danger)]"
                  >
                    Yes, delete my account
                  </Button>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setShowDeleteConfirm(false)}
                  >
                    Cancel
                  </Button>
                </div>
              ) : (
                <Button
                  variant="outline"
                  className="border-[var(--danger)] text-[var(--danger)]"
                  onClick={() => setShowDeleteConfirm(true)}
                >
                  Delete Account
                </Button>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
