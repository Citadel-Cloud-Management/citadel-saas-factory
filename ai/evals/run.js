#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

// ─── Paths ───
const ROOT = path.resolve(__dirname, "../..");
const AI_DIR = path.join(ROOT, "ai");
const TESTS_DIR = path.join(AI_DIR, "evals", "tests");
const TRACES_DIR = path.join(AI_DIR, "evals", "traces");
const SCORECARDS_DIR = path.join(AI_DIR, "evals", "scorecards");
const PROMPTS_DIR = path.join(AI_DIR, "prompts");

// ─── Parse args ───
const args = process.argv.slice(2);
const flags = {};
for (let i = 0; i < args.length; i++) {
  if (args[i] === "--id" && args[i + 1]) flags.id = args[++i];
  else if (args[i] === "--tag" && args[i + 1]) flags.tag = args[++i];
  else if (args[i] === "--file" && args[i + 1]) flags.file = args[++i];
  else if (args[i] === "--dry-run") flags.dryRun = true;
  else if (args[i] === "--verbose") flags.verbose = true;
  else if (args[i] === "--mock") flags.mock = true;
  else if (args[i] === "--help" || args[i] === "-h") {
    printHelp();
    process.exit(0);
  }
}

function printHelp() {
  console.log(`
ai/evals/run.js — Citadel AI Eval Runner

Usage:
  node ai/evals/run.js                  Run all tests in ai/evals/tests/
  node ai/evals/run.js --id sum-001     Run a single test by ID
  node ai/evals/run.js --tag tool-use   Run all tests matching a tag
  node ai/evals/run.js --file my.json   Run tests from a specific file
  node ai/evals/run.js --dry-run        Parse and validate tests without calling the API
  node ai/evals/run.js --mock           Run with mock LLM responses (no API key needed)
  node ai/evals/run.js --verbose        Print full request/response payloads

Environment:
  ANTHROPIC_API_KEY    Required unless --mock is used
  AI_EVAL_MODEL        Model override (default: claude-sonnet-4-6)
  AI_EVAL_THRESHOLD    Score threshold override (default: 0.85)
`);
}

// ─── Load tests ───
function loadTests() {
  let tests = [];

  if (flags.file) {
    // Single file mode
    const testFile = path.resolve(flags.file);
    if (!fs.existsSync(testFile)) {
      console.error(`Test file not found: ${testFile}`);
      process.exit(1);
    }
    try {
      const parsed = JSON.parse(fs.readFileSync(testFile, "utf8"));
      if (!Array.isArray(parsed)) {
        console.error(`Test file must contain a JSON array: ${testFile}`);
        process.exit(1);
      }
      tests = parsed;
    } catch (err) {
      console.error(`Invalid JSON in ${testFile}: ${err.message}`);
      process.exit(1);
    }
  } else {
    // Load ALL .json files from the tests directory
    if (!fs.existsSync(TESTS_DIR)) {
      console.error(`Tests directory not found: ${TESTS_DIR}`);
      process.exit(1);
    }
    const files = fs.readdirSync(TESTS_DIR)
      .filter((f) => f.endsWith(".json"))
      .sort();
    if (files.length === 0) {
      console.error(`No test files found in ${TESTS_DIR}`);
      process.exit(1);
    }
    for (const file of files) {
      const filePath = path.join(TESTS_DIR, file);
      try {
        const parsed = JSON.parse(fs.readFileSync(filePath, "utf8"));
        if (Array.isArray(parsed)) {
          tests.push(...parsed);
        }
      } catch (err) {
        console.error(`Invalid JSON in ${filePath}: ${err.message}`);
        process.exit(1);
      }
    }
  }

  if (flags.id) tests = tests.filter((t) => t.id === flags.id);
  if (flags.tag) tests = tests.filter((t) => t.tags && t.tags.includes(flags.tag));

  return tests;
}

