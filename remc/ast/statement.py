class NonExpression:
    pass


class Return(NonExpression):
    def __init__(self, expression):
        self.expression = expression


class Expression:
    def __init__(self):
        self.kind = None


class VariableRef(Expression):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.ref = None


class FunctionCall(Expression):
    def __init__(self, name, arguments):
        super().__init__()
        self.name = name
        self.arguments = arguments
        self.ref = None


class StringLitteral(Expression):
    def __init__(self, value):
        super().__init__()
        self.value = value


class IntLitteral(Expression):
    def __init__(self, value):
        super().__init__()
        self.value = value


class BinOp(Expression):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right


class Add(BinOp):
    pass
class Sub(BinOp):
    pass