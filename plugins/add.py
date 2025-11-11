from core.interfaces import Operation

class Add(Operation):
    def name(self):
        return "add"

    def arity(self):
        return 2

    def execute(self, args):
        return sum(args)
