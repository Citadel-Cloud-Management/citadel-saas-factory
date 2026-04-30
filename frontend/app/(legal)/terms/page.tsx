import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Terms of Service — Citadel Cloud Management",
  description:
    "Terms and conditions governing your use of the Citadel Cloud Management platform.",
};

export default function TermsOfServicePage() {
  return (
    <article className="prose prose-invert max-w-none prose-headings:text-white prose-p:text-[var(--muted)] prose-li:text-[var(--muted)] prose-strong:text-white">
      <h1>Terms of Service</h1>
      <p className="text-sm">Last updated: April 30, 2026</p>

      <p>
        These Terms of Service (&quot;Terms&quot;) govern your access to and use
        of the Citadel Cloud Management platform and related services
        (collectively, the &quot;Service&quot;) operated by Citadel Cloud
        Management (&quot;we,&quot; &quot;us,&quot; or &quot;our&quot;). By
        accessing or using the Service, you agree to be bound by these Terms.
      </p>

      <h2>1. Acceptance of Terms</h2>
      <p>
        By creating an account or using the Service, you confirm that you are at
        least 18 years old and have the legal authority to enter into these
        Terms. If you are using the Service on behalf of an organization, you
        represent that you have authority to bind that organization to these
        Terms.
      </p>

      <h2>2. Description of Service</h2>
      <p>
        Citadel Cloud Management provides a SaaS platform featuring autonomous
        AI agents, multi-model orchestration, enterprise security tooling, and
        related infrastructure management capabilities. We reserve the right to
        modify, suspend, or discontinue any aspect of the Service at any time
        with reasonable notice.
      </p>

      <h2>3. User Accounts</h2>
      <ul>
        <li>
          You are responsible for maintaining the confidentiality of your account
          credentials and for all activities that occur under your account.
        </li>
        <li>
          You must provide accurate and complete registration information and
          keep it up to date.
        </li>
        <li>
          You must notify us immediately of any unauthorized use of your account.
        </li>
        <li>
          We reserve the right to suspend or terminate accounts that violate
          these Terms.
        </li>
      </ul>

      <h2>4. Acceptable Use</h2>
      <p>You agree not to:</p>
      <ul>
        <li>
          Use the Service for any unlawful purpose or in violation of any
          applicable laws or regulations.
        </li>
        <li>
          Attempt to gain unauthorized access to the Service, other accounts, or
          related systems.
        </li>
        <li>
          Transmit malware, viruses, or any code designed to disrupt or damage
          the Service.
        </li>
        <li>
          Reverse engineer, decompile, or disassemble any portion of the
          Service.
        </li>
        <li>
          Use the Service to send unsolicited communications or spam.
        </li>
        <li>
          Resell, sublicense, or redistribute the Service without written
          consent.
        </li>
      </ul>

      <h2>5. Intellectual Property</h2>
      <p>
        All intellectual property rights in the Service, including software,
        designs, trademarks, and documentation, are owned by Citadel Cloud
        Management or its licensors. You retain ownership of any data you upload
        to the Service. By using the Service, you grant us a limited license to
        process your data solely for the purpose of providing the Service.
      </p>

      <h2>6. Billing &amp; Payment</h2>
      <ul>
        <li>
          Paid plans are billed in advance on a monthly or annual basis, as
          selected during signup.
        </li>
        <li>
          All fees are non-refundable except as required by law or as explicitly
          stated in our refund policy.
        </li>
        <li>
          We may change pricing with at least 30 days&apos; notice before the
          next billing cycle.
        </li>
        <li>
          Failure to pay may result in suspension or termination of your
          account.
        </li>
      </ul>

      <h2>7. Termination</h2>
      <p>
        Either party may terminate these Terms at any time. You may cancel your
        account through the account settings or by contacting support. We may
        terminate or suspend your access immediately, without prior notice, for
        conduct that we determine violates these Terms or is harmful to other
        users or the Service. Upon termination, your right to use the Service
        ceases immediately. We will make your data available for export for 30
        days following termination.
      </p>

      <h2>8. Limitation of Liability</h2>
      <p>
        To the maximum extent permitted by applicable law, Citadel Cloud
        Management shall not be liable for any indirect, incidental, special,
        consequential, or punitive damages, or any loss of profits, revenue,
        data, or business opportunities arising out of or related to your use of
        the Service. Our total aggregate liability shall not exceed the amount
        you paid us in the 12 months preceding the claim.
      </p>

      <h2>9. Governing Law</h2>
      <p>
        These Terms are governed by and construed in accordance with the laws of
        the State of Delaware, United States, without regard to its conflict of
        law provisions. Any disputes arising from these Terms shall be resolved
        in the state or federal courts located in Delaware.
      </p>

      <h2>10. Contact</h2>
      <p>
        If you have questions about these Terms, please contact us:
      </p>
      <ul>
        <li>
          <strong>Email:</strong>{" "}
          <a href="mailto:legal@citadelcloudmanagement.com">
            legal@citadelcloudmanagement.com
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
