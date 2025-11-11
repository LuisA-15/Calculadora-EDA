from core.interfaces import Operation 

class Add(Operation):

    def name (self) -> str:
        return "add"
    
    def arity (self) -> int:
        return 2    
    
    def execute (self, args):
        a,b = args
        return a + b