"""Streaming readers and analyses for movie metadata and rating records."""

from __future__ import annotations

from collections import Counter, defaultdict
import csv
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Iterator, Mapping


PathLike = str | Path
FRENCH_LABELS = {"fr", "french", "francais", "français"}


@dataclass(frozen=True, slots=True)
class Movie:
    movie_id: str
    title: str
    languages: tuple[str, ...]

    @property
    def is_french(self) -> bool:
        return any(language in FRENCH_LABELS for language in self.languages)


@dataclass(frozen=True, slots=True)
class Rating:
    user_id: str
    movie_id: str
    value: float
    timestamp: int


@dataclass(frozen=True, slots=True)
class EarliestRating:
    user_id: str
    timestamp: int


@dataclass(frozen=True, slots=True)
class MovieRatingResult:
    movie_id: str
    title: str
    rating_count: int
    average_rating: float | None = None


def _normalise_languages(record: Mapping[str, object]) -> tuple[str, ...]:
    raw_languages: object
    if "language" in record:
        raw_languages = record["language"]
    elif "languages" in record:
        raw_languages = record["languages"]
    else:
        raw_languages = record.get("original_language", "")

    if not isinstance(raw_languages, list):
        raw_languages = [raw_languages]

    languages: list[str] = []
    for item in raw_languages:
        value = item.get("name", "") if isinstance(item, dict) else item
        label = str(value).strip().lower()
        if label:
            languages.append(label)
    return tuple(languages)


def iter_movies(path: PathLike) -> Iterator[Movie]:
    """Yield validated movie records from a UTF-8 JSON Lines file."""

    with Path(path).open("r", encoding="utf-8") as source:
        for line_number, line in enumerate(source, start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Malformed JSON in {path!s} on line {line_number}."
                ) from exc
            if not isinstance(record, dict) or "id" not in record:
                raise ValueError(
                    f"Expected a movie object with an id on line {line_number}."
                )
            yield Movie(
                movie_id=str(record["id"]),
                title=str(record.get("title", "")),
                languages=_normalise_languages(record),
            )


def load_movies(path: PathLike) -> dict[str, Movie]:
    """Load movie metadata into an ID-keyed lookup."""

    return {movie.movie_id: movie for movie in iter_movies(path)}


def iter_ratings(path: PathLike) -> Iterator[Rating]:
    """Yield validated rating rows from CSV."""

    required_fields = {"userId", "movieId", "rating", "timestamp"}
    with Path(path).open("r", encoding="utf-8", newline="") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames is None or not required_fields.issubset(reader.fieldnames):
            raise ValueError(
                "ratings CSV must contain userId, movieId, rating and timestamp"
            )
        for line_number, row in enumerate(reader, start=2):
            try:
                yield Rating(
                    user_id=row["userId"],
                    movie_id=row["movieId"],
                    value=float(row["rating"]),
                    timestamp=int(row["timestamp"]),
                )
            except (TypeError, ValueError) as exc:
                raise ValueError(
                    f"Invalid rating values in {path!s} on line {line_number}."
                ) from exc


def earliest_rating(ratings_path: PathLike) -> EarliestRating:
    """Return the user and timestamp of the earliest rating."""

    earliest: Rating | None = None
    for rating in iter_ratings(ratings_path):
        if earliest is None or rating.timestamp < earliest.timestamp:
            earliest = rating
    if earliest is None:
        raise ValueError("ratings file contains no records")
    return EarliestRating(earliest.user_id, earliest.timestamp)


def most_rated_movie(
    movies_path: PathLike,
    ratings_path: PathLike,
) -> MovieRatingResult:
    """Return the metadata and count for the movie with most ratings."""

    movies = load_movies(movies_path)
    counts: Counter[str] = Counter(
        rating.movie_id for rating in iter_ratings(ratings_path)
    )
    eligible = [movie_id for movie_id in counts if movie_id in movies]
    if not eligible:
        raise ValueError("no rating movie IDs matched the movie metadata")

    movie_id = min(eligible, key=lambda value: (-counts[value], value))
    movie = movies[movie_id]
    return MovieRatingResult(movie.movie_id, movie.title, counts[movie_id])


def best_french_exclusive_movie(
    movies_path: PathLike,
    ratings_path: PathLike,
    *,
    minimum_ratings: int = 4,
) -> MovieRatingResult:
    """Find the best movie among users rating French-labelled titles only."""

    if minimum_ratings < 1:
        raise ValueError("minimum_ratings must be at least 1")

    movies = load_movies(movies_path)
    language_flags: defaultdict[str, list[bool]] = defaultdict(
        lambda: [False, False]
    )

    for rating in iter_ratings(ratings_path):
        movie = movies.get(rating.movie_id)
        if movie is None:
            continue
        if movie.is_french:
            language_flags[rating.user_id][0] = True
        else:
            language_flags[rating.user_id][1] = True

    exclusive_users = {
        user_id
        for user_id, (rated_french, rated_other) in language_flags.items()
        if rated_french and not rated_other
    }

    rating_sums: defaultdict[str, float] = defaultdict(float)
    rating_counts: Counter[str] = Counter()
    for rating in iter_ratings(ratings_path):
        if rating.user_id not in exclusive_users:
            continue
        movie = movies.get(rating.movie_id)
        if movie is None or not movie.is_french:
            continue
        rating_sums[rating.movie_id] += rating.value
        rating_counts[rating.movie_id] += 1

    eligible = [
        movie_id
        for movie_id, count in rating_counts.items()
        if count >= minimum_ratings
    ]
    if not eligible:
        raise ValueError("no movie satisfied the minimum eligible-rating count")

    def ranking_key(movie_id: str) -> tuple[float, int, str, str]:
        count = rating_counts[movie_id]
        average = rating_sums[movie_id] / count
        return (-average, -count, movies[movie_id].title.lower(), movie_id)

    movie_id = min(eligible, key=ranking_key)
    count = rating_counts[movie_id]
    movie = movies[movie_id]
    return MovieRatingResult(
        movie_id=movie.movie_id,
        title=movie.title,
        rating_count=count,
        average_rating=rating_sums[movie_id] / count,
    )
