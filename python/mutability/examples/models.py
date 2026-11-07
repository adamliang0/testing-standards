"""Value-oriented data and clearly owned mutable state."""

from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class LineItem:
    sku: str
    quantity: int


@dataclass(frozen=True, slots=True)
class Basket:
    # Both the container and its element type are immutable.
    items: tuple[LineItem, ...] = ()

    def with_item(self, item: LineItem) -> "Basket":
        return Basket(items=(*self.items, item))


@dataclass(slots=True)
class TaskQueue:
    # Every instance owns a distinct list; it is not part of the public API.
    _pending: list[str] = field(default_factory=list, init=False, repr=False)

    def add(self, task: str) -> None:
        self._pending.append(task)

    def snapshot(self) -> tuple[str, ...]:
        return tuple(self._pending)


def with_score(scores: Mapping[str, int], key: str, value: int) -> dict[str, int]:
    """Copy caller-owned data before adding an entry."""
    result = dict(scores)
    result[key] = value
    return result


def normalized_tags(tags: Iterable[str] | None = None) -> tuple[str, ...]:
    """Use an immutable default and return a new immutable snapshot."""
    normalized: list[str] = []
    for tag in () if tags is None else tags:
        value = tag.strip()
        if value:
            normalized.append(value)
    return tuple(normalized)


def make_minimum_checks(limits: Iterable[int]) -> tuple[Callable[[int], bool], ...]:
    """Bind each limit in its own closure instead of capturing a loop variable."""

    def at_least(limit: int) -> Callable[[int], bool]:
        def predicate(value: int) -> bool:
            return value >= limit

        return predicate

    return tuple(at_least(limit) for limit in limits)
