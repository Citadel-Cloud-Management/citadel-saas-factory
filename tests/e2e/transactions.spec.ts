import { test, expect } from "@playwright/test";

const BASE_URL = process.env.BASE_URL || "http://localhost:3000";

test.describe("Transaction Flow", () => {
  test.beforeEach(async ({ page }) => {
    // Login first
    await page.goto(`${BASE_URL}/login`);
    await page.fill('input[type="email"]', "admin@citadel.test");
    await page.fill('input[type="password"]', "admin123");
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/\/dashboard/, { timeout: 10000 });
  });

  test("dashboard displays account balances", async ({ page }) => {
    await page.goto(`${BASE_URL}/dashboard`);
    await expect(page.locator("text=Total Balance")).toBeVisible();
  });

  test("accounts page shows account cards", async ({ page }) => {
    await page.goto(`${BASE_URL}/dashboard/accounts`);
    await expect(page.locator("text=Accounts")).toBeVisible();
  });

  test("transactions page shows transaction history", async ({ page }) => {
    await page.goto(`${BASE_URL}/dashboard/transactions`);
    await expect(page.locator("text=Transactions")).toBeVisible();
    await expect(page.locator("text=Total Volume")).toBeVisible();
    await expect(page.locator("text=Success Rate")).toBeVisible();
  });

  test("compliance page shows KYC status", async ({ page }) => {
    await page.goto(`${BASE_URL}/dashboard/compliance`);
    await expect(page.locator("text=Compliance")).toBeVisible();
    await expect(page.locator("text=KYC Level")).toBeVisible();
    await expect(page.locator("text=All Systems Operational")).toBeVisible();
  });

  test("settings page shows billing plan", async ({ page }) => {
    await page.goto(`${BASE_URL}/dashboard/settings`);
    await expect(page.locator("text=Settings")).toBeVisible();
    await expect(page.locator("text=API Keys")).toBeVisible();
  });
});
