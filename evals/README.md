# Evals — Model Evaluation Framework

Continuous evaluation of agent quality using DeepEval and promptfoo.

## Tools

| Tool | Config | Purpose |
|------|--------|---------|
| DeepEval | `deepeval/config.yaml` | Hallucination, factuality, toxicity, PII detection |
| promptfoo | `promptfoo.yaml` | Prompt regression testing, A/B comparisons |

## Run Evaluations

```bash
# DeepEval
cd evals && deepeval test run

# promptfoo
npx promptfoo eval --config evals/promptfoo.yaml
npx promptfoo view  # Open results dashboard
```

## CI Integration

Evaluations run automatically in `.github/workflows/eval-models.yml` on every PR that modifies agent prompts or model configuration.

## Add a Test Case

1. Add test to `deepeval/config.yaml`
2. Define expected output and metrics
3. Run locally, verify, commit
