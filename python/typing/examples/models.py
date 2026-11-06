"""Finite unions, TypedDicts, structural protocols, and exhaustive matching."""

from typing import Literal, Protocol, TypedDict, assert_never


class UserRecord(TypedDict):
    id: int
    name: str


class Named(Protocol):
    @property
    def name(self) -> str: ...


class Person:
    def __init__(self, name: str) -> None:
        self._name = name

    @property
    def name(self) -> str:
        return self._name


def greeting(item: Named) -> str:
    return f"Hello, {item.name}"


def user_label(user: UserRecord) -> str:
    return f"{user['id']}: {user['name']}"


type Status = Literal["pending", "complete", "failed"]


def status_message(status: Status) -> str:
    match status:
        case "pending":
            return "Waiting"
        case "complete":
            return "Done"
        case "failed":
            return "Error"
        case _:
            assert_never(status)
