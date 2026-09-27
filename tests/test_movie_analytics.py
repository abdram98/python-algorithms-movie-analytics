"""Tests for streaming movie-rating analytics."""

from pathlib import Path
import sys
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.movie_analytics import (  # noqa: E402
    best_french_exclusive_movie,
    earliest_rating,
    most_rated_movie,
)


SAMPLE_DIR = PROJECT_ROOT / "data" / "sample"
MOVIES = SAMPLE_DIR / "movies.json"
RATINGS = SAMPLE_DIR / "ratings.csv"


class MovieAnalyticsTests(unittest.TestCase):
    def test_earliest_rating(self) -> None:
        result = earliest_rating(RATINGS)
        self.assertEqual(result.user_id, "u6")
        self.assertEqual(result.timestamp, 90)

    def test_most_rated_movie(self) -> None:
        result = most_rated_movie(MOVIES, RATINGS)
        self.assertEqual(result.movie_id, "101")
        self.assertEqual(result.title, "Le Rivage")
        self.assertEqual(result.rating_count, 5)

    def test_best_movie_for_french_exclusive_users(self) -> None:
        result = best_french_exclusive_movie(MOVIES, RATINGS)
        self.assertEqual(result.movie_id, "101")
        self.assertEqual(result.rating_count, 4)
        self.assertAlmostEqual(result.average_rating or 0.0, 4.625)

    def test_minimum_rating_validation(self) -> None:
        with self.assertRaises(ValueError):
            best_french_exclusive_movie(MOVIES, RATINGS, minimum_ratings=0)


if __name__ == "__main__":
    unittest.main()
