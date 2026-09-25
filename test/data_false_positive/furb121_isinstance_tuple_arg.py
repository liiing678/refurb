# False positive sample for FURB121 (use-isinstance-issubclass-tuple).
#
# Old (this code): the first call already passes a tuple of types, which is
# valid because isinstance() accepts a tuple.
#
# What refurb currently suggests (Python 3.10+):
#     isinstance(value, (int, float) | str)
#
# Why the suggestion is wrong: `tuple | type` is not a supported operation,
# so the merged check raises `TypeError: unsupported operand type(s) for |`
# at runtime. (On older Python versions refurb suggests nesting the tuple,
# `isinstance(value, ((int, float), str))`, which also raises TypeError.)
# The old code runs fine; the new code crashes.
#
# Expected: no FURB121 error when one of the classinfo arguments is already
# a tuple.


def is_number_or_text(value: object) -> bool:
    return isinstance(value, (int, float)) or isinstance(value, str)
