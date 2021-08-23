grammar language;

IDENTIFIER :    [A-Za-z] ([A-Za-z] | '_')* ;
NUMBER:         [0-9]+ ;
STRING:         '"'.*?'"' ;
COMMENTS:       '//'.*?[\n] -> skip ;
WS:             [ \t\r\n]+ -> skip ;
ELIPSIS:        '...' ;
PLUS:           '+' ;
MINUS:          '-' ;

entry_point:                (function_declaration | extern_declaration)* ;

extern_declaration:         'extern' (function_prototype) ';' ;

function_prototype:         kind IDENTIFIER '(' parameters? ')' ;
function_declaration:       function_prototype block ;

kind:                       normal_type | pointer_type ;
normal_type:                IDENTIFIER ;
pointer_type:               IDENTIFIER '&' ;

block:                      '{' statement* '}' ;
statement:                  non_expression | expression ';' ;
expression:
    expression (PLUS | MINUS) expression
    | function_call
    | factor
    ;
function_call:              IDENTIFIER '(' arguments? ')' ;
factor:                     STRING | NUMBER | IDENTIFIER ;

non_expression:             return_statement ';' ;
return_statement:           'return' expression ;

parameters:                 parameter (',' parameter)* (',' ELIPSIS)? ;
parameter:                  kind IDENTIFIER ;
arguments:                  expression (',' expression)* ;