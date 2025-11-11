from core.interfaces import Operation

class Mul(Operation):
    def name(self) -> str:
        return "Mul"

    def arity(self) -> int:
        return 2

    def execute(self, args) -> float:
        a, b = args
        return a * b