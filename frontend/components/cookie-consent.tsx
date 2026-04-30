"use client";

import { useEffect, useState } from "react";

const STORAGE_KEY = "cookie-consent";

export default function CookieConsent() {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored === null) {
      setVisible(true);
    }
  }, []);

  function handleChoice(accepted: boolean) {
    localStorage.setItem(STORAGE_KEY, accepted ? "accepted" : "declined");
    setVisible(false);
  }

  if (!visible) {
    return null;
  }

  return (
    <div className="fixed bottom-0 left-0 right-0 z-50 border-t border-[var(--card-border)] bg-[var(--card)] px-6 py-4">
      <div className="mx-auto flex max-w-5xl flex-col items-center gap-4 sm:flex-row sm:justify-between">
        <p className="text-sm text-[var(--muted)]">
          We use cookies to improve your experience and analyze site usage. By
          continuing to use this site, you consent to our use of cookies.
        </p>
        <div className="flex shrink-0 gap-3">
          <button
            onClick={() => handleChoice(false)}
            className="rounded-lg border border-[var(--card-border)] px-4 py-2 text-sm text-[var(--muted)] transition hover:border-[var(--muted)] hover:text-white"
          >
            Decline
          </button>
          <button
            onClick={() => handleChoice(true)}
            className="rounded-lg bg-[var(--accent)] px-4 py-2 text-sm font-medium text-white transition hover:bg-[var(--accent-hover)]"
          >
            Accept
          </button>
        </div>
      </div>
    </div>
  );
}
