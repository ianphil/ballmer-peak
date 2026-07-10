"""Command-line interface for the Ballmer Peak eval."""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Sequence

from .impairment import PROFILES
from .report import render_report
from .runner import run_eval
from .scoring import summarize


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ballmer",
        description="Evaluate coding agents across the Behavioral Ambiguity Coefficient.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    demo = subparsers.add_parser("demo", help="render a deterministic synthetic curve")
    demo.add_argument("--output", type=Path)

    run = subparsers.add_parser("run", help="run an agent against an eval")
    run.add_argument("--eval", dest="eval_dir", required=True, type=Path)
    run.add_argument("--agent-command", required=True)
    run.add_argument(
        "--levels",
        default=",".join(f"{profile.bac:.2f}" for profile in PROFILES),
        help="comma-separated BAC values",
    )
    run.add_argument("--repetitions", type=int, default=1)
    run.add_argument("--timeout", type=int, default=120)
    run.add_argument("--output", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    if args.command == "demo":
        runs = _demo_runs()
    else:
        if args.repetitions < 1:
            raise SystemExit("--repetitions must be at least 1")
        levels = [float(value.strip()) for value in args.levels.split(",")]
        runs = run_eval(
            args.eval_dir.resolve(),
            args.agent_command,
            levels,
            args.repetitions,
            args.timeout,
        )

    summary = summarize(runs)
    print(render_report(summary))
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps({"summary": summary, "runs": runs}, indent=2) + "\n",
            encoding="utf-8",
        )


def _demo_runs() -> list[dict[str, float | int]]:
    randomizer = random.Random(1975)
    expected = {
        0.00: 78,
        0.03: 84,
        0.06: 92,
        0.10: 73,
        0.14: 41,
        0.20: 12,
    }
    return [
        {
            "bac": bac,
            "trial": trial,
            "score": max(0, min(100, base + randomizer.randint(-4, 4))),
        }
        for bac, base in expected.items()
        for trial in range(5)
    ]


if __name__ == "__main__":
    main()
