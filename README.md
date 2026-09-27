# Python Algorithms and Movie Analytics

A standard-library Python project combining algorithm design, file processing
and movie-rating analytics. It moves from compact programming problems to a
streaming analysis of more than one million ratings.

## Project highlights

- Analysed **1,059,098 ratings**, **45,463 movie records** and a
  **45,402-word dictionary** without requiring pandas.
- Implemented sliding-window validation, bigram counting and constrained
  combinatorial search.
- Built boundary-safe horizontal, vertical and diagonal match detection for
  rectangular game boards.
- Streamed CSV and JSON Lines data instead of loading the full ratings table
  into memory.
- Identified the earliest rating, the most-rated movie and the highest-rated
  movie among users who rated French-language titles exclusively.
- Added deterministic behaviour, input validation and automated unit tests.

## Questions explored

1. Does every value in a sequence equal the sum of its preceding `n` values?
2. Which character bigrams occur most frequently in a word list?
3. Which combinations of four animal types satisfy specified animal and leg
   totals?
4. Where do three-piece matches occur on a two-dimensional game board?
5. Which user submitted the earliest recorded movie rating?
6. Which movie received the largest number of ratings?
7. Which qualifying movie scored highest among French-exclusive raters?

## Recorded full-data findings

| Analysis | Result |
|---|---|
| Earliest rating | User `5274`, timestamp `825582938` |
| Most-rated movie | *The Million Dollar Hotel*, 8,531 ratings |
| Best qualifying French-language movie | *Sous le Sable*, mean rating 4.625 from 4 eligible ratings |

The word-list analysis found `in` as the most frequent bigram, with 8,427
occurrences. Complete reproduced outputs are in
[`results/README.md`](results/README.md).

## Implementation

The reusable code is split into two modules:

- [`src/algorithms.py`](src/algorithms.py) contains the sequence, bigram,
  animal-combination and board-search algorithms.
- [`src/movie_analytics.py`](src/movie_analytics.py) contains validated JSONL
  and CSV readers plus the movie-rating analyses.

The rating table is processed as an iterator. The French-exclusive analysis
uses two passes: the first classifies users by the languages of movies they
rated, and the second aggregates ratings only for qualifying users. This keeps
memory use tied to users and movies rather than to the number of rating rows.

See [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md) for design decisions and
complexity notes.

## Data

Small fabricated files in `data/sample/` allow the notebook and tests to run
immediately. They are not extracts from the full dataset.

To reproduce the complete analysis, place the following files in `data/raw/`:

```text
data/raw/linuxwords
data/raw/movies.json
data/raw/ratings.csv
```

The raw files are excluded from version control because redistribution terms
for the course-provided movie files have not been confirmed. See
[`data/README.md`](data/README.md) for schemas and record counts.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m unittest discover -s tests -v
jupyter lab notebooks/python_algorithms_and_movie_analytics.ipynb
```

Python 3.10 or later is recommended. The analysis modules use only the Python
standard library.

## Repository structure

```text
python-algorithms-movie-analytics/
├── README.md
├── data/
│   ├── README.md
│   └── sample/
├── docs/
│   └── METHODOLOGY.md
├── notebooks/
│   └── python_algorithms_and_movie_analytics.ipynb
├── results/
│   └── README.md
├── src/
│   ├── __init__.py
│   ├── algorithms.py
│   └── movie_analytics.py
├── tests/
│   ├── test_algorithms.py
│   └── test_movie_analytics.py
├── .gitignore
└── requirements.txt
```

## Interpretation boundaries

- Results describe the supplied historical files and should not be treated as
  current audience preferences.
- A user is classified as French-exclusive only when every matched movie they
  rated is labelled French in the movie metadata.
- Ratings whose movie identifier is absent from the metadata are ignored for
  language classification.
- The language rule follows dataset labels; it does not infer language from
  titles, countries or genres.
- A run longer than three pieces produces every contiguous three-piece window.
