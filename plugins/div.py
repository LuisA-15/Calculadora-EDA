from core.interfaces import Operation

class Div(Operation):

    def name (self) -> str:
        return "div"
    
    def arity (self) -> int:
        return 2    
    
    def execute (self, args):
        a,b = args
        if b == 0:
            raise ValueError("Division by zero is not allowed.")
        return a / b    