// ─── Prompt loader ───
function loadPrompt(promptPath) {
  const full = path.join(ROOT, promptPath);
  if (!fs.existsSync(full)) return null;

  const raw = fs.readFileSync(full, "utf8");
  const fmMatch = raw.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (!fmMatch) return { frontmatter: {}, body: raw };

  const frontmatter = {};
  for (const line of fmMatch[1].split("\n")) {
    const colon = line.indexOf(":");
    if (colon > 0) {
      frontmatter[line.slice(0, colon).trim()] = line.slice(colon + 1).trim().replace(/^["']|["']$/g, "");
    }
  }
  return { frontmatter, body: fmMatch[2] };
}

// ─── Template renderer ───
function renderTemplate(template, variables) {
  return template.replace(/\{\{(\w+)\}\}/g, (_, key) =>
    variables[key] !== undefined ? String(variables[key]) : `{{${key}}}`
  );
}

// ─── Mock LLM ───
function mockLLMCall(test) {
  const input = test.input;
  const expected = test.expected_output || {};

  // Summarization tests (have document_text)
  if (input.document_text !== undefined) {
    const points = [];
    if (input.document_text.length > 0) {
      const sentences = input.document_text.split(". ").filter(Boolean);
      const max = Math.min(input.max_points || 5, sentences.length);
      for (let i = 0; i < max; i++) {
        points.push({
          point: sentences[i].trim().replace(/\.$/, ""),
          source_ref: `sentence-${i + 1}`,
          confidence: i === 0 ? "HIGH" : i === 1 ? "MEDIUM" : "LOW",
        });
      }
    }
    return {
      summary: points,
      total_points: points.length,
      document_length_chars: (input.document_text || "").length,
    };
  }

  // Search/tool tests (have query)
  if (input.query !== undefined) {
    return {
      results: [
        {
          title: `Result for: ${input.query}`,
          url: "https://example.com/result",
          snippet: `Mock result matching query "${input.query}"`,
        },
      ],
    };
  }

  // Council / generic tests — build mock output that includes expected
  // sections and concepts so the scorer can verify the pipeline works
  const sections = [];
  if (expected.must_contain_sections) {
    for (const section of expected.must_contain_sections) {
      sections.push({
        agent: section,
        analysis: `Mock ${section} analysis for ${input.task || "unknown task"}`,
        findings: [`${section} finding 1`, `${section} finding 2`],
      });
    }
  }

  const body = { sections, _mock: true };

  // Inject expected concepts as keywords so accuracy scoring picks them up
  if (expected.must_contain_concepts) {
    body.concepts = expected.must_contain_concepts.map((c) => ({
      name: c,
      present: true,
    }));
  }

  // Add verdict/findings for validation-type tests
  if (test.tags && test.tags.includes("validation")) {
    body.verdict = "SHIP WITH CONDITIONS";
    body.findings = [
      { id: "M1", severity: "MEDIUM", category: "mock", location: "mock.py:1" },
    ];
  }

  return body;
}

// ─── Real LLM call ───
async function callLLM(systemPrompt, userMessage, model) {
  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) {
    console.error("ANTHROPIC_API_KEY not set. Use --mock for testing without an API key.");
    process.exit(1);
  }

  const body = JSON.stringify({
    model: model || process.env.AI_EVAL_MODEL || "claude-sonnet-4-6",
    max_tokens: 4096,
    system: systemPrompt,
    messages: [{ role: "user", content: userMessage }],
  });

  // Use Node 18+ native fetch
  const resp = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-api-key": apiKey,
      "anthropic-version": "2023-06-01",
    },
    body,
  });

  if (!resp.ok) {
    const errText = await resp.text();
    throw new Error(`Anthropic API ${resp.status}: ${errText}`);
  }

  const data = await resp.json();
  return data.content[0].text;
}

// ─── Scorer ───
function scoreResult(test, output) {
  const scores = { accuracy: 0, format: 0, tool_use: 0, latency: 0 };
  const criteria = test.pass_criteria;
  const expected = test.expected_output;

  // Accuracy: check must_contain_sections, must_contain_concepts, or min_results
  let accuracyChecks = 0;
  let accuracyTotal = 0;

  if (expected.must_contain_sections) {
    const text = JSON.stringify(output).toLowerCase();
    const found = expected.must_contain_sections.filter((s) =>
      text.includes(s.toLowerCase())
    );
    accuracyChecks++;
    accuracyTotal += (found.length / expected.must_contain_sections.length) * 10;
  }

  if (expected.must_contain_concepts) {
    const text = JSON.stringify(output).toLowerCase();
    const found = expected.must_contain_concepts.filter((c) =>
      text.includes(c.toLowerCase())
    );
    accuracyChecks++;
    accuracyTotal += (found.length / expected.must_contain_concepts.length) * 10;
  }

  if (accuracyChecks > 0) {
    scores.accuracy = accuracyTotal / accuracyChecks;
  } else if (expected.error_or_empty) {
    const arr = output.summary || output.results || [];
    scores.accuracy = arr.length === 0 ? 10 : 3;
  } else if (expected.min_results !== undefined) {
    const results = output.results || [];
    scores.accuracy = results.length >= expected.min_results ? 10 : 2;
  } else {
    scores.accuracy = 5; // no expected output to compare
  }

  // Format: is it valid JSON / has expected shape
  try {
    if (typeof output === "object" && output !== null) {
      scores.format = 10;
      if (expected.summary_length !== undefined) {
        const actual = (output.summary || []).length;
        if (actual !== expected.summary_length && !expected.error_or_empty) {
          scores.format = 6;
        }
      }
    } else {
      scores.format = 2;
    }
  } catch {
    scores.format = 0;
  }

  // Tool use: tag-based heuristic
  if (test.tags.includes("tool-use")) {
    const hasResults = output.results && output.results.length > 0;
    scores.tool_use = hasResults ? 10 : 2;
  } else {
    scores.tool_use = 10; // not a tool test
  }

  // Latency: scored by the caller based on elapsed time
  scores.latency = 10; // placeholder, overwritten by runner

  return scores;
}

