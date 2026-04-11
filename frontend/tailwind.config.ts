import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        ink: "#0b0f19",
        paper: "#111827",
        card: "#161d2e",
        card2: "#1c2537",
        edge: "#243044",
        edge2: "#2e3d56",
        cyan: "#22d3ee",
        orange: "#fb923c",
        green: "#4ade80",
        yellow: "#fbbf24",
        purple: "#a78bfa",
        red: "#f87171",
        white: "#f0f6ff",
        gray: "#64748b",
        gray2: "#94a3b8",
      },
      fontFamily: {
        syne: ["Syne", "sans-serif"],
        sans: ["DM Sans", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
    },
  },
  plugins: [],
};
export default config;
