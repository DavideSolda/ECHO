"""This module contain the definition of Fluent"""
from dataclasses import dataclass

from predicate import Literal
from arithmetic_expression import ArithmeticExpr
from ftype import BoolType, Type


@dataclass(frozen=True)
class Fluent():
    """Fluent class to represnet classical planning fluents"""
    name: str
    _type: Type

    def __init__(self, name: str, ftype: Type = BoolType("bool")):

        if not isinstance(name, str):
            raise Exception("The fluent name must be a string")

        if not isinstance(ftype, Type):
            raise Exception("""The fluent type must be \
                                an instance of fType.Type""")

        object.__setattr__(self, "name", name)
        object.__setattr__(self, "_type", ftype)

    @property
    def type(self):
        """Returns the ftype.Type of the Fluent"""
        return self._type

    def __eq__(self, other):
        return self.name == other.name and self.type == other.type

    def __repr__(self):
        return f"fluent {self.name} of type {self.type}"

    def __neg__(self):
        literal = Literal(fluent=self, args=[])
        return -literal

    @staticmethod
    def _check_type(arg, _type: Type, pos: int) -> bool:
        """check if the argument at {pos}
           position of self is complient with _type"""
        str_error = f"""Fluent has type {_type} at position {pos},\
        but an argument: \"{arg}\" was given"""
        if _type.is_int_type():

            if isinstance(arg, int) and _type.min <= arg <= _type.max:
                return True
            if isinstance(arg, ArithmeticExpr):
                return True
            if arg.type.contained_in(_type):
                return True
            raise Exception(str_error)
        if _type.is_enum_type():

            if isinstance(arg, str) and arg in _type.enum_values or \
               arg.type.is_enum_type():
                return True
            raise Exception(str_error)

        if _type.is_bool_type():

            if isinstance(arg, bool) or arg.type.is_bool_type():
                return True
            raise Exception(str_error)
        raise Exception(str_error)

    def __call__(self, *args):

        if len(self.type) != len(args):
            raise Exception(f"""Fluent {self.name} has {len(self.type)} arguments,
                            but {len(args)} were given""")

        if len(self.type) == 1:

            self._check_type(args[0], self.type, 0)
            return Literal(self, args)

        c: int = 0

        for arg, t in zip(args, self.type):

            self._check_type(arg, t, c)
            c += 1

        return Literal(self, list(args))
