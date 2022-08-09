from dataclasses import dataclass
from enum import Enum

from ftype import Type, BoolType, IntType, EnumType
from interval import Interval

class Operator(Enum):
    Plus = "+"
    Sub  = "-"

@dataclass
class Variable():

    def __init__(self, name : str, vtype : Type):

        if isinstance(vtype, BoolType):
            raise Exception("do not define a varible boolean, define instead a boolean fluent")

        self._name = name
        self._vtype = vtype

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._vtype

    def __eq__(self, var):
        return var.name == self.name and var.type == self.type

    def __repr__(self):
        return f"var {self.name} of type {self.type}"

    def _op_int(self, other, op):
        
        if self.type.is_int_type():
            if isinstance(other, int) or self.type == other.type:
                return Expr(op = op, left = self, right = other, t = self.type)
        raise Exception("only integer varialbes can be used as sum term")

    def __add__(self, other):

        return self._op_int(other, Operator.Plus)

    def __radd__(self, other):

        return self._op_int(other, Operator.Plus)
    
    def __sub__(self, other):
        
        return self._op_int(other, Operator.Sub)
    
    def __rsub__(self, other):                                                                                                                                                               

        return self._op_int(other, Operator.Sub)

class Expr():

    
    def __init__(self, op : Operator, left, right, t):

        self.left = left
        self.right = right
        self.op    = op
        self.type  = t

    def __repr__(self):
        return f"{self.left} {self.op} {self.right}"

    def __equal__(self, other):
        Literal()
def main():
    v = Variable("v", IntType(1, 2))
    print(v)
    print(v + 1)
    print(1+v)
    print(v+v)

    print(v-1)
if __name__ == "__main__":
    main()
