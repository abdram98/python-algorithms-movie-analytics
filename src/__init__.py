"""Reusable algorithms and movie-rating analytics."""

from .algorithms import (
    AnimalCombination,
    check_preceding_sum,
    count_bigrams,
    enumerate_animal_combinations,
    find_matches,
    top_bigrams,
)
from .movie_analytics import (
    EarliestRating,
    MovieRatingResult,
    best_french_exclusive_movie,
    earliest_rating,
    most_rated_movie,
)

__all__ = [
    "AnimalCombination",
    "EarliestRating",
    "MovieRatingResult",
    "best_french_exclusive_movie",
    "check_preceding_sum",
    "count_bigrams",
    "earliest_rating",
    "enumerate_animal_combinations",
    "find_matches",
    "most_rated_movie",
    "top_bigrams",
]
