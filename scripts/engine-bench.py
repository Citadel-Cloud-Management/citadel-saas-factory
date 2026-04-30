#!/usr/bin/env python3
"""Benchmark LLM engine response time.

Measures latency and token counts for a given model/prompt combination.
Supports a --mock flag for CI environments without API keys.
"""

import argparse
import json
import sys
import time
from pathlib import Path


def run_mock_benchmark(model: str, prompt: str) -> dict:
    """Return synthetic benchmark results for CI without API keys."""
    start = time.perf_counter()
    # Simulate processing delay
    time.sleep(0.05)
    elapsed_ms = (time.perf_counter() - start) * 1000
    return {
        "model": model,
        "latency_ms": round(elapsed_ms, 2),
        "tokens": len(prompt.split()),
        "status": "ok",
        "mock": True,
    }


def run_api_benchmark(model: str, prompt: str) -> dict:
    """Call the model API and measure response latency."""
    try:
        import anthropic  # noqa: F811
    except ImportError:
        return {
            "model": model,
            "latency_ms": 0,
            "tokens": 0,
            "status": "error",
            "error": "anthropic package not installed",
        }

    try:
        client = anthropic.Anthropic()
        start = time.perf_counter()
        response = client.messages.create(
            model=model,
            max_tokens=256,
            messages=[{"role": "user", "content": prompt}],
        )
        elapsed_ms = (time.perf_counter() - start) * 1000

        input_tokens = getattr(response.usage, "input_tokens", 0)
        output_tokens = getattr(response.usage, "output_tokens", 0)

        return {
            "model": model,
            "latency_ms": round(elapsed_ms, 2),
            "tokens": input_tokens + output_tokens,
            "status": "ok",
        }
    except Exception as exc:
        return {
            "model": model,
            "latency_ms": 0,
            "tokens": 0,
            "status": "error",
            "error": str(exc),
        }


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark LLM engine response time")
    parser.add_argument(
        "--model",
        default="claude-sonnet-4-6",
        help="Model identifier to benchmark",
    )
    parser.add_argument(
        "--prompt",
        default="Explain the CAP theorem in one sentence.",
        help="Prompt to send to the model",
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Use mock results instead of calling the API",
    )
    parser.add_argument(
        "--engine",
        default="paid",
        help="Engine tier label (paid, free, local)",
    )
    parser.add_argument(
        "--out",
        default=None,
        help="Write JSON results to this file instead of stdout",
    )
    parser.add_argument(
        "--dimensions",
        default=None,
        help="Comma-separated benchmark dimensions (currently informational)",
    )
    args = parser.parse_args()

    if args.mock:
        result = run_mock_benchmark(args.model, args.prompt)
    else:
        result = run_api_benchmark(args.model, args.prompt)

    result["engine"] = args.engine

    output = json.dumps(result, indent=2)

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output + "\n", encoding="utf-8")
    else:
        print(output)

    if result["status"] != "ok":
        sys.exit(1)


if __name__ == "__main__":
    main()
