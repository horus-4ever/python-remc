from antlr_output.languageVisitor import languageVisitor
import ast
from collections import deque


class Parser(languageVisitor):
    def __init__(self, config):
        self.config = config
        self.builtin_scope = ast.SymbolTable()
        for name, size in config["builtin_types"].items():
            self.builtin_scope[name] = ast.BuiltinType(name, size)
        self.scopes = deque([])

    def visitEntry_point(self, ctx):
        global_scope = ast.SymbolTable(parent_scope=self.builtin_scope)
        self.scopes.append(global_scope)
        for extern in ctx.extern_declaration():
            decl = self.visitExtern_declaration(extern)
            global_scope[decl.name] = decl
        for function in ctx.function_declaration():
            func = self.visitFunction_declaration(function)
            global_scope[func.name] = func
        self.scopes.pop()
        return ast.AST(global_scope, self.builtin_scope)

    def visitExtern_declaration(self, ctx):
        return self.visitFunction_prototype(ctx.function_prototype())

    def visitFunction_prototype(self, ctx):
        func_name = ctx.IDENTIFIER().getText()
        parameters = self.visitParameters(ctx.parameters())
        return_type = self.visitKind(ctx.kind())
        return ast.FunctionPrototype(func_name, return_type, parameters)
    
    def visitFunction_declaration(self, ctx):
        func = self.visitFunction_prototype(ctx.function_prototype())
        func_name = func.name
        parameters = func.parameters
        return_type = func.return_type
        block = self.visitBlock(ctx.block())
        parameters.child_scopes.append(block.scope)
        block.scope.parent_scope = parameters
        return ast.Function(func_name, return_type, parameters, block)

    def visitParameters(self, ctx):
        result = ast.Parameters()
        result.parent_scope = self.scopes[-1]
        self.scopes[-1].child_scopes.append(result)
        self.scopes.append(result)
        if ctx is None:
            return result
        for parameter in ctx.parameter():
            parameter = self.visitParameter(parameter)
            result[parameter.name] = parameter
        if ctx.ELIPSIS():
            result.variable_length = True
        self.scopes.pop()
        return result

    def visitParameter(self, ctx):
        kind = self.visitKind(ctx.kind())
        name = ctx.IDENTIFIER().getText()
        return ast.Parameter(name, kind)

    def visitKind(self, ctx):
        if ctx.normal_type():
            return self.visitNormal_type(ctx.normal_type())
        else:
            return self.visitPointer_type(ctx.pointer_type())

    def visitNormal_type(self, ctx):
        type_name = ctx.IDENTIFIER().getText()
        return ast.NormalType(type_name)

    def visitPointer_type(self, ctx):
        type_name = ctx.IDENTIFIER().getText()
        return ast.PointerType(type_name)

    def visitBlock(self, ctx):
        block_scope = ast.SymbolTable(self.scopes[-1])
        self.scopes[-1].child_scopes.append(block_scope)
        self.scopes.append(block_scope)
        statements = []
        for statement in ctx.statement():
            if statement.expression():
                result = self.visitExpression(statement.expression())
                statements.append(result)
            elif statement.non_expression():
                result = self.visitNon_expression(statement.non_expression())
                statements.append(result)
        self.scopes.pop()
        return ast.Block(statements, block_scope)

    def visitNon_expression(self, ctx):
        if ctx.return_statement():
            return self.visitReturn_statement(ctx.return_statement())

    def visitReturn_statement(self, ctx):
        if ctx.expression():
            expression = self.visitExpression(ctx.expression())
        else:
            expression = None
        return ast.Return(expression)
    
    def visitExpression(self, ctx):
        if ctx.function_call():
            return self.visitFunction_call(ctx.function_call())
        elif ctx.factor():
            return self.visitFactor(ctx.factor())
        elif ctx.PLUS():
            left, right = map(self.visitExpression, ctx.expression())
            return ast.Add(left, right)
        elif ctx.MINUS():
            left, right = map(self.visitExpression, ctx.expression())
            return ast.Add(left, right)

    def visitFactor(self, ctx):
        if ctx.STRING():
            return ast.StringLitteral(ctx.STRING().getText()[1:-1])
        elif ctx.NUMBER():
            return ast.IntLitteral(int(ctx.NUMBER().getText()))
        elif ctx.IDENTIFIER():
            return self.visitVariable_ref(ctx.IDENTIFIER().getText())

    def visitVariable_ref(self, variable_name):
        return ast.VariableRef(variable_name)

    def visitFunction_call(self, ctx):
        func_name = ctx.IDENTIFIER().getText()
        arguments = self.visitArguments(ctx.arguments())
        return ast.FunctionCall(func_name, arguments)

    def visitArguments(self, ctx):
        result = []
        if ctx is None:
            return result
        for expression in ctx.expression():
            result.append(self.visitExpression(expression))
        return result