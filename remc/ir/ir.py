class Extern:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"extern {self.name}"


class Litteral:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return repr(self.value)


class String(Litteral):
    pass
class Integer(Litteral):
    pass


class Temp:
    def __init__(self, name):
        self.name = name
        self.lifetime = None

    def __repr__(self):
        return f"t_{self.name}"


class Variable:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.lifetime = None

    def __repr__(self):
        return f"v_{self.name}"


class ParameterRef:
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def __repr__(self):
        return f"p_{self.name}"


class Parameter:
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def __repr__(self):
        return f"{self.name}: {self.size}"

    def __eq__(self, other):
        return self.name == other.name and self.size == other.size


class Function:
    def __init__(self, name, parameters, return_size, instructions):
        self.name = name
        self.parameters = parameters
        self.return_size = return_size
        self.instructions = instructions
        self.temps = []

    def __repr__(self):
        params = ",".join(map(repr, self.parameters))
        instructions = "\n\t".join(map(repr, self.instructions))
        result = f"function {self.name}({params}) -> {self.return_size} {{\n\t{instructions}\n}}"
        return result


class Program:
    def __init__(self):
        self.functions = []
        self.externs = []

    def add_extern(self, extern):
        self.externs.append(extern)

    def add_function(self, function):
        self.functions.append(function)

    def __repr__(self):
        externs = "\n".join(map(repr, self.externs))
        functions = "\n\n".join(map(repr, self.functions))
        return f"{externs}\n\n{functions}"


class Instruction:
    pass


class BinOp(Instruction):
    def __init__(self, dest, a, b):
        self.dest = dest
        self.a = a
        self.b = b

    def __repr__(self):
        return f"{self.__class__.__name__} {self.dest}, {self.a}, {self.b}"


class ADD(BinOp):
    pass
class SUB(BinOp):
    pass


class CALL(Instruction):
    def __init__(self, name, dest, args):
        self.dest = dest
        self.name = name
        self.args = args

    def __repr__(self):
        return f"CALL {self.dest}, {self.name}, {self.args}"


class CALLSAVE(Instruction):
    def __init__(self, name, dest, args, to_save):
        self.name = name
        self.dest = dest
        self.args = args
        self.to_save = to_save

    def __repr__(self):
        return f"CALLSAVE {self.dest}, {self.name}, {self.args}, {self.to_save}"


class PARAM(Instruction):
    def __init__(self, a):
        self.a = a

    def __repr__(self):
        return f"PARAM {self.a}"


class MOV(Instruction):
    def __init__(self, dest, a):
        self.dest = dest
        self.a = a

    def __repr__(self):
        return f"MOV {self.dest}, {self.a}"


class RET(Instruction):
    def __init__(self, a):
        self.a = a

    def __repr__(self):
        return f"RET {self.a}"


class PUSH(Instruction):
    def __init__(self, a):
        self.a = a

    def __repr__(self):
        return f"PUSH {self.a}"


class POP(Instruction):
    def __init__(self, a):
        self.a = a

    def __repr__(self):
        return f"POP {self.a}"


class POPN(Instruction):
    def __init__(self, n):
        self.n = n

    def __repr__(self):
        return f"POPN {self.n}"