"""Tests for the standalone algorithm implementations."""

from pathlib import Path
import sys
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.algorithms import (  # noqa: E402
    AnimalCombination,
    check_preceding_sum,
    enumerate_animal_combinations,
    find_matches,
    top_bigrams,
)


class AlgorithmTests(unittest.TestCase):
    def test_preceding_sum_examples(self) -> None:
        self.assertTrue(check_preceding_sum([1, 2, 3, 5, 8, 13], 2))
        self.assertFalse(check_preceding_sum([1, 2, 3, 5, 8, 13], 3))
        self.assertTrue(check_preceding_sum([1, 1, 2, 2, 6, 11, 21], 4))

    def test_preceding_sum_rejects_invalid_window(self) -> None:
        with self.assertRaises(ValueError):
            check_preceding_sum([1, 2], 0)

    def test_bigrams_do_not_cross_word_boundaries(self) -> None:
        self.assertEqual(
            top_bigrams(["climb", "time"], limit=6),
            [("im", 2), ("cl", 1), ("li", 1), ("mb", 1), ("me", 1), ("ti", 1)],
        )

    def test_animal_combinations(self) -> None:
        combinations = enumerate_animal_combinations(3, 10)
        self.assertEqual(
            set(combinations),
            {
                AnimalCombination(1, 2, 0, 0),
                AnimalCombination(2, 0, 1, 0),
            },
        )

    def test_match_search_includes_last_valid_column(self) -> None:
        board = [
            ["a", "b", "c", "x", "x"],
            ["d", "e", "f", "x", "x"],
            ["g", "h", "i", "x", "x"],
        ]
        matches = find_matches(board)
        self.assertIn(((0, 3), (1, 3), (2, 3)), matches)
        self.assertIn(((0, 4), (1, 4), (2, 4)), matches)

    def test_match_search_validates_shape(self) -> None:
        with self.assertRaises(ValueError):
            find_matches([["x", "x"], ["x"]])


if __name__ == "__main__":
    unittest.main()
