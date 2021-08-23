import ast


class Typechecker:
    def __init__(self, AST, config):
        self.ast = AST
        self.config = config

    def typecheck(self):
        for function_prototype in self.ast.scope.find_all(ast.FunctionPrototype):
            self.check_function_prototype(function_prototype)
        for function in self.ast.scope.find_all(ast.Function):
            self.check_function(function)

    def check_function_prototype(self, function):
        return_type_name = function.return_type.name
        ast_scope = self.ast.scope
        lookup_result = ast_scope.find(return_type_name)
        if lookup_result is None:
            raise TypeError(f"Type {return_type_name} not found.")
        function.return_type.type_ref = lookup_result
        self.check_parameters(function)

    def check_function(self, function):
        self.check_function_prototype(function)
        self.check_block(function.block)

    def check_parameters(self, function):
        for name, parameter in function.parameters:
            type_name = parameter.kind.name
            lookup_result = self.ast.scope.find(type_name)
            if lookup_result is None:
                raise TypeError(f"Type {type_name} not found.")
            parameter.kind.type_ref = lookup_result

    def check_block(self, block):
        for statement in block.statements:
            self.check_statement(statement)

    def check_statement(self, statement):
        if isinstance(statement, ast.Expression):
            self.check_expression(statement)
        elif isinstance(statement, ast.Return):
            self.check_expression(statement.expression)

    def check_expression(self, expression):
        if isinstance(expression, ast.StringLitteral):
            expression.kind = ast.PointerType("char", is_immut=True)
            expression.kind.type_ref = self.ast.builtin_scope["char"]
        elif isinstance(expression, ast.FunctionCall):
            self.check_function_call(expression)
        elif isinstance(expression, ast.BinOp):
            self.check_expression(expression.left)
            self.check_expression(expression.right)
        elif isinstance(expression, ast.VariableRef):
            self.check_variable_ref(expression)

    def check_variable_ref(self, expression):
        expression.kind = expression.ref.kind
        #print(expression.ref.kind.type_ref)

    def check_function_call(self, expression):
        for argument in expression.arguments:
            self.check_expression(argument)