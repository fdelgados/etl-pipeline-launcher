from __future__ import annotations


class SimilarityThreshold:
    _MIN_VALUE = 0
    _MAX_VALUE = 1.0

    def __init__(self, value: float):
        self._ensure_is_valid_threshold(value)
        self._value = value

    def _ensure_is_valid_threshold(self, value):
        if not isinstance(value, float):
            raise ValueError(f"{value} is not a valid similarity threshold")

        if value < self._MIN_VALUE:
            raise ValueError(
                f"Similarity threshold cannot be lower than {self._MIN_VALUE}"
            )

        if value > self._MAX_VALUE:
            raise ValueError(
                f"Similarity threshold cannot be higher than {self._MAX_VALUE}"
            )

    @staticmethod
    def min() -> float:
        return SimilarityThreshold._MIN_VALUE

    @staticmethod
    def max() -> float:
        return SimilarityThreshold._MAX_VALUE

    @property
    def value(self) -> float:
        return self._value

    def __float__(self):
        return self.value

    def __eq__(self, other: SimilarityThreshold) -> bool:
        if not isinstance(other, SimilarityThreshold):
            return False

        return other.value == self._value
