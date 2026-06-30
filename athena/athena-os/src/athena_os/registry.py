"""Generic named-object registry — APS-005."""

from __future__ import annotations

from typing import Generic, TypeVar

from athena_os.errors import NotFoundError

T = TypeVar("T")


class Registry(Generic[T]):
    """Thread-unsafe in-memory registry with typed entries."""

    def __init__(self, name: str = "default") -> None:
        self.name = name
        self._entries: dict[str, T] = {}

    def register(self, key: str, value: T, *, overwrite: bool = False) -> None:
        if key in self._entries and not overwrite:
            msg = f"registry entry already exists: {key}"
            raise NotFoundError(msg, context={"registry": self.name, "key": key})
        self._entries[key] = value

    def get(self, key: str) -> T:
        value = self._entries.get(key)
        if value is None:
            msg = f"registry entry not found: {key}"
            raise NotFoundError(msg, context={"registry": self.name, "key": key})
        return value

    def get_optional(self, key: str) -> T | None:
        return self._entries.get(key)

    def unregister(self, key: str) -> T:
        value = self._entries.pop(key, None)
        if value is None:
            msg = f"registry entry not found: {key}"
            raise NotFoundError(msg, context={"registry": self.name, "key": key})
        return value

    def list_keys(self) -> list[str]:
        return list(self._entries.keys())

    def items(self) -> list[tuple[str, T]]:
        return list(self._entries.items())

    def clear(self) -> None:
        self._entries.clear()

    def __len__(self) -> int:
        return len(self._entries)
