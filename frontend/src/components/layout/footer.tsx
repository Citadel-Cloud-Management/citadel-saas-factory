import Link from "next/link";

const links = {
  Platform: [
    { label: "Products", href: "/products" },
    { label: "Courses", href: "/courses" },
    { label: "Pricing", href: "/pricing" },
  ],
  Resources: [
    { label: "About", href: "/about" },
    { label: "Contact", href: "/contact" },
    { label: "Blog", href: "/blog" },
  ],
  Legal: [
    { label: "Privacy", href: "/privacy" },
    { label: "Terms", href: "/terms" },
    { label: "Refunds", href: "/refunds" },
  ],
};

export function Footer() {
  return (
    <footer className="bg-ink border-t border-edge py-16">
      <div className="max-w-7xl mx-auto px-4 grid grid-cols-1 md:grid-cols-4 gap-12">
        <div>
          <div className="flex items-center gap-2 mb-4">
            <span className="w-8 h-8 bg-cyan rounded-md flex items-center justify-center text-ink font-bold text-sm">C</span>
            <span className="text-white font-semibold">Citadel Cloud</span>
          </div>
          <p className="text-gray text-sm leading-relaxed">Global premier cloud career platform. Build skills, earn certifications, launch your cloud career.</p>
          <p className="text-gray text-xs mt-4">citadelcloudmanagement@gmail.com</p>
        </div>
        {Object.entries(links).map(([title, items]) => (
          <div key={title}>
            <h4 className="text-white text-sm font-semibold mb-4 uppercase tracking-wider">{title}</h4>
            <ul className="space-y-2">
              {items.map((item) => (
                <li key={item.href}>
                  <Link href={item.href} className="text-gray text-sm hover:text-cyan transition-colors">{item.label}</Link>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
      <div className="max-w-7xl mx-auto px-4 mt-12 pt-8 border-t border-edge text-center">
        <p className="text-gray text-xs">&copy; 2026 Citadel Cloud Management. All rights reserved.</p>
      </div>
    </footer>
  );
}
