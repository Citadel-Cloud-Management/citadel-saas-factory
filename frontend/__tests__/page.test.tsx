import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import HomePage from "../app/page";

// Mock next/link since it requires the Next.js runtime
vi.mock("next/link", () => ({
  __esModule: true,
  default: ({
    children,
    href,
  }: {
    children: React.ReactNode;
    href: string;
  }) => <a href={href}>{children}</a>,
}));

describe("HomePage", () => {
  it('renders the heading "Citadel SaaS Factory"', () => {
    render(<HomePage />);
    const heading = screen.getByRole("heading", {
      name: /Citadel SaaS Factory/i,
    });
    expect(heading).toBeDefined();
  });

  it("renders the Get Started link", () => {
    render(<HomePage />);
    const links = screen.getAllByText(/Get Started/i);
    expect(links.length).toBeGreaterThan(0);
  });

  it("renders the feature cards", () => {
    render(<HomePage />);
    expect(screen.getByText(/500\+ Agents/i)).toBeDefined();
    expect(screen.getByText(/Multi-Model AI/i)).toBeDefined();
    expect(screen.getByText(/Enterprise Security/i)).toBeDefined();
    expect(screen.getByText(/Zero Lock-in/i)).toBeDefined();
  });
});
