from core.interfaces import Operation

class Sub(Operation):
    def name (self) -> str:
        return "sub"
    
    def arity (self) -> int:
        return 2    
    
    def execute (self, args):
        a,b = args
        return a - b