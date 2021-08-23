from .ast import *
from .scope import *
from .function import *
from .types import *
from .statement import *

def _repr_(self):
    return f"{self.__class__.__name__}({self.__dict__})"

def _repr_st_(self):
    return f"{self.__class__.__name__}([[{self.data}]])"

for name in list(globals().values()):
    if isinstance(name, type) and issubclass(name, SymbolTable):
        name.__repr__ = _repr_st_
    elif isinstance(name, type):
        name.__repr__ = _repr_