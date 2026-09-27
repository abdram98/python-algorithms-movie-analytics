# Data

The repository includes fabricated sample files so that every analysis can run
without the original course archive.

## Expected full-data files

Place the following files in `data/raw/` to reproduce the recorded analysis:

| File | Format | Validated records | Uncompressed size |
|---|---|---:|---:|
| `linuxwords` | One word per line | 45,402 words | 409,048 bytes |
| `movies.json` | JSON Lines | 45,463 movies | 6,883,107 bytes |
| `ratings.csv` | CSV with header | 1,059,098 ratings | 27,348,802 bytes |

### Movie schema

Each line of `movies.json` is a JSON object similar to:

```json
{"genres": ["Animation"], "id": "862", "language": "en", "title": "Toy Story", "countries": ["US"], "releasedate": "1995-10-30"}
```

The analysis requires `id`, `title` and a language field. The loader accepts
`language`, `languages` or `original_language`.

### Rating schema

```text
userId,movieId,rating,timestamp
```

Movie identifiers are treated as strings and linked directly to `id` in the
movie file. Ratings are parsed as floating-point values and timestamps as
integers.

## Included sample

Files in `data/sample/` are small, fabricated examples. They preserve the
expected schemas but contain no original user records or course-data extracts.

## Data availability

The word list was supplied with a reference to the
[Duke Linux words file](https://users.cs.duke.edu/~ola/ap/linuxwords). The
movie and rating files were supplied as course material, but their upstream
provenance and redistribution terms were not stated in the archive. For that
reason, `data/raw/` is excluded from version control and the original files
should not be uploaded until their licence is confirmed.
