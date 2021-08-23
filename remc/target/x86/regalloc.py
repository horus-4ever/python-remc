import ir
from collections import namedtuple
from functools import partial


Lifetime = namedtuple("Lifetime", ("name", "start", "stop"))
"""
class Lifetime:
    def __init__(self, start, stop, register=None):
        self.start = start
        self.stop = stop
        self.register = register

    def __repr__(self):
        return f"({self.start}, {self.stop}, reg={self.register})"

    def __iter__(self):
        return iter((self.start, self.stop))
"""

class Register:
    def __init__(self, reference):
        self.reference = reference
        self.lifetimes = [None]

    @property
    def initial_lifetime(self):
        return self.lifetimes[0]

    @initial_lifetime.setter
    def initial_lifetime(self, value):
        self.lifetimes[0] = Lifetime(*value)

    def __repr__(self):
        lifetimes =  ",".join(map(repr, self.lifetimes))
        return f"[{lifetimes}]"


class LiveAnalysis:
    def __init__(self, function):
        self.function = function

    def run(self):
        lifetimes = {}
        for i, instruction in enumerate(self.function.instructions):
            for atom in self.decompose_instruction(instruction):
                if isinstance(atom, (ir.Integer, ir.String, ir.ParameterRef)):
                    continue
                if atom in lifetimes:
                    start, stop = lifetimes[atom]
                    lifetimes[atom] = (start, i)
                else:
                    lifetimes[atom] = (i, i)
        for atom, lifetime in lifetimes.items():
            atom.lifetime = Lifetime(atom.name, *lifetime)
        self.function.temps = list(lifetimes)

    def decompose_instruction(self, instruction):
        if isinstance(instruction, ir.BinOp):
            return instruction.dest, instruction.a, instruction.b
        elif isinstance(instruction, ir.MOV):
            return instruction.dest, instruction.a
        elif isinstance(instruction, ir.CALL):
            return instruction.dest, *instruction.args
        elif isinstance(instruction, ir.RET):
            return instruction.a,
        elif isinstance(instruction, (ir.PUSH, ir.POP)):
            return instruction.a,
        else:
            return ()


class RegAlloc:
    def __init__(self, function):
        self.function = function
        self.registers = {"eax": True, "edx": True, "ecx": True}

    def regalloc(self):
        lifetimes = self.live_analysis()
        print(lifetimes)
        lifetimes = [Lifetime(lifetime, start, stop) for lifetime, (start, stop) in lifetimes.items()]
        lifetimes.sort(key=lambda lifetime: lifetime.start)
        result = {}
        active_lifetimes = []
        for lifetime in lifetimes:
            for active in active_lifetimes:
                if lifetime.start >= active.stop:
                    self._free_register(result[active.name])
                    active_lifetimes.remove(active)
            register = self._allocate_register()
            active_lifetimes.append(lifetime)
            if register is None:
                to_spill = max(active_lifetimes, key=lambda lifetime: lifetime.stop - lifetime.start)
                result[lifetime.name] = result[to_spill.name]
                result[to_spill.name] = None
            else:
                result[lifetime.name] = register
        print(result)
        for lifetime in lifetimes:
            lifetime.name.register = result[lifetime.name]

    """
    def regalloc(self):
        lifetimes = self.live_analysis()
        print(lifetimes)
        lifetimes.sort(key=lambda lifetime: lifetime.initial_lifetime.start)
        result = {}
        active_lifetimes = []
        for lifetime in lifetimes:
            for active in active_lifetimes:
                if lifetime.start >= active.stop:
                    self._free_register(result[active.name])
                    active_lifetimes.remove(active)
            register = self._allocate_register()
            active_lifetimes.append(lifetime)
            if register is None:
                to_spill = max(active_lifetimes, key=lambda lifetime: lifetime.stop - lifetime.start)
                result[lifetime.name] = result[to_spill.name]
                result[to_spill.name] = None
            else:
                result[lifetime.name] = register
        print(result)
        for lifetime in lifetimes:
            lifetime.name.register = result[lifetime.name]
    """
        

    def _free_register(self, register):
        self.registers[register] = True

    def _allocate_register(self):
        for name, available in self.registers.items():
            if available:
                self.registers[name] = False
                return name
        return None

    def live_analysis(self):
        lifetimes = {}
        for i, instruction in enumerate(self.function.instructions):
            for atom in self.decompose_instruction(instruction):
                if isinstance(atom, (ir.Integer, ir.String, ir.ParameterRef)):
                    continue
                if atom in lifetimes:
                    start, stop = lifetimes[atom]
                    lifetimes[atom] = (start, i)
                else:
                    lifetimes[atom] = (i, i)
        return lifetimes

    """
    def live_analysis(self):
        registers = {}
        for i, instruction in enumerate(self.function.instructions):
            for atom in self.decompose_instruction(instruction):
                if isinstance(atom, (ir.Integer, ir.String, ir.ParameterRef)):
                    continue
                if atom in registers:
                    start, stop = registers[atom].initial_lifetime
                    registers[atom].initial_lifetime = (start, i)
                else:
                    register = Register(atom)
                    registers[atom] = register
                    registers[atom].initial_lifetime = (i, i)
        return registers
    """

    def decompose_instruction(self, instruction):
        if isinstance(instruction, ir.BinOp):
            return instruction.dest, instruction.a, instruction.b
        elif isinstance(instruction, ir.MOV):
            return instruction.dest, instruction.a
        elif isinstance(instruction, (ir.CALL, ir.CALLSAVE)):
            return instruction.dest, *instruction.args
        elif isinstance(instruction, ir.RET):
            return instruction.a,
        elif isinstance(instruction, (ir.PUSH, ir.POP)):
            return instruction.a,
        else:
            return ()