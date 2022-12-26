"""This module contain the definition of Fluent"""
import sys, os
from dataclasses import dataclass
from typing import ClassVar

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, current_dir)

from .predicate import Literal
from .arithmetic_expression import ArithmeticExpr
from .ftype import BoolType, Type
from .variable import Variable


@dataclass(frozen=True)
class Fluent():
    """Fluent class to represnet classical planning fluents"""
    default_type : ClassVar = BoolType('bool')
    name: str
    type: Type = default_type

    def __post_init__(self):

        if not isinstance(self.name, str):
            raise Exception("The fluent name must be a string")

        if not isinstance(self.type, Type):
            raise Exception("""The fluent type must be \
                                an instance of fType.Type""")

    def __eq__(self, other):
        return self.name == other.name and self.type == other.type

    def __repr__(self):
        return f"fluent {self.name} of type {self.type}"

    @staticmethod
    def _check_type(arg, _type: Type, pos: int) -> bool:
        """check if the value {arg} has type types[{pos}]"""
        str_error = f"""Fluent has type {_type} at position {pos},\
        but an argument: \"{arg}\" was given"""
        if _type.is_int_type():

            if isinstance(arg, int) and _type.min <= arg <= _type.max:
                return True
            if isinstance(arg, ArithmeticExpr):
                #I do not add other checks
                return True
            if arg.type.contained_in(_type):
                #if it is a variable, its domain should be contained
                return True
    
        if _type.is_enum_type():
            if isinstance(arg, str) and arg in _type.enum_values or \
               arg.type.contained_in(_type):
                return True
            
        if _type.is_bool_type():
            if isinstance(arg, bool) or arg.type.is_bool_type():
                return True

        raise Exception(str_error)

    def __call__(self, *args) -> Literal:

        if len(self.type) != len(args):
            raise Exception(f"""Fluent {self.name} has {len(self.type)} arguments,
                            but {len(args)} were given""")

        vars = []
        for arg in args:
            if isinstance(arg, Variable):
                vars.append(arg)

        if len(self.type) == 0:
            return Literal(negated = False, types = [self.type],
                           variables = [], fluent = self, args = [])

        if len(self.type) == 1:
            self._check_type(args[0], self.type, 0)
            return Literal(negated = False, types = [self.type],
                           variables = vars, fluent = self, args = list(args))

        c = 0
        for arg, t in zip(args, self.type):
            self._check_type(arg, t, c)
            c += 1
        return Literal(negated = False, types = [self.type], variables = vars,
                       fluent = self, args = list(args))
