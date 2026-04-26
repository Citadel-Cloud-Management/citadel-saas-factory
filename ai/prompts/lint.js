#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "../..");
const PROMPTS_DIR = path.join(ROOT, "ai", "prompts");

const REQUIRED_FM_FIELDS = ["name", "version", "description"];
const VARIABLE_PATTERN = /\{\{(\w+)\}\}/g;

let errors = 0;
let warnings = 0;
let checked = 0;

function log(level, file, msg) {
  const rel = path.relative(ROOT, file);
  if (level === "error") {
    console.error(`  ✗ ${rel}: ${msg}`);
    errors++;
  } else {
    console.warn(`  ⚠ ${rel}: ${msg}`);
    warnings++;
  }
}

function parseFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (!match) return null;

  const fm = {};
  for (const line of match[1].split("\n")) {
    const colon = line.indexOf(":");
    if (colon > 0) {
      const key = line.slice(0, colon).trim();
      const val = line.slice(colon + 1).trim().replace(/^["']|["']$/g, "");
      fm[key] = val;
    }
  }
  return { frontmatter: fm, body: match[2] };
}

function lintFile(filePath) {
  const content = fs.readFileSync(filePath, "utf8");
  checked++;

  if (!content.startsWith("---\n")) {
    log("error", filePath, "missing frontmatter (must start with ---)");
    return;
  }

  const parsed = parseFrontmatter(content);
  if (!parsed) {
    log("error", filePath, "malformed frontmatter (no closing ---)");
    return;
  }

  for (const field of REQUIRED_FM_FIELDS) {
    if (!parsed.frontmatter[field]) {
      log("error", filePath, `missing required frontmatter field: ${field}`);
    }
  }

  if (parsed.frontmatter.version && !/^\d+\.\d+\.\d+$/.test(parsed.frontmatter.version)) {
    log("warn", filePath, `version "${parsed.frontmatter.version}" is not semver`);
  }

  if (parsed.body.trim().length === 0) {
    log("error", filePath, "prompt body is empty");
  }

  if (filePath.includes(path.join("prompts", "tasks"))) {
    const usedVars = [];
    let match;
    while ((match = VARIABLE_PATTERN.exec(parsed.body)) !== null) {
      if (!usedVars.includes(match[1])) usedVars.push(match[1]);
    }

    if (usedVars.length === 0 && parsed.body.length > 100) {
      log("warn", filePath, "task prompt has no {{variable}} slots");
    }
  }
}

function walkDir(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      walkDir(full);
    } else if (entry.name.endsWith(".md")) {
      lintFile(full);
    }
  }
}

console.log("\n  Citadel AI Prompt Linter\n");

if (!fs.existsSync(PROMPTS_DIR)) {
  console.error(`  ✗ Prompts directory not found: ${PROMPTS_DIR}`);
  process.exit(1);
}

walkDir(PROMPTS_DIR);

console.log(`\n  Checked: ${checked}  Errors: ${errors}  Warnings: ${warnings}\n`);

if (errors > 0) {
  process.exit(1);
}
