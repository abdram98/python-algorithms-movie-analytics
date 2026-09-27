"""Small, testable algorithms developed from introductory Python exercises."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Iterable, Sequence


Coordinate = tuple[int, int]
Match = tuple[Coordinate, ...]


@dataclass(frozen=True, slots=True)
class AnimalCombination:
    """Counts satisfying an animal-total and leg-total constraint."""

    parrots: int
    lions: int
    ladybugs: int
    scorpions: int

    @property
    def animal_count(self) -> int:
        return self.parrots + self.lions + self.ladybugs + self.scorpions

    @property
    def leg_count(self) -> int:
        return (
            2 * self.parrots
            + 4 * self.lions
            + 6 * self.ladybugs
            + 8 * self.scorpions
        )


def check_preceding_sum(values: Sequence[int | float], window: int) -> bool:
    """Return whether each checked value equals the preceding window's sum."""

    if window < 1:
        raise ValueError("window must be at least 1")

    return all(
        values[index] == sum(values[index - window : index])
        for index in range(window, len(values))
    )


def count_bigrams(words: Iterable[str]) -> Counter[str]:
    """Count adjacent, lowercased character pairs within individual words."""

    counts: Counter[str] = Counter()
    for raw_word in words:
        word = raw_word.strip().lower()
        counts.update(word[index : index + 2] for index in range(len(word) - 1))
    return counts


def top_bigrams(words: Iterable[str], *, limit: int = 25) -> list[tuple[str, int]]:
    """Return the most frequent bigrams with deterministic tie ordering."""

    if limit < 1:
        raise ValueError("limit must be at least 1")
    counts = count_bigrams(words)
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:limit]


def enumerate_animal_combinations(
    total_animals: int,
    total_legs: int,
) -> list[AnimalCombination]:
    """Return all non-negative animal counts satisfying both totals."""

    if total_animals < 0 or total_legs < 0:
        raise ValueError("totals cannot be negative")

    combinations: list[AnimalCombination] = []
    for parrots in range(total_animals + 1):
        for lions in range(total_animals - parrots + 1):
            # From the two constraints:
            # ladybugs = (8N - 6P - 4L - total_legs) / 2
            numerator = 8 * total_animals - 6 * parrots - 4 * lions - total_legs
            if numerator < 0 or numerator % 2:
                continue
            ladybugs = numerator // 2
            scorpions = total_animals - parrots - lions - ladybugs
            if ladybugs < 0 or scorpions < 0:
                continue

            combination = AnimalCombination(
                parrots=parrots,
                lions=lions,
                ladybugs=ladybugs,
                scorpions=scorpions,
            )
            if combination.leg_count == total_legs:
                combinations.append(combination)

    return combinations


def find_matches(board: Sequence[Sequence[str]], *, length: int = 3) -> list[Match]:
    """Find equal-piece windows horizontally, vertically and diagonally."""

    if length < 2:
        raise ValueError("length must be at least 2")
    if not board:
        return []

    column_count = len(board[0])
    if column_count == 0:
        return []
    if any(len(row) != column_count for row in board):
        raise ValueError("board must be rectangular")

    row_count = len(board)
    directions = ((0, 1), (1, 0), (1, 1), (1, -1))
    matches: list[Match] = []

    for row in range(row_count):
        for column in range(column_count):
            piece = board[row][column]
            for row_step, column_step in directions:
                end_row = row + (length - 1) * row_step
                end_column = column + (length - 1) * column_step
                if not (0 <= end_row < row_count and 0 <= end_column < column_count):
                    continue

                coordinates = tuple(
                    (row + offset * row_step, column + offset * column_step)
                    for offset in range(length)
                )
                if all(board[r][c] == piece for r, c in coordinates[1:]):
                    matches.append(coordinates)

    return matches
