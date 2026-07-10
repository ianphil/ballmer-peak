import sys
import unittest
from pathlib import Path

from ballmer_peak.runner import run_eval


ROOT = Path(__file__).resolve().parents[1]


class RunnerTests(unittest.TestCase):
    def test_reference_agent_passes_benchmark(self):
        command = (
            f'"{sys.executable}" '
            f'"{ROOT / "examples" / "reference_agent.py"}" '
            '"{workspace}"'
        )
        runs = run_eval(
            ROOT / "evals" / "retry-client",
            command,
            [0.00, 0.20],
            repetitions=1,
            timeout=30,
        )
        self.assertEqual([run["score"] for run in runs], [100.0, 100.0])


if __name__ == "__main__":
    unittest.main()
