import unittest

from ballmer_peak.impairment import impair_prompt, profile_for


class ImpairmentTests(unittest.TestCase):
    def test_sober_prompt_is_unchanged(self):
        self.assertEqual(impair_prompt("Do the precise thing.", 0.00), "Do the precise thing.")

    def test_mutation_is_deterministic(self):
        first = impair_prompt("Implement reliable retry behavior correctly.", 0.10, 3)
        second = impair_prompt("Implement reliable retry behavior correctly.", 0.10, 3)
        self.assertEqual(first, second)

    def test_unknown_level_is_rejected(self):
        with self.assertRaises(ValueError):
            profile_for(0.08)


if __name__ == "__main__":
    unittest.main()
