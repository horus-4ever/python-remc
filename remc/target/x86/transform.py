import ir


class PreLiveAnalysisTransform:
    def __init__(self, instructions):
        self.instructions = instructions
        self.result = []

    def emit(self, instruction):
        self.result.append(instruction)

    def transform(self):
        for i, instruction in enumerate(self.instructions):
            self.transform_instruction(instruction, i)
        return self.result

    def transform_instruction(self, instruction, i):
        self.emit(instruction)


class PostLiveAnalysisTransform:
    def __init__(self, function):
        self.function = function
        self.result = []

    def emit(self, instruction):
        self.result.append(instruction)

    def run(self):
        for i, instruction in enumerate(self.function.instructions):
            self.transform_instruction(instruction, i)
        self.function.instructions = self.result

    def transform_instruction(self, instruction, i):
        if isinstance(instruction, ir.BinOp):
            self.transform_binop(instruction, i)
        elif isinstance(instruction, ir.CALL):
            self.transform_call(instruction, i)
        else:
            self.emit(instruction)

    def transform_binop(self, instruction, i):
        dest, a = instruction.dest, instruction.a
        if a.lifetime.stop > i:
            self.emit(ir.MOV(dest, a))
        self.emit(instruction)

    def transform_call(self, instruction, i):
        to_save = []
        for temp in self.function.temps:
            if temp.lifetime.start < i and temp.lifetime.stop > i:
                to_save.append(temp)
        to_save_not_arg = set(to_save) - set(instruction.args)
        self.emit(ir.CALLSAVE(instruction.name, instruction.dest, instruction.args, to_save))


class PostRegallocTransform:
    def __init__(self, function):
        self.function = function
        self.result = []

    def emit(self, instruction):
        self.result.append(instruction)

    def run(self):
        for i, instruction in enumerate(self.function.instructions):
            self.transform_instruction(instruction, i)
        self.function.instructions = self.result

    def transform_instruction(self, instruction, i):
        if isinstance(instruction, ir.CALLSAVE):
            self.transform_call(instruction, i)
        else:
            self.emit(instruction)
    
    def transform_call(self, instruction, i):
        args = instruction.args
        to_save = instruction.to_save
        to_save_not_args = tuple(set(to_save) - set(args))
        # print("SAVE", to_save, to_save_not_args)
        intersection = []
        for i, arg in enumerate(args):
            if arg in to_save:
                intersection.append(i)
        for save in to_save_not_args:
            self.emit(ir.PUSH(save))
        for arg in reversed(args):
            self.emit(ir.PUSH(arg))
        self.emit(ir.CALL(instruction.name, instruction.dest, ()))
        counter = 0
        for i, arg in enumerate(args):
            if i in intersection:
                if counter != 0:
                    self.emit(ir.POPN(counter))
                counter = 0
                self.emit(ir.POP(arg))
            else:
                counter += 1
        if counter != 0:
            self.emit(ir.POPN(counter))
        for arg in reversed(to_save_not_args):
            self.emit(ir.POP(arg))



def pre_live_analysis_transform(function):
    result = PreLiveAnalysisTransform(function.instructions).transform()
    function.instructions = result

def post_live_analysis_transform(function):
    result = PostLiveAnalysisTransform(function).transform()
    function.instructions = result