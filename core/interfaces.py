from abc import ABC, abstractmethod
from typing import Sequence


class Operation(ABC):

    @abstractmethod
    def name(self) -> str:
        """Unique operation name (e.g., 'add', 'sqrt')."""
        raise NotImplementedError


    @abstractmethod
    def arity(self) -> int:
        """Number of required arguments. Use 1 for unary ops like sqrt, 2 for binary ops."""
        raise NotImplementedError


    @abstractmethod
    def execute(self, args: Sequence[float]) -> float:
        """Compute result. `len(args)` must equal `arity()`; validate inside if needed."""
        raise NotImplementedError