import unittest

from ballmer_peak.scoring import summarize


class ScoringTests(unittest.TestCase):
    def test_finds_peak_cliff_and_windows_me_event(self):
        result = summarize(
            [
                {"bac": 0.00, "score": 70},
                {"bac": 0.06, "score": 95},
                {"bac": 0.10, "score": 60},
                {"bac": 0.14, "score": 20},
            ]
        )
        self.assertEqual(result["peak_bac"], 0.06)
        self.assertEqual(result["confidence_cliff"], 0.10)
        self.assertEqual(result["windows_me_events"], 1)


if __name__ == "__main__":
    unittest.main()
