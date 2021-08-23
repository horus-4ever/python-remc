import ast
import ir


class RegAlloc:
    def __init__(self):
        self.counter = 0

    def require_new_reg(self):
        result = ir.Temp(self.counter)
        self.counter += 1
        return result


class Translate:
    def __init__(self, ast, config):
        self.ast = ast
        self.config = config
        self.result = None
        self.regs = None
        self.instructions = None

    def to_ir(self):
        result = ir.Program()
        for function in self.ast.scope.find_all(ast.Function):
            self.instructions = []
            function = self.translate_function(function)
            result.add_function(function)
        for function in self.ast.scope.find_all(ast.FunctionPrototype):
            result.add_extern(ir.Extern(function.name))
        return result

    def translate_function(self, function):
        self.regs = RegAlloc()
        name = function.name
        self.translate_block(function.block)
        return_size = function.return_type.type_ref.size
        parameters = [ir.Parameter(name, parameter.kind.type_ref.size) for name, parameter in function.parameters]
        return ir.Function(name, parameters, return_size, self.instructions)

    def emit(self, instruction):
        self.instructions.append(instruction)

    @property
    def last_instruction(self):
        return self.instructions[-1]

    def translate_block(self, block):
        for statement in block.statements:
            self.translate_statement(statement)

    def translate_statement(self, statement):
        if isinstance(statement, ast.Expression):
            return self.translate_expression(statement)
        elif isinstance(statement, ast.Return):
            return self.translate_return(statement)

    def translate_return(self, statement):
        self.translate_expression(statement.expression)
        dest = self.last_instruction.dest
        self.emit(ir.RET(dest))

    def translate_expression(self, expression):
        if isinstance(expression, ast.BinOp):
            return self.translate_binop(expression)
        elif isinstance(expression, ast.IntLitteral):
            return self.translate_int_litteral(expression)
        elif isinstance(expression, ast.StringLitteral):
            return self.translate_str_litteral(expression)
        elif isinstance(expression, ast.VariableRef):
            self.translate_variable_ref(expression)
        elif isinstance(expression, ast.FunctionCall):
            self.translate_function_call(expression)

    def translate_function_call(self, expression):
        regs = []
        for argument in expression.arguments:
            self.translate_expression(argument)
            regs.append(self.last_instruction.dest)
        reg = self.regs.require_new_reg()
        self.emit(ir.CALL(expression.name, reg, tuple(regs)))

    def translate_argument(self, expression):
        self.translate_expression(expression)
        self.emit(ir.PARAM(self.last_instruction.dest))

    def translate_int_litteral(self, expression):
        reg = self.regs.require_new_reg()
        self.emit(ir.MOV(reg, ir.Integer(expression.value)))

    def translate_str_litteral(self, expression):
        reg = self.regs.require_new_reg()
        self.emit(ir.MOV(reg, ir.String(expression.value)))

    def translate_variable_ref(self, expression):
        reg = self.regs.require_new_reg()
        TYPE = {
            ast.Parameter: ir.ParameterRef,
            ast.Variable: ir.Variable
        }[type(expression.ref)]
        self.emit(ir.MOV(reg, TYPE(expression.name, expression.kind.type_ref.size)))

    def translate_binop(self, expression):
        OP = {
            ast.Add: ir.ADD,
            ast.Sub: ir.SUB
        }[type(expression)]
        """
        self.translate_expression(expression.left)
        left = self.last_instruction.dest
        """
        if isinstance(expression.right, ast.IntLitteral):
            right = ir.Integer(expression.right.value)
        else:
            self.translate_expression(expression.right)
            right = self.last_instruction.dest
        dest = self.regs.require_new_reg()
        
        self.translate_expression(expression.left)
        left = self.last_instruction.dest
        self.emit(OP(dest, left, right))
        