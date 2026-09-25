# False positive sample for FURB101 (use-pathlib-read-text-read-bytes).
#
# Old (this code): `open` here is `gzip.open`, not `builtins.open`, so the
# file is transparently decompressed while being read.
#
# What refurb currently suggests:
#     contents = Path(filename).read_text()
#
# Why the suggestion is wrong: `Path.read_text()` reads the raw, still
# compressed bytes and tries to decode them as text. Applying the fix either
# raises UnicodeDecodeError or returns garbage, so the suggested "new" code is
# NOT behaviorally equivalent to the old code.
#
# Expected: no FURB101 error, because the check must only fire when `open`
# resolves to `builtins.open`.

from gzip import open


def read_gzipped_text(filename: str) -> str:
    with open(filename, "rt") as f:
        contents = f.read()

    return contents
