import { test, expect } from "@playwright/test";

const BASE_URL = process.env.BASE_URL || "http://localhost:3000";

test.describe("Authentication Flow", () => {
  test("signup creates account and redirects to dashboard", async ({ page }) => {
    await page.goto(`${BASE_URL}/signup`);

    await page.fill('input[type="text"]', "Test User");
    await page.fill('input[type="email"]', `test-${Date.now()}@example.com`);
    await page.fill('input[type="password"]', "SecurePass123!");
    await page.click('button[type="submit"]');

    // Should redirect to dashboard after successful signup
    await expect(page).toHaveURL(/\/dashboard/, { timeout: 10000 });
  });

  test("login with valid credentials redirects to dashboard", async ({ page }) => {
    await page.goto(`${BASE_URL}/login`);

    await page.fill('input[type="email"]', "admin@citadel.test");
    await page.fill('input[type="password"]', "admin123");
    await page.click('button[type="submit"]');

    await expect(page).toHaveURL(/\/dashboard/, { timeout: 10000 });
  });

  test("login with invalid credentials shows error", async ({ page }) => {
    await page.goto(`${BASE_URL}/login`);

    await page.fill('input[type="email"]', "wrong@example.com");
    await page.fill('input[type="password"]', "wrongpass");
    await page.click('button[type="submit"]');

    await expect(page.locator("text=Invalid credentials")).toBeVisible({ timeout: 5000 });
  });

  test("unauthenticated user is redirected from dashboard to login", async ({ page }) => {
    await page.goto(`${BASE_URL}/dashboard`);
    await expect(page).toHaveURL(/\/login/);
  });
});
