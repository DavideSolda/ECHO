"""
module for definition of Variable and ArithmeticExpr
which are the possible arguments of a predicate
"""
import os, sys
from typing import List, Union
from enum import Enum

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, current_dir)

from .ftype import IntType, EnumType

class ArithmeticOperator(Enum):
    """Arithmetic operators"""
    Plus = "+"
    Sub = "-"


class ArithmeticExpr():
    """
    class for arithmentic expressions involving variables, for istance
    X + 3 or X + Y
    """
    def __init__(self, op: ArithmeticOperator,
                 values: List[Union['ArithmenticExpr', int, 'Variable']]):

        assert len(values) == 2  # till now only binary arithmentic operators
        self._values = values
        self._op = op
        self._types = []
        #  collect subtypes:
        for value in values:
            if isinstance(value, int):
                continue
            if hasattr(value, 'type'):
                self._types.append(value.type)
            elif hasattr(value, 'types'):
                self._types += value.types
            else:
                raise ValueError(f"{value} as arithmetic term")

        #  collect variables:
        self._variables = []
        for v in values:
            if isinstance(v, type(self)):
                self._variables += v.variables
            elif isinstance(v, int):
                continue
            else:  # Variable
                self._variables.append(v)

    @property
    def values(self) -> List[Union['ArithmenticExpr', int, 'Variable']]:
        return self._values

    @property
    def operator(self):
        return self._op

    @property
    def variables(self):
        return self._variables

    @property
    def types(self):
        return self._types

    def _op_int(self, other, op):
        if is_int_fvalue(other):
            return ArithmeticExpr(op=op, values=[self, other])

        raise Exception("""Sum and sub defined only for
        integer expressions/variables/integers""")

    def __add__(self, other):

        return self._op_int(other, ArithmeticOperator.Plus)

    def __radd__(self, other):

        return self._op_int(other, ArithmeticOperator.Plus)

    def __sub__(self, other):

        return self._op_int(other, ArithmeticOperator.Sub)

    def __rsub__(self, other):

        return self._op_int(other, ArithmeticOperator.Sub)

    def __repr__(self):
        return f"{self.values[0]} {self.operator} {self.values[1]}"


def is_int_fvalue(fvalue) -> bool:
    """Check if fvalue (the fluent parameter) is int"""
    return isinstance(fvalue, (int, ArithmeticExpr)) or \
        type(fvalue).__name__ == 'Variable' and \
        isinstance(fvalue.type, IntType)


def is_enum_fvalue(fvalue) -> bool:
    """Check if fvalue (the fluent parameter) is enum"""
    return isinstance(fvalue, str) or \
        type(fvalue).__name__ == 'Variable' and \
        isinstance(fvalue.type, EnumType)
