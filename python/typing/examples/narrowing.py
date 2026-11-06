"""Sound runtime predicates and static narrowing examples for Python 3.13+."""

from typing import TypeGuard, TypeIs, assert_type


def length_or_zero(value: str | None) -> int:
    """Narrow an optional value with an explicit None check."""
    if value is None:
        assert_type(value, None)
        return 0
    assert_type(value, str)
    return len(value)


def stringify(value: str | int) -> str:
    """Narrow a union with isinstance."""
    if isinstance(value, str):
        assert_type(value, str)
        return value
    assert_type(value, int)
    return str(value)


def is_str(value: object) -> TypeIs[str]:
    """Both True and False mean exactly what the predicate claims."""
    return isinstance(value, str)


def normalize(value: str | int) -> str:
    """TypeIs narrows both branches."""
    if is_str(value):
        assert_type(value, str)
        return value.lower()
    assert_type(value, int)
    return str(value)


def is_int_list(values: list[object]) -> TypeGuard[list[int]]:
    """TypeGuard may narrow invariant generics, unlike TypeIs."""
    return all(type(value) is int for value in values)


def sum_if_ints(values: list[object]) -> int | None:
    """The false branch is still list[object], not a complementary type."""
    if is_int_list(values):
        assert_type(values, list[int])
        return sum(values)
    assert_type(values, list[object])
    return None
