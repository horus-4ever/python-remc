class StringLitterals:
    def __init__(self):
        self.data = []

    def register(self, string):
        if string not in self.data:
            self.data.append(string)

    def get_id(self, string):
        return self.data.index(string)

    def __iter__(self):
        return iter(self.data)


class rodata:
    BASE_STRLIT_NAME = "string.SL_"
    def __init__(self):
        self.string_litterals = StringLitterals()

    def add_string_litteral(self, string):
        self.string_litterals.register(string)

    def get_string_litteral_label(self, string):
        return f"{self.BASE_STRLIT_NAME}{self.string_litterals.get_id(string)}"

    def __str__(self):
        result = "section .rodata\n"
        for i, string in enumerate(self.string_litterals):
            result += f"{self.BASE_STRLIT_NAME}{i}: db '{string}', 0\n"
        return result


class text:
    def __init__(self):
        self.externs = []
        self.code = []

    def add_extern(self, extern_decl):
        self.externs.append(extern_decl)

    def add_label(self, label_name):
        self.code.append(f"{label_name}:")

    def add_instruction(self, instruction):
        self.code.append(instruction)

    def __str__(self):
        result = "section .text\nglobal main\n"
        for extern in self.externs:
            result += f"extern {extern}\n"
        result += "\n"
        for code in self.code:
            result += f"{code}\n"
        return result


class Program:
    def __init__(self):
        self.rodata = rodata()
        self.text = text()

    def __str__(self):
        return f"{self.rodata}\n{self.text}"