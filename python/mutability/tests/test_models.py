"""Public-contract tests for mutability and value semantics."""

from dataclasses import FrozenInstanceError

import pytest

from mutability.examples.models import (
    Basket,
    LineItem,
    TaskQueue,
    make_minimum_checks,
    normalized_tags,
    with_score,
)


def test_immutable_update_does_not_change_original() -> None:
    original = Basket()
    updated = original.with_item(LineItem("sku", 2))
    assert original.items == ()
    assert updated.items == (LineItem("sku", 2),)

    with pytest.raises(FrozenInstanceError):
        setattr(updated, "items", ())


def test_instances_do_not_share_state() -> None:
    first, second = TaskQueue(), TaskQueue()
    first.add("first")
    assert first.snapshot() == ("first",)
    assert second.snapshot() == ()


def test_snapshot_is_not_a_mutable_alias() -> None:
    queue = TaskQueue()
    queue.add("one")
    snapshot = queue.snapshot()
    queue.add("two")
    assert snapshot == ("one",)
    assert queue.snapshot() == ("one", "two")


def test_copy_does_not_mutate_caller() -> None:
    source = {"alpha": 1}
    updated = with_score(source, "beta", 2)
    assert source == {"alpha": 1}
    assert updated == {"alpha": 1, "beta": 2}
    assert updated is not source


def test_optional_collection_is_a_snapshot() -> None:
    source = [" a ", "", "b"]
    snapshot = normalized_tags(source)
    source.append("c")
    assert snapshot == ("a", "b")
    assert normalized_tags() == ()


def test_closures_bind_each_limit_independently() -> None:
    checks = make_minimum_checks([2, 5, 10])
    assert tuple(check(6) for check in checks) == (True, True, False)
