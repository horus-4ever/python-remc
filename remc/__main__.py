import sys
import os
import json
import importlib
import subprocess
from antlr4 import *
from antlr_output.languageLexer import languageLexer
from antlr_output.languageParser import languageParser
from parser import Parser
from analysis import Typechecker, NameChecker
from translate import Translate

# alias antlr4='java -jar /usr/local/lib/antlr-4.9.2-complete.jar'
# cd remc; antlr4 -o antlr_output/ -Dlanguage=Python3 -visitor language.g4; cd ..

with open(sys.argv[1]) as doc:
    CODE = doc.read()

TARGET = "x86"
with open(os.path.join(os.getcwd(), "remc", "target", TARGET, "config.json")) as file:
    CONFIG = json.load(file)
asm = importlib.import_module(".".join(["target", TARGET, "asm"]))

input = InputStream(CODE)

lexer = languageLexer(input)
tokens = CommonTokenStream(lexer)
parser = languageParser(tokens)
tree = parser.entry_point()

# print(tree.toStringTree(recog=parser))

ast_parser = Parser(CONFIG)
ast = ast_parser.visitEntry_point(tree)

namechecker = NameChecker(ast, CONFIG)
namechecker.check()

typechecker = Typechecker(ast, CONFIG)
typechecker.typecheck()
# print(ast)

translator = Translate(ast, CONFIG)
ir = translator.to_ir()
print(ir)

codegen = asm.ASM(ir, CONFIG)

with open("out/out.s", "w") as doc:
    doc.write(codegen.to_asm())

subprocess.run(["sh", "out/build.sh"])