function compositeScore(scores) {
  return (
    scores.accuracy * 0.4 +
    scores.format * 0.25 +
    scores.tool_use * 0.2 +
    scores.latency * 0.15
  );
}

function verdict(composite) {
  if (composite >= 7.0) return "PASS";
  if (composite >= 5.0) return "WARN";
  return "FAIL";
}

// ─── Write trace ───
function writeTrace(test, output, scores, elapsed, composite) {
  const trace = {
    id: test.id,
    timestamp: new Date().toISOString(),
    model: process.env.AI_EVAL_MODEL || "claude-sonnet-4-6",
    mode: flags.mock ? "mock" : "live",
    input: test.input,
    output,
    scores,
    composite: Math.round(composite * 100) / 100,
    verdict: verdict(composite),
    elapsed_ms: elapsed,
    latency_budget_ms: test.pass_criteria.latency_budget_ms || null,
  };

  const traceFile = path.join(
    TRACES_DIR,
    `${test.id}_${Date.now()}.json`
  );
  fs.writeFileSync(traceFile, JSON.stringify(trace, null, 2));
  return traceFile;
}

// ─── Main ───
async function main() {
  const tests = loadTests();

  if (tests.length === 0) {
    console.log("No tests matched the filter.");
    process.exit(0);
  }

  console.log(`\n  Citadel AI Eval Runner`);
  console.log(`  Mode: ${flags.mock || flags.dryRun ? (flags.dryRun ? "dry-run" : "mock") : "live"}`);
  console.log(`  Tests: ${tests.length}\n`);

  if (flags.dryRun) {
    for (const test of tests) {
      console.log(`  [DRY] ${test.id} — ${test.description}`);
      console.log(`         tags: ${(test.tags || []).join(", ")}`);
      console.log(`         criteria: ${Object.keys(test.pass_criteria).join(", ")}`);
    }
    console.log(`\n  ${tests.length} test(s) validated. No API calls made.\n`);
    return;
  }

  // Load system prompt
  const systemPromptData = loadPrompt("ai/prompts/system/base.md");
  const systemPrompt = systemPromptData ? systemPromptData.body : "You are a helpful assistant.";

  const results = [];

  for (const test of tests) {
    const start = Date.now();
    let output;

    try {
      if (flags.mock) {
        output = mockLLMCall(test);
      } else {
        const userMsg = `Run this test:\n\n${JSON.stringify(test.input, null, 2)}\n\nRespond with valid JSON only. No markdown fences.`;
        const raw = await callLLM(systemPrompt, userMsg);
        if (flags.verbose) console.log(`  [RAW] ${raw.slice(0, 200)}...`);
        output = JSON.parse(raw);
      }
    } catch (err) {
      output = { error: err.message };
    }

    const elapsed = Date.now() - start;
    const scores = scoreResult(test, output);

    // Score latency based on budget
    const budget = test.pass_criteria.latency_budget_ms || 5000;
    if (elapsed <= budget * 0.5) scores.latency = 10;
    else if (elapsed <= budget * 0.75) scores.latency = 8;
    else if (elapsed <= budget) scores.latency = 6;
    else if (elapsed <= budget * 2) scores.latency = 3;
    else scores.latency = 0;

    const comp = compositeScore(scores);
    const v = verdict(comp);
    const traceFile = writeTrace(test, output, scores, elapsed, comp);

    const icon = v === "PASS" ? "✓" : v === "WARN" ? "⚠" : "✗";
    console.log(
      `  ${icon} ${test.id.padEnd(12)} ${v.padEnd(6)} ${comp.toFixed(1).padStart(4)}/10  ${elapsed}ms  ${test.description}`
    );

    if (flags.verbose) {
      console.log(`    scores: acc=${scores.accuracy} fmt=${scores.format} tool=${scores.tool_use} lat=${scores.latency}`);
      console.log(`    trace:  ${path.relative(ROOT, traceFile)}`);
    }

    results.push({ test: test.id, verdict: v, composite: comp });
  }

  // Summary
  const passed = results.filter((r) => r.verdict === "PASS").length;
  const warned = results.filter((r) => r.verdict === "WARN").length;
  const failed = results.filter((r) => r.verdict === "FAIL").length;

  console.log(`\n  ━━━ Results: ${passed} passed, ${warned} warned, ${failed} failed ━━━\n`);

  if (failed > 0) process.exit(1);
}

main().catch((err) => {
  console.error(`Fatal: ${err.message}`);
  process.exit(1);
});
