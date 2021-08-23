# Generated from language.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .languageParser import languageParser
else:
    from languageParser import languageParser

# This class defines a complete generic visitor for a parse tree produced by languageParser.

class languageVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by languageParser#entry_point.
    def visitEntry_point(self, ctx:languageParser.Entry_pointContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#extern_declaration.
    def visitExtern_declaration(self, ctx:languageParser.Extern_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#function_prototype.
    def visitFunction_prototype(self, ctx:languageParser.Function_prototypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#function_declaration.
    def visitFunction_declaration(self, ctx:languageParser.Function_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#kind.
    def visitKind(self, ctx:languageParser.KindContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#normal_type.
    def visitNormal_type(self, ctx:languageParser.Normal_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#pointer_type.
    def visitPointer_type(self, ctx:languageParser.Pointer_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#block.
    def visitBlock(self, ctx:languageParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#statement.
    def visitStatement(self, ctx:languageParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#expression.
    def visitExpression(self, ctx:languageParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#function_call.
    def visitFunction_call(self, ctx:languageParser.Function_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#factor.
    def visitFactor(self, ctx:languageParser.FactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#non_expression.
    def visitNon_expression(self, ctx:languageParser.Non_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#return_statement.
    def visitReturn_statement(self, ctx:languageParser.Return_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#parameters.
    def visitParameters(self, ctx:languageParser.ParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#parameter.
    def visitParameter(self, ctx:languageParser.ParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by languageParser#arguments.
    def visitArguments(self, ctx:languageParser.ArgumentsContext):
        return self.visitChildren(ctx)



del languageParser