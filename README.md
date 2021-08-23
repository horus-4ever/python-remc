# RemC

## About
RemC is a C-like language designed to be, overall, C with generics. For now, it only targets x86 assembly.

## Features
RemC adds a set of new keywords and data types to C, in order to remove syntaxical and type ambiguities.


Features :
- [x] primitive data types: `uint8`, `uint16`, `uint32`, `int8`, `int16`, `int32`
- [x] primitive type alias: `int`, `char`
- [ ] read-only string litterals
- [ ] pointers (`type&`) and immutable pointed value (`immut type&`)
- [ ] functions
- [ ] structures
- [ ] enumerations
- [ ] genericity (both functions and structures / enumerations)
- [ ] full compatibility with C


Implementation :
- [ ] Full grammar
- [ ] Lexing and parsing (antlr4)
- [ ] Static analysis (name- and type-checker)
- [ ] Intermediate representation (register-based)
- [ ] Live analysis
- [ ] Register allocation
- [ ] Translation to target assembler


## Usage
To run any program, execute `python3 remc <filename.remc>`, then build the generated asm (in `out/`) manually, with `nasm` and `gcc` for instance.