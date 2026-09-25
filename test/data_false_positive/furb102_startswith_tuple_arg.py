# False positive sample for FURB102 (use-startswith-endswith-tuple).
#
# Old (this code): the first call already passes a tuple of prefixes, which is
# valid because str.startswith() accepts a tuple.
#
# What refurb currently suggests:
#     filename.startswith(((".", "~"), "backup_"))
#
# Why the suggestion is wrong: merging the two calls nests a tuple inside the
# tuple, and str.startswith() raises `TypeError: startswith first arg must be
# str or a tuple of str` at runtime. The old code runs fine; the new code
# crashes.
#
# Expected: no FURB102 error when one of the arguments is already a tuple.


def is_hidden_or_backup_file(filename: str) -> bool:
    return filename.startswith((".", "~")) or filename.startswith("backup_")
