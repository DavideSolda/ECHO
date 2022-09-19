from dataclasses import dataclass
from typing import List, Union
from enum import Enum

from ftype import Type, BoolType, IntType, EnumType
from interval import Interval

from literal import *

class Operator(Enum):
    pass

class ArithmeticOperator(Operator):
    Plus = "+"
    Sub  = "-"
    
class BooleanOperator(Operator):
    Eq = "=="
    Neq = "!="

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
            if is_int_fvalue(other):
                return ArithmeticExpr(op = op, values = [self, other])
        raise Exception("only integer varialbes can be used as sum term")

    def __add__(self, other):

        return self._op_int(other, ArithmeticOperator.Plus)

    def __radd__(self, other):

        return self._op_int(other, ArithmeticOperator.Plus)
    
    def __sub__(self, other):
        
        return self._op_int(other, ArithmeticOperator.Sub)
    
    def __rsub__(self, other):                                                                                                                                                               
        return self._op_int(other, ArithmeticOperator.Sub)


class ArithmeticExpr():

    
    def __init__(self, op : ArithmeticOperator, values : List[Union["ArithmenticExpr", int, Variable]]):

        self.values = values
        self.op    = op
        self._types = []
        for v in values:
            try:
                self._types.append(v.types)
            except:
                pass
        self._variables = []
        for v in values:
            if isinstance(v, Variable):
                self._variables.append(v)
            elif isinstance(v, int):
                pass
            else: #ArithmeticExpr
                self._variables += v.variables
                

    @property
    def variables(self):
        return self._variables

    @property
    def types(self):
        return self._types

    def _op_int(self, other, op):

        if is_int_fvalue(other):
            return ArithmeticExpr(op = op, values = [self, other])

        raise Exception("Sum and sub defined only for integer expressions/variables/integers")

    def __add__(self, other):

        return self._op_int(other, ArithmeticOperator.Plus)

    def __radd__(self, other):

        return self._op_int(other, ArithmeticOperator.Plus)
    
    def __sub__(self, other):
        
        return self._op_int(other, ArithmeticOperator.Sub)
    
    def __rsub__(self, other):                                                                                                                                                               
        return self._op_int(other, ArithmenticOperator.Sub)

    def __repr__(self):
        return f"{self.values[0]} {self.op} {self.values[1]}"

def is_int_fvalue(x):
    return isinstance(x, int) \
           or isinstance(x, ArithmeticExpr) \
           or (isinstance(x, Variable) and isinstance(x.type, IntType))

def is_enum_fvalue(x):
    return isinstance(x, str) \
           or (isinstance(x, Variable) and isinstance(x.type, EnumType))


def eq(l, r):
    
    if is_int_fvalue(l) and is_int_fvalue(r):
        return BELiteral(BooleanOperator.Eq, [l, r])

    if is_enum_fvalue(l) and is_enum_fvalue(r):
        return BELiteral(BooleanOperator.Eq, [l, r])

    raise Exception(f"{l} and {r} are not compatible")


def neq(l, r):

    if is_int_fvalue(l) and is_int_fvalue(r):
        return BELiteral(BooleanOperator.Eq, [l, r])

    if is_enum_fvalue(l) and is_enum_fvalue(r):
        return BELiteral(BooleanOperator.Eq, [l, r])

    raise Exception(f"{l} and {r} are not compatible")

def main():
    v = Variable("v", IntType(1, 2))
    print(v)
    print(v + 1)
    l = eq(1+v, 1+v)
    print(f"literal: {l}")
    print(v+v)

    print(v-1)
if __name__ == "__main__":
    main()
