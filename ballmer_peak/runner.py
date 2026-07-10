"""Execute coding agents against Ballmer Peak evals."""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from .impairment import impair_prompt


def run_eval(
    eval_dir: Path,
    agent_command: str,
    levels: list[float],
    repetitions: int,
    timeout: int,
) -> list[dict[str, Any]]:
    """Run an eval at every requested BAC level."""
    task = json.loads((eval_dir / "task.json").read_text(encoding="utf-8"))
    source_repo = eval_dir / "repo"
    grader = eval_dir / "grader.py"
    runs: list[dict[str, Any]] = []

    for bac in levels:
        for trial in range(repetitions):
            prompt = impair_prompt(task["prompt"], bac, trial)
            with tempfile.TemporaryDirectory(prefix="ballmer-") as temp:
                temp_dir = Path(temp)
                workspace = temp_dir / "workspace"
                prompt_file = temp_dir / "prompt.txt"
                shutil.copytree(source_repo, workspace)
                prompt_file.write_text(prompt, encoding="utf-8")

                command = agent_command.format(
                    workspace=str(workspace),
                    prompt_file=str(prompt_file),
                )
                agent = subprocess.run(
                    command,
                    cwd=Path.cwd(),
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                )
                grade = _grade(grader, workspace, timeout)
                runs.append(
                    {
                        "bac": bac,
                        "trial": trial,
                        "score": round(100 * grade["passed"] / grade["total"], 2),
                        "passed": grade["passed"],
                        "total": grade["total"],
                        "details": grade.get("details", []),
                        "agent_exit_code": agent.returncode,
                        "prompt": prompt,
                    }
                )
    return runs


def _grade(grader: Path, workspace: Path, timeout: int) -> dict[str, Any]:
    result = subprocess.run(
        ["python", str(grader), str(workspace)],
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Grader failed:\n{result.stderr or result.stdout}")
    try:
        grade = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise RuntimeError(f"Grader returned invalid JSON: {result.stdout}") from error
    if not {"passed", "total"} <= grade.keys() or grade["total"] <= 0:
        raise RuntimeError(f"Grader returned an invalid result: {grade}")
    return grade
