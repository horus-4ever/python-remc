# Generated from language.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .languageParser import languageParser
else:
    from languageParser import languageParser

# This class defines a complete listener for a parse tree produced by languageParser.
class languageListener(ParseTreeListener):

    # Enter a parse tree produced by languageParser#entry_point.
    def enterEntry_point(self, ctx:languageParser.Entry_pointContext):
        pass

    # Exit a parse tree produced by languageParser#entry_point.
    def exitEntry_point(self, ctx:languageParser.Entry_pointContext):
        pass


    # Enter a parse tree produced by languageParser#extern_declaration.
    def enterExtern_declaration(self, ctx:languageParser.Extern_declarationContext):
        pass

    # Exit a parse tree produced by languageParser#extern_declaration.
    def exitExtern_declaration(self, ctx:languageParser.Extern_declarationContext):
        pass


    # Enter a parse tree produced by languageParser#function_prototype.
    def enterFunction_prototype(self, ctx:languageParser.Function_prototypeContext):
        pass

    # Exit a parse tree produced by languageParser#function_prototype.
    def exitFunction_prototype(self, ctx:languageParser.Function_prototypeContext):
        pass


    # Enter a parse tree produced by languageParser#function_declaration.
    def enterFunction_declaration(self, ctx:languageParser.Function_declarationContext):
        pass

    # Exit a parse tree produced by languageParser#function_declaration.
    def exitFunction_declaration(self, ctx:languageParser.Function_declarationContext):
        pass


    # Enter a parse tree produced by languageParser#kind.
    def enterKind(self, ctx:languageParser.KindContext):
        pass

    # Exit a parse tree produced by languageParser#kind.
    def exitKind(self, ctx:languageParser.KindContext):
        pass


    # Enter a parse tree produced by languageParser#normal_type.
    def enterNormal_type(self, ctx:languageParser.Normal_typeContext):
        pass

    # Exit a parse tree produced by languageParser#normal_type.
    def exitNormal_type(self, ctx:languageParser.Normal_typeContext):
        pass


    # Enter a parse tree produced by languageParser#pointer_type.
    def enterPointer_type(self, ctx:languageParser.Pointer_typeContext):
        pass

    # Exit a parse tree produced by languageParser#pointer_type.
    def exitPointer_type(self, ctx:languageParser.Pointer_typeContext):
        pass


    # Enter a parse tree produced by languageParser#block.
    def enterBlock(self, ctx:languageParser.BlockContext):
        pass

    # Exit a parse tree produced by languageParser#block.
    def exitBlock(self, ctx:languageParser.BlockContext):
        pass


    # Enter a parse tree produced by languageParser#statement.
    def enterStatement(self, ctx:languageParser.StatementContext):
        pass

    # Exit a parse tree produced by languageParser#statement.
    def exitStatement(self, ctx:languageParser.StatementContext):
        pass


    # Enter a parse tree produced by languageParser#expression.
    def enterExpression(self, ctx:languageParser.ExpressionContext):
        pass

    # Exit a parse tree produced by languageParser#expression.
    def exitExpression(self, ctx:languageParser.ExpressionContext):
        pass


    # Enter a parse tree produced by languageParser#function_call.
    def enterFunction_call(self, ctx:languageParser.Function_callContext):
        pass

    # Exit a parse tree produced by languageParser#function_call.
    def exitFunction_call(self, ctx:languageParser.Function_callContext):
        pass


    # Enter a parse tree produced by languageParser#factor.
    def enterFactor(self, ctx:languageParser.FactorContext):
        pass

    # Exit a parse tree produced by languageParser#factor.
    def exitFactor(self, ctx:languageParser.FactorContext):
        pass


    # Enter a parse tree produced by languageParser#non_expression.
    def enterNon_expression(self, ctx:languageParser.Non_expressionContext):
        pass

    # Exit a parse tree produced by languageParser#non_expression.
    def exitNon_expression(self, ctx:languageParser.Non_expressionContext):
        pass


    # Enter a parse tree produced by languageParser#return_statement.
    def enterReturn_statement(self, ctx:languageParser.Return_statementContext):
        pass

    # Exit a parse tree produced by languageParser#return_statement.
    def exitReturn_statement(self, ctx:languageParser.Return_statementContext):
        pass


    # Enter a parse tree produced by languageParser#parameters.
    def enterParameters(self, ctx:languageParser.ParametersContext):
        pass

    # Exit a parse tree produced by languageParser#parameters.
    def exitParameters(self, ctx:languageParser.ParametersContext):
        pass


    # Enter a parse tree produced by languageParser#parameter.
    def enterParameter(self, ctx:languageParser.ParameterContext):
        pass

    # Exit a parse tree produced by languageParser#parameter.
    def exitParameter(self, ctx:languageParser.ParameterContext):
        pass


    # Enter a parse tree produced by languageParser#arguments.
    def enterArguments(self, ctx:languageParser.ArgumentsContext):
        pass

    # Exit a parse tree produced by languageParser#arguments.
    def exitArguments(self, ctx:languageParser.ArgumentsContext):
        pass



del languageParser