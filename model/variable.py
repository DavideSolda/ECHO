"""
module for definition of Variable and ArithmeticExpr
which are the possible arguments of a predicate
"""
import sys, os
from dataclasses import dataclass

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, current_dir)

from .ftype import Type, BoolType, AgentType
from .arithmetic_expression import ArithmeticExpr, is_int_fvalue, \
    ArithmeticOperator


@dataclass
class Variable():
    """Variable of a given ftype.Type"""
    def __init__(self, name: str, vtype: Type, agent=False):
        if isinstance(vtype, BoolType):
            raise Exception("""do not define a varible boolean,
            define instead a boolean fluent""")
        self._name = name
        self._vtype = vtype
        self._agent = agent

    def is_agent(self) -> bool:
        """Returns True iff the variable represents an agent"""
        return isinstance(self._vtype, AgentType)

    @property
    def name(self):
        """Get the name of the variable"""
        return self._name

    @property
    def type(self):
        """Get the ftype.Typeof the variable"""
        return self._vtype

    def __hash__(self):
        return hash(self.name)#**hash(self.type)

    def __eq__(self, var):
        return var.name == self.name and var.type == self.type

    def __repr__(self):
        return f"var {self.name} of type {self.type}"

    def __str__(self):
        return self.name

    def _op_int(self, other, operator):
        """Return an arithmetic expression"""
        if self.type.is_int_type():
            if is_int_fvalue(other):
                return ArithmeticExpr(op=operator, values=[self, other])
        raise Exception("only integer varialbes can be used as sum term")

    def __add__(self, other):
        return self._op_int(other, ArithmeticOperator.Plus)

    def __radd__(self, other):
        return self._op_int(other, ArithmeticOperator.Plus)

    def __sub__(self, other):
        return self._op_int(other, ArithmeticOperator.Sub)

    def __rsub__(self, other):
        return self._op_int(other, ArithmeticOperator.Sub)
