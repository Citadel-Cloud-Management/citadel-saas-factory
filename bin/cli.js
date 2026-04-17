#!/usr/bin/env node

const { execFileSync } = require("child_process");
const fs = require("fs");
const path = require("path");

const VERSION = "3.1.0";
const REPO_URL =
  "https://github.com/Citadel-Cloud-Management/citadel-saas-factory.git";

const HELP = `
Citadel SaaS Factory v${VERSION}
Universal Full-Stack SaaS Production Framework — 265 Autonomous Business Agents

Usage:
  citadel-factory init [directory]    Scaffold a new project
  citadel-factory bootstrap           Run parallel bootstrap in current project
  citadel-factory detect              Detect business vertical
  citadel-factory status              Show system status
  citadel-factory verify              Run installation verification
  citadel-factory --version           Show version
  citadel-factory --help              Show this help

Examples:
  npx @citadel-cloud/saas-factory init my-saas
  npx @citadel-cloud/saas-factory init .
  cd my-saas && citadel-factory bootstrap
`;

function run(command, args, opts = {}) {
  try {
    execFileSync(command, args, { stdio: "inherit", ...opts });
  } catch {
    process.exit(1);
  }
}

function init(targetDir) {
  const dest = path.resolve(targetDir);
  const name = path.basename(dest);

  if (
    fs.existsSync(dest) &&
    fs.readdirSync(dest).length > 0 &&
    targetDir !== "."
  ) {
    console.error(
      `Error: Directory '${targetDir}' already exists and is not empty.`
    );
    process.exit(1);
  }

  console.log(`\n  Citadel SaaS Factory v${VERSION}`);
  console.log(`  Scaffolding into: ${dest}\n`);

  if (targetDir === ".") {
    console.log("  Initializing in current directory...\n");
    run("git", ["clone", REPO_URL, "__citadel_tmp__"]);
    const tmpDir = path.resolve("__citadel_tmp__");
    const entries = fs.readdirSync(tmpDir);
    for (const entry of entries) {
      if (entry === ".git") continue;
      const src = path.join(tmpDir, entry);
      const dst = path.join(dest, entry);
      if (!fs.existsSync(dst)) {
        fs.renameSync(src, dst);
      }
    }
    fs.rmSync(tmpDir, { recursive: true, force: true });
    run("git", ["init"], { cwd: dest });
  } else {
    run("git", ["clone", REPO_URL, dest]);
    try {
      execFileSync("git", ["remote", "remove", "origin"], {
        cwd: dest,
        stdio: "ignore",
      });
    } catch {
      // origin may not exist, ignore
    }
  }

  console.log("\n  Project scaffolded successfully!\n");
  console.log("  Next steps:\n");
  if (targetDir !== ".") {
    console.log(`    cd ${name}`);
  }
  console.log("    cp .env.example .env       # Set your API keys");
  console.log("    ./scripts/parallel-bootstrap.sh");
  console.log(
    "    claude                      # Or open in Cursor, Copilot, Codex, Jules...\n"
  );
}

function requireProject(scriptName) {
  if (!fs.existsSync(scriptName)) {
    console.error("Error: Not in a Citadel SaaS Factory project directory.");
    process.exit(1);
  }
}

function bootstrap() {
  requireProject("scripts/parallel-bootstrap.sh");
  run("bash", ["scripts/parallel-bootstrap.sh"]);
}

function detect() {
  requireProject("scripts/detect-business.sh");
  run("bash", ["scripts/detect-business.sh"]);
}

function status() {
  requireProject(".claude/agents/_registry.yaml");
  console.log("\n  === Citadel SaaS Factory Status ===\n");

  const count = (file, pattern) => {
    try {
      const content = fs.readFileSync(file, "utf8");
      return (content.match(new RegExp(pattern, "gm")) || []).length;
    } catch {
      return 0;
    }
  };

  const dirCount = (pattern) => {
    try {
      const dir = path.dirname(pattern);
      const ext = path.extname(pattern);
      return fs
        .readdirSync(dir)
        .filter((f) => f.endsWith(ext)).length;
    } catch {
      return 0;
    }
  };

  console.log(
    `  Agents:    ${count(".claude/agents/_registry.yaml", "^  - id:")}`
  );
  console.log(`  Models:    ${count("models/catalog.yaml", "    - id:")}`);
  console.log(`  Rules:     ${dirCount(".claude/rules/*.md")}`);
  console.log(`  Providers: ${dirCount("agents/providers/*.yaml")}`);
  console.log(`  Scripts:   ${dirCount("scripts/*.sh")}`);
  console.log("");
}

function verify() {
  requireProject("scripts/verify-install.sh");
  run("bash", ["scripts/verify-install.sh"]);
}

// --- Main ---
const args = process.argv.slice(2);
const command = args[0];

switch (command) {
  case "init":
    init(args[1] || "citadel-saas-factory");
    break;
  case "bootstrap":
    bootstrap();
    break;
  case "detect":
    detect();
    break;
  case "status":
    status();
    break;
  case "verify":
    verify();
    break;
  case "--version":
  case "-v":
    console.log(VERSION);
    break;
  case "--help":
  case "-h":
  case undefined:
    console.log(HELP);
    break;
  default:
    console.error(`Unknown command: ${command}`);
    console.log(HELP);
    process.exit(1);
}
