class FunctionPrototype:
    def __init__(self, name, return_type, parameters):
        self.name = name
        self.return_type = return_type
        self.parameters = parameters


class Function:
    def __init__(self, name, return_type, parameters, block):
        self.name = name
        self.return_type = return_type
        self.parameters = parameters
        self.block = block


class Variable:
    def __init__(self, name, kind, is_const=False):
        self.name = name
        self.kind = kind
        self.is_const = is_const
        self.id = id(self)


class Parameter(Variable):
    pass