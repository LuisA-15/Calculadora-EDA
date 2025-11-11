from typing import Sequence

class Validator:
    @staticmethod
    def ensure_arity(args: Sequence[float], expected: int, opname: str) -> None:
        if len(args) != expected:
            raise ValueError(f"{opname}: expected {expected} argument(s), got {len(args)}")


    @staticmethod
    def ensure_numbers(args: Sequence[float], opname: str) -> None:
        try:
            for _ in map(float, args):
                pass
        except Exception as e:
            raise ValueError(f"{opname}: arguments must be numeric") from e