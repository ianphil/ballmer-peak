"""Human-readable Ballmer Peak reports."""

from __future__ import annotations

from typing import Any


def render_report(summary: dict[str, Any]) -> str:
    """Render a compact terminal report."""
    lines = [
        "BALLMER PEAK EVALUATION",
        "=======================",
        "",
        "BAC    MEAN SCORE    CURVE",
    ]
    for point in summary["curve"]:
        score = point["mean_score"]
        bar = "#" * round(score / 5)
        lines.append(f"{point['bac']:>4.2f}   {score:>6.2f}        {bar}")

    cliff = summary["confidence_cliff"]
    lines.extend(
        [
            "",
            f"Peak BAC:          {summary['peak_bac']:.2f}",
            f"Peak score:        {summary['peak_score']:.2f}",
            f"Confidence cliff:  {cliff:.2f}" if cliff is not None else "Confidence cliff:  not observed",
            f"Windows ME events: {summary['windows_me_events']}",
        ]
    )
    return "\n".join(lines)
