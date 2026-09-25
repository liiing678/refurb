# False positive sample for FURB127 (no-with-assign).
#
# Old (this code): `text` is initialized before the `with` statement, and the
# assignment inside the `with` body READS that initial value on its right
# hand side (`text + f.read()`).
#
# What refurb currently reports:
#     "This variable is redeclared later, and can be removed here"
#     (pointing at `text = "prefix: "`)
#
# Why the suggestion is wrong: removing the first assignment makes the code
# raise NameError (or silently drop the prefix if an outer-scope `text`
# exists), because the `with` body depends on the old binding. The check is
# only valid when the reassigned value does not depend on the previous one.
#
# Expected: no FURB127 error when the `with` body reads the variable it
# reassigns.


def read_file_with_prefix() -> str:
    text = "prefix: "

    with open("file.txt") as f:
        text = text + f.read()

    return text
