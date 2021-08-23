from collections import deque
import ast


class _Scopes:
    def __init__(self, scopes):
        self.scopes = scopes

    def __getitem__(self, key):
        return self.scopes[key]

    def enter(self, scope):
        return _Scope(self, scope)


class _Scope:
    def __init__(self, parent, scope):
        self.parent = parent
        self.scope = scope

    def __enter__(self):
        self.parent.scopes.append(self.scope)
        return self

    def __exit__(self, *_):
        self.parent.scopes.pop()


class NameChecker:
    def __init__(self, ast, config):
        self.ast = ast
        self.config = config
        self.scopes = _Scopes(deque([self.ast.scope]))
    
    @property
    def current_scope(self):
        return self.scopes[-1]

    @property
    def global_scope(self):
        return self.scopes[0]

    def check(self):
        for function in self.global_scope.find_all(ast.Function):
            self.check_function(function)

    def check_function(self, function):
        self.check_parameters(function.parameters)
        self.check_block(function.block)

    def check_parameters(self, parameters):
        pass

    def check_block(self, block):
        with self.scopes.enter(block.scope):
            self.check_statements(block.statements)

    def check_statements(self, statements):
        for statement in statements:
            self.check_statement(statement)

    def check_statement(self, statement):
        if isinstance(statement, ast.Expression):
            self.check_expression(statement)
        elif isinstance(statement, ast.NonExpression):
            self.check_non_expression(statement)

    def check_non_expression(self, statement):
        if isinstance(statement, ast.Return):
            self.check_expression(statement.expression)

    def check_expression(self, expression):
        if isinstance(expression, ast.BinOp):
            self.check_expression(expression.left)
            self.check_expression(expression.right)
        elif isinstance(expression, ast.FunctionCall):
            for expression in expression.arguments:
                self.check_expression(expression)
        elif isinstance(expression, ast.VariableRef):
            self.check_variable_ref(expression)

    def check_variable_ref(self, expression):
        lookup = self.current_scope.find(expression.name, constraints=(ast.Variable,))
        expression.ref = lookup