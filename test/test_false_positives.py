"""
Regression tests for known false positives.

Each test targets one check that currently fires on code it should not fire
on. The minimal reproducing samples live in `test/data_false_positive/`, and
each sample file documents the behavioral difference between the old (current)
code and the code refurb suggests, i.e. why applying the suggestion would
break the program.

These tests FAIL against the current implementation: that is intentional, and
is what exposes each bug. As each underlying check is fixed, the corresponding
test starts passing. Do not "fix" these tests by loosening the assertions.
"""

from collections.abc import Sequence
from pathlib import Path

from refurb.error import Error, ErrorCode
from refurb.main import run_refurb
from refurb.settings import Settings

FALSE_POSITIVE_DATA_PATH = Path(__file__).parent / "data_false_positive"


def run_single_check(filename: str, code: int) -> Sequence[Error | str]:
    settings = Settings(
        files=[str(FALSE_POSITIVE_DATA_PATH / filename)],
        disable_all=True,
        enable={ErrorCode(code)},
    )

    return run_refurb(settings)


def test_furb101_ignores_non_builtin_open() -> None:
    # `gzip.open` decompresses while reading; the suggested
    # `Path(x).read_text()` does not, so the fix changes behavior.
    errors = run_single_check("furb101_gzip_open.py", 101)

    assert not errors, f"FURB101 false positive: {errors[0]}"


def test_furb102_ignores_calls_that_already_take_a_tuple() -> None:
    # Merging `x.startswith((a, b)) or x.startswith(c)` into
    # `x.startswith(((a, b), c))` raises TypeError at runtime.
    errors = run_single_check("furb102_startswith_tuple_arg.py", 102)

    assert not errors, f"FURB102 false positive: {errors[0]}"


def test_furb121_ignores_calls_that_already_take_a_tuple() -> None:
    # Merging `isinstance(x, (A, B)) or isinstance(x, C)` into
    # `isinstance(x, (A, B) | C)` raises TypeError at runtime.
    errors = run_single_check("furb121_isinstance_tuple_arg.py", 121)

    assert not errors, f"FURB121 false positive: {errors[0]}"


def test_furb127_ignores_assignments_read_by_the_with_body() -> None:
    # The `with` body reads the old value of the variable (`text + f.read()`),
    # so the pre-`with` assignment cannot be removed.
    errors = run_single_check("furb127_with_assign_reads_old_value.py", 127)

    assert not errors, f"FURB127 false positive: {errors[0]}"


def test_furb128_ignores_temps_used_after_the_swap() -> None:
    # `temp` is read after the swap, so the three assignments cannot be
    # collapsed into `x, y = y, x`.
    errors = run_single_check("furb128_temp_used_after_swap.py", 128)

    assert not errors, f"FURB128 false positive: {errors[0]}"
