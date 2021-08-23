class SymbolTable:
    def __init__(self, parent_scope=None):
        self.parent_scope = parent_scope
        self.child_scopes = []
        self.data = {}

    def find(self, key, constraints=()):
        current_scope = self
        while current_scope is not None:
            if key in current_scope.data:
                result = current_scope.data[key]
                if not constraints:
                    return result
                elif isinstance(result, constraints):
                    return result
                else:
                    break
            current_scope = current_scope.parent_scope
        return None

    def find_all(self, constraints):
        result = []
        current_scope = self
        while current_scope is not None:
            for key, value in current_scope.data.items():
                if isinstance(value, constraints):
                    result.append(value)
            current_scope = current_scope.parent_scope
        return result

    def local_find(self, key, constraints=()):
        if key in self.data:
            result = self.data[key]
            if not constraints:
                return result
            elif isinstance(result, constraints):
                return result
        return None

    def __getitem__(self, key):
        return self.find(key)

    def __setitem__(self, key, value):
        self.data[key] = value


class Parameters(SymbolTable):
    def __init__(self, parent_scope=None):
        super().__init__(parent_scope)
        self.variable_length = False

    def __iter__(self):
        return iter(self.data.items())


class FunctionScope(SymbolTable):
    pass


class Block:
    def __init__(self, statements, scope):
        self.statements = statements
        self.scope = scope