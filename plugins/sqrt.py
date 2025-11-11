import math
from core.interfaces import Operation

class Sqrt(Operation):
    
    def name(self) -> str:
        return "Sqrt"
    
    def arity(self) -> int:
        return 1    
    
    def execute(self, args) -> float:
        (a,) = args
        if a < 0:
            raise ValueError("Cannot compute square root of a negative number.")
        return math.sqrt(a)