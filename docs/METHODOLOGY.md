# Methodology

## Sequence validation

For each element after the first `n` values, the implementation compares the
value with the sum of the preceding window. With `m` values and window width
`n`, the direct implementation runs in `O(mn)` time and uses `O(1)` additional
space apart from each short slice.

## Bigram frequency

Each word is stripped and lowercased independently before adjacent character
pairs are counted. Word boundaries are never joined. Results are ordered by
descending frequency and then alphabetically so tied outputs are reproducible.

## Animal combinations

The four animal types have 2, 4, 6 and 8 legs. Rather than trying every value
for all four counts, the algorithm loops over parrot and lion counts and solves
algebraically for ladybugs and scorpions. This reduces the search from cubic
to quadratic in the total number of animals.

## Board-match detection

The board is validated as rectangular and searched in four directions:
horizontal, vertical, descending diagonal and ascending diagonal. An endpoint
check occurs before any indexing, including positions at the final valid start
column or row. This removes the edge-position omission found in the original
prototype.

## Movie data processing

Movies are read from JSON Lines into a metadata lookup keyed by movie ID.
Ratings are yielded one at a time from CSV.

- Earliest rating requires one pass and constant analysis state.
- Most-rated movie requires one pass plus a count per observed movie ID.
- French-exclusive analysis uses two passes. The first stores whether each
  user has rated French and non-French movies; the second stores only the sum
  and count for movies rated by qualifying users.

This approach avoids retaining more than one million complete rating records
in memory.

## Qualification rule

A movie is considered French-language when its normalised language labels
contain `fr`, `french`, `francais` or `français`. A French-exclusive user must
have at least one matched French-language rating and no matched non-French
rating. The final movie must receive at least four ratings from qualifying
users. Ties are resolved deterministically by rating count, title and ID.
