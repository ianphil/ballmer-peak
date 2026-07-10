"""Aggregate benchmark runs into Ballmer metrics."""

from __future__ import annotations

from collections import defaultdict
from typing import Any


def summarize(runs: list[dict[str, Any]]) -> dict[str, Any]:
    """Calculate curve statistics from individual runs."""
    grouped: dict[float, list[float]] = defaultdict(list)
    for run in runs:
        grouped[float(run["bac"])].append(float(run["score"]))

    curve = [
        {
            "bac": bac,
            "mean_score": round(sum(scores) / len(scores), 2),
            "runs": len(scores),
        }
        for bac, scores in sorted(grouped.items())
    ]
    if not curve:
        raise ValueError("At least one run is required")

    peak = max(curve, key=lambda point: (point["mean_score"], point["bac"]))
    confidence_cliff = None
    for point in curve:
        if point["bac"] > peak["bac"] and point["mean_score"] <= peak["mean_score"] - 25:
            confidence_cliff = point["bac"]
            break

    windows_me_events = sum(
        1 for run in runs if float(run["bac"]) >= 0.14 and float(run["score"]) < 25
    )
    return {
        "curve": curve,
        "peak_bac": peak["bac"],
        "peak_score": peak["mean_score"],
        "confidence_cliff": confidence_cliff,
        "windows_me_events": windows_me_events,
    }
