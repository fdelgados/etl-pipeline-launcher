from __future__ import annotations


class KShingleSize:
    _MIN_VALUE = 2
    _MAX_VALUE = 10

    def __init__(self, value: int):
        self._ensure_is_valid_value(value)

        self._value = value

    def _ensure_is_valid_value(self, value):
        if not isinstance(value, int):
            raise ValueError(f"{value} is not a valid k-shingle size value")

        if value < self._MIN_VALUE:
            raise ValueError(
                f"K-shingle size cannot be lower than {self._MIN_VALUE}"
            )

        if value > self._MAX_VALUE:
            raise ValueError(
                f"K-shingle size cannot be higher than {self._MAX_VALUE}"
            )

    @property
    def value(self):
        return self._value

    @staticmethod
    def min() -> int:
        return KShingleSize._MIN_VALUE

    @staticmethod
    def max() -> int:
        return KShingleSize._MAX_VALUE

    def __eq__(self, other: KShingleSize) -> bool:
        if not isinstance(other, KShingleSize):
            return False

        return other.value == self._value
