import ir
from . import asmbase
from . import regalloc
from . import transform


class ASM:
    def __init__(self, ir, config):
        self.ir = ir
        self.config = config
        self.regs = None
        self.program = None

    def to_asm(self):
        self.program = asmbase.Program()
        for function in self.ir.functions:
            # transform.pre_live_analysis_transform(function)
            regalloc.LiveAnalysis(function).run()
            transform.PostLiveAnalysisTransform(function).run()
            regalloc.RegAlloc(function).regalloc()
            transform.PostRegallocTransform(function).run()
        print(self.ir)
        for extern in self.ir.externs:
            self.gen_extern(extern)
        for function in self.ir.functions:
            self.gen_function(function)
        return str(self.program)

    def gen_extern(self, extern):
        self.program.text.add_extern(extern.name)

    def gen_function(self, func):
        self.function = func
        self.program.text.add_label(func.name)
        self.program.text.add_instruction("push ebp")
        self.program.text.add_instruction("mov ebp, esp")
        for instruction in func.instructions:
            self.gen_instruction(instruction)
        self.program.text.add_instruction("leave")
        self.program.text.add_instruction("ret\n")

    def gen_instruction(self, instruction):
        if isinstance(instruction, ir.MOV):
            self.gen_MOV(instruction)
        elif isinstance(instruction, ir.BinOp):
            self.gen_binop(instruction)
        elif isinstance(instruction, ir.CALL):
            self.gen_CALL(instruction)
        elif isinstance(instruction, ir.RET):
            self.gen_RET(instruction)
        elif isinstance(instruction, (ir.PUSH, ir.POP)):
            self.gen_push_pop(instruction)
        elif isinstance(instruction, ir.POPN):
            self.gen_POPN(instruction)

    def gen_MOV(self, instruction):
        dest = instruction.dest.register
        argument = instruction.a
        if isinstance(argument, ir.String):
            self.program.rodata.add_string_litteral(argument.value)
            label = self.program.rodata.get_string_litteral_label(argument.value)
            self.program.text.add_instruction(f"mov {dest}, {label}")
        elif isinstance(argument, ir.Integer):
            self.program.text.add_instruction(f"mov {dest}, {argument.value}")
        elif isinstance(argument, ir.Temp):
            self.program.text.add_instruction(f"mov {dest}, {argument.register}")
        elif isinstance(argument, ir.ParameterRef):
            where = 0
            for i, param in enumerate(self.function.parameters):
                if param == ir.Parameter(argument.name, argument.size):
                    where = i
                    break
            #where = self.function.parameters.index(ir.Parameter(argument.name, argument.size))
            self.program.text.add_instruction(f"mov {dest}, [ebp+{where*4 + 8}]")

    def gen_CALL(self, instruction):
        # self.program.text.add_instruction("push eax")
        """
        for argument in reversed(instruction.args):
            self.program.text.add_instruction(f"push {argument.register}")
        """
        self.program.text.add_instruction(f"call {instruction.name}")
        # self.program.text.add_instruction(f"add esp, {len(instruction.args) * 4}")
        if instruction.dest.register != "eax":
            self.program.text.add_instruction(f"mov {instruction.dest.register}, eax")
        # self.program.text.add_instruction("pop eax")

    def gen_RET(self, instruction):
        self.program.text.add_instruction(f"mov eax, {instruction.a.register}")
        self.program.text.add_instruction("leave\nret")

    def gen_push_pop(self, instruction):
        asm = {
            ir.PUSH: "push",
            ir.POP: "pop"
        }[type(instruction)]
        self.program.text.add_instruction(f"{asm} {instruction.a.register}")

    def gen_POPN(self, instruction):
        self.program.text.add_instruction(f"add esp, {instruction.n * 4}")

    def gen_binop(self, instruction):
        asm = {
            ir.ADD: "add",
            ir.SUB: "sub"
        }[type(instruction)]
        dest = instruction.dest.register
        a = instruction.a.register
        if isinstance(instruction.b, ir.Integer):
            b = instruction.b.value
        else:
            b = instruction.b.register
        if dest == a:
            self.program.text.add_instruction(f"{asm} {dest}, {b}")
        else:
            self.program.text.add_instruction(f"{asm} {dest}, {a}")