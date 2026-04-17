"""CLI entry point — run the backbone from the command line.

Usage:
    python -m backbone.cli run "Analyze competitor pricing"
    python -m backbone.cli health
    python -m backbone.cli agents
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from dataclasses import asdict

from backbone.orchestrator.supervisor import AutonomyLevel
from backbone.runtime.engine import BackboneEngine


def main() -> None:
    parser = argparse.ArgumentParser(description="Citadel Agent Backbone CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # run
    run_parser = subparsers.add_parser("run", help="Execute a goal")
    run_parser.add_argument("goal", help="The goal to execute")
    run_parser.add_argument(
        "--autonomy",
        choices=[a.name.lower() for a in AutonomyLevel],
        default="approval_gate",
        help="Autonomy level (default: approval_gate)",
    )
    run_parser.add_argument(
        "--registry",
        default=".claude/agents/_registry.yaml",
        help="Path to agent registry",
    )

    # health
    subparsers.add_parser("health", help="Check backbone health")

    # agents
    subparsers.add_parser("agents", help="List registered agents")

    args = parser.parse_args()

    if args.command == "run":
        level = AutonomyLevel[args.autonomy.upper()]
        engine = BackboneEngine.create(
            registry_path=args.registry,
            autonomy_level=level,
        )
        result = asyncio.run(engine.run(args.goal))
        print(json.dumps({
            "run_id": result.run_id,
            "goal": result.goal,
            "status": result.status,
            "total_steps": result.total_steps,
            "completed_steps": result.completed_steps,
            "errors": list(result.errors),
        }, indent=2))

    elif args.command == "health":
        engine = BackboneEngine.create()
        health = asyncio.run(engine.health())
        print(json.dumps(health, indent=2, default=str))

    elif args.command == "agents":
        from backbone.agents.registry import load_registry

        router = load_registry()
        agents = router.list_agents()
        total = sum(len(v) for v in agents.values())
        print(f"Registered agents: {total}")
        for domain, types in sorted(agents.items()):
            print(f"  {domain}: {len(types)} agents")
            for t in types[:5]:
                print(f"    - {t}")
            if len(types) > 5:
                print(f"    ... and {len(types) - 5} more")


if __name__ == "__main__":
    main()
