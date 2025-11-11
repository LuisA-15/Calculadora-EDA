from core.interfaces import Operation

class Pow(Operation):
    
    def name(self) -> str:
        return "Pow"
    
    def arity(self) -> int:
        return 2    
    
    def execute(self, args) -> float:
        a,b = args
        return a ** b