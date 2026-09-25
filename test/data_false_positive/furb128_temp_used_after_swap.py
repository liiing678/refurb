# False positive sample for FURB128 (use-tuple-unpack-swap).
#
# Old (this code): a classic temp-variable swap, except `temp` is still read
# AFTER the swap (it holds the original value of `first`, which is reported).
#
# What refurb currently reports:
#     "Use tuple unpacking instead of temporary variables to swap values"
#
# Why the suggestion is wrong: applying it means replacing the three
# assignments with `first, second = second, first` and deleting `temp`, but
# `temp` is used later, so the "fixed" code raises NameError (or prints the
# wrong value). The check is only valid when the temp variable is never read
# again after the swap.
#
# Expected: no FURB128 error when the temporary variable is used after the
# swap.
#
# Note: the swap lives inside an `if` block because mypy mangles names of
# variables that are reassigned in the same scope (`first` -> `first'`),
# which would keep the check from matching at all. This mirrors how the
# check's own test data (test/data/err_128.py) is structured.

first = 1
second = 2

if first < second:
    temp = first
    first = second
    second = temp

    print(temp)
