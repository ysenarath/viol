from __future__ import annotations

from collections.abc import Iterable, MutableSequence
from typing import Any, Generic, TypeVar, overload

from typing_extensions import Self

T = TypeVar("T")

__all__ = [
    "ValidatedList",
]


class ValidatedList(MutableSequence[T], Generic[T]):
    def __init__(self, data: Iterable[T] | None = None):
        self._data = data or []

    @overload
    def __getitem__(self, i: int) -> T: ...
    @overload
    def __getitem__(self, i: slice) -> Self: ...
    def __getitem__(self, i: Any) -> Any:
        # For sequence types, the accepted keys should be integers.
        # Optionally, they may support slice objects as well.
        # Negative index support is also optional.
        if isinstance(i, slice):
            cls = type(self)
            obj = cls.__new__(cls)
            obj._data = self._data[i]
            return obj
        if isinstance(i, int):
            return self._data[i]
        cls = type(self).__name__
        indexer = type(i).__name__
        msg = f"{cls} indices must be integers or slices, not {indexer}"
        raise TypeError(msg)

    def __setitem__(self, i: int, value: Any) -> None:
        self._data[i] = self.validate(value)

    def __delitem__(self, i: int) -> None:
        del self._data[i]

    def __len__(self) -> int:
        return len(self._data)

    def insert(self, i: int, value: Any) -> None:
        self._data.insert(i, self.validate(value))

    def validate(self, value: Any) -> T:
        return value
