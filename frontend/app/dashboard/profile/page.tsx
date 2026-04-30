"use client";

import { useState } from "react";
import { Card, CardHeader, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { api } from "@/lib/api";

export default function ProfilePage() {
  const [fullName, setFullName] = useState("Admin User");
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [saving, setSaving] = useState(false);
  const [passwordError, setPasswordError] = useState("");

  const email = "admin@citadel.dev";
  const role = "Owner";
  const initials = fullName
    .split(" ")
    .map((n) => n[0])
    .join("")
    .toUpperCase()
    .slice(0, 2);

  const handleSave = async () => {
    setPasswordError("");

    if (newPassword && newPassword !== confirmPassword) {
      setPasswordError("Passwords do not match");
      return;
    }

    if (newPassword && newPassword.length < 8) {
      setPasswordError("Password must be at least 8 characters");
      return;
    }

    setSaving(true);
    try {
      await api.put("/api/v1/users/me", {
        full_name: fullName,
        ...(newPassword
          ? { current_password: currentPassword, new_password: newPassword }
          : {}),
      });
      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");
    } catch {
      // error handled by api layer
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white">Profile</h1>
        <p className="mt-1 text-[var(--muted)]">
          Manage your personal information and security.
        </p>
      </div>

      <div className="max-w-2xl space-y-6">
        {/* Avatar + Info */}
        <Card>
          <CardHeader>
            <h2 className="text-lg font-semibold text-white">
              Personal Information
            </h2>
          </CardHeader>
          <CardContent>
            <div className="mb-6 flex items-center gap-4">
              <div className="flex h-16 w-16 items-center justify-center rounded-full bg-[var(--accent)] text-xl font-bold text-white">
                {initials}
              </div>
              <div>
                <p className="text-sm font-medium text-white">{fullName}</p>
                <p className="text-sm text-[var(--muted)]">{email}</p>
              </div>
            </div>
            <div className="space-y-4">
              <Input
                label="Full Name"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
              />
              <Input
                label="Email"
                value={email}
                disabled
                readOnly
              />
              <div className="space-y-1.5">
                <span className="block text-sm font-medium text-[var(--foreground)]">
                  Role
                </span>
                <span className="inline-flex items-center rounded-full bg-emerald-600 px-3 py-1 text-xs font-medium text-white">
                  {role}
                </span>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Change Password */}
        <Card>
          <CardHeader>
            <h2 className="text-lg font-semibold text-white">
              Change Password
            </h2>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <Input
                label="Current Password"
                type="password"
                value={currentPassword}
                onChange={(e) => setCurrentPassword(e.target.value)}
                placeholder="Enter current password"
              />
              <Input
                label="New Password"
                type="password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                placeholder="Enter new password"
                error={passwordError}
              />
              <Input
                label="Confirm New Password"
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="Confirm new password"
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
      </div>
    </div>
  );
}
