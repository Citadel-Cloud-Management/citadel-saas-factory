import { ButtonHTMLAttributes, forwardRef } from "react";

type Variant = "primary" | "ghost" | "outline";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
  size?: "sm" | "md" | "lg";
}

const styles: Record<Variant, string> = {
  primary: "bg-cyan text-ink hover:opacity-90",
  ghost: "border border-edge bg-transparent text-white hover:border-edge2",
  outline: "border border-cyan text-cyan hover:bg-cyan hover:text-ink",
};

const sizes = { sm: "px-3 py-1.5 text-xs", md: "px-5 py-2.5 text-sm", lg: "px-8 py-3 text-base" };

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(({ variant = "primary", size = "md", className = "", ...props }, ref) => (
  <button ref={ref} className={`inline-flex items-center justify-center gap-2 font-semibold rounded-md transition-all duration-200 disabled:opacity-40 disabled:cursor-not-allowed ${styles[variant]} ${sizes[size]} ${className}`} {...props} />
));
Button.displayName = "Button";
