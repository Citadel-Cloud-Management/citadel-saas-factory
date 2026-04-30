import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Privacy Policy — Citadel Cloud Management",
  description:
    "Learn how Citadel Cloud Management collects, uses, and protects your personal data.",
};

export default function PrivacyPolicyPage() {
  return (
    <article className="prose prose-invert max-w-none prose-headings:text-white prose-p:text-[var(--muted)] prose-li:text-[var(--muted)] prose-strong:text-white">
      <h1>Privacy Policy</h1>
      <p className="text-sm">Last updated: April 30, 2026</p>

      <p>
        Citadel Cloud Management (&quot;we,&quot; &quot;us,&quot; or
        &quot;our&quot;) is committed to protecting your privacy. This Privacy
        Policy explains how we collect, use, disclose, and safeguard your
        information when you use our SaaS platform and related services
        (collectively, the &quot;Service&quot;).
      </p>

      <h2>1. Information We Collect</h2>
      <p>We collect the following categories of information:</p>
      <ul>
        <li>
          <strong>Account Information:</strong> name, email address, company
          name, and billing details you provide when creating an account.
        </li>
        <li>
          <strong>Usage Data:</strong> pages visited, features used, session
          duration, and interaction patterns collected automatically.
        </li>
        <li>
          <strong>Device &amp; Technical Data:</strong> IP address, browser type,
          operating system, and device identifiers.
        </li>
        <li>
          <strong>Communications:</strong> messages you send through our support
          channels, feedback forms, and surveys.
        </li>
        <li>
          <strong>Third-Party Integrations:</strong> data you authorize us to
          access when connecting third-party services to your account.
        </li>
      </ul>

      <h2>2. How We Use Your Information</h2>
      <p>We use the information we collect to:</p>
      <ul>
        <li>Provide, maintain, and improve the Service.</li>
        <li>Process transactions and send billing-related communications.</li>
        <li>Respond to support requests and communicate with you.</li>
        <li>
          Analyze usage patterns to enhance performance, security, and user
          experience.
        </li>
        <li>
          Detect, prevent, and address fraud, abuse, and security incidents.
        </li>
        <li>Comply with legal obligations and enforce our Terms of Service.</li>
      </ul>

      <h2>3. Data Sharing</h2>
      <p>
        We do not sell your personal data. We may share information with:
      </p>
      <ul>
        <li>
          <strong>Service Providers:</strong> trusted vendors who assist with
          hosting, analytics, payment processing, and customer support, bound by
          data processing agreements.
        </li>
        <li>
          <strong>Legal Compliance:</strong> when required by law, regulation,
          legal process, or governmental request.
        </li>
        <li>
          <strong>Business Transfers:</strong> in connection with a merger,
          acquisition, or sale of assets, with prior notice to affected users.
        </li>
      </ul>

      <h2>4. Data Retention</h2>
      <p>
        We retain your personal data for as long as your account is active or as
        needed to provide the Service. After account deletion, we retain certain
        data for up to 90 days for backup and compliance purposes, after which it
        is permanently deleted. Anonymized, aggregated data may be retained
        indefinitely for analytics.
      </p>

      <h2>5. Your Rights (GDPR)</h2>
      <p>
        If you are located in the European Economic Area (EEA), you have the
        following rights under the General Data Protection Regulation:
      </p>
      <ul>
        <li>
          <strong>Access:</strong> request a copy of the personal data we hold
          about you.
        </li>
        <li>
          <strong>Rectification:</strong> request correction of inaccurate or
          incomplete data.
        </li>
        <li>
          <strong>Erasure:</strong> request deletion of your personal data
          (&quot;right to be forgotten&quot;).
        </li>
        <li>
          <strong>Restriction:</strong> request that we limit processing of your
          data.
        </li>
        <li>
          <strong>Portability:</strong> receive your data in a structured,
          machine-readable format.
        </li>
        <li>
          <strong>Objection:</strong> object to processing based on legitimate
          interests or direct marketing.
        </li>
      </ul>
      <p>
        To exercise any of these rights, contact us at{" "}
        <a href="mailto:privacy@citadelcloudmanagement.com">
          privacy@citadelcloudmanagement.com
        </a>
        . We will respond within 30 days.
      </p>

      <h2>6. Cookies</h2>
      <p>
        We use cookies and similar tracking technologies to operate the Service
        and collect usage data. You can control cookie preferences through your
        browser settings or our cookie consent banner. Essential cookies required
        for Service functionality cannot be disabled. For more details, see our
        cookie consent banner upon first visit.
      </p>

      <h2>7. Contact</h2>
      <p>
        If you have questions about this Privacy Policy or our data practices,
        please contact us:
      </p>
      <ul>
        <li>
          <strong>Email:</strong>{" "}
          <a href="mailto:privacy@citadelcloudmanagement.com">
            privacy@citadelcloudmanagement.com
          </a>
        </li>
        <li>
          <strong>Website:</strong>{" "}
          <a
            href="https://citadelcloudmanagement.com"
            target="_blank"
            rel="noopener noreferrer"
          >
            citadelcloudmanagement.com
          </a>
        </li>
      </ul>
    </article>
  );
}
