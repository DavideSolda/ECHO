from dataclasses import dataclass
from typing import List, Union

from interval import Interval
from ftype import Type, BoolType, IntType, EnumType, StructType
from fvalue import Variable, ArithmeticExpr

from literal import *

@dataclass(frozen=True)
class Fluent():

    name : str
    type : Type
    
    def __init__(self, name : str, ftype : Type = BoolType()):

        if(not isinstance(name, str)):
            raise Exception("The fluent name must be a string")
        
        if(not isinstance(ftype, Type)):
            raise Exception("The fluent type must be an instance of fType.Type")

        object.__setattr__(self, "name", name)
        object.__setattr__(self, "type", ftype)

    def __eq__(self, other):
        return self.name == other.name and self.type == other.type

    def __repr__(self):
        return f"fluent {self.name} of type {self.type}"

    @staticmethod
    def _check_type(arg, t : Type, pos : int):

        se = f"Fluent has type {t} at position {pos}, but an argument: \"{arg}\" was given"
        if t.is_int_type():

            try:
                if isinstance(arg, int) and t.min <= arg and t.max >= arg:
                    return
                if isinstance(arg, ArithmeticExpr):
                    return
                elif arg.type.contained_in(t):
                    return
                else:
                    raise Exception(se)
            except:
                raise Exception(se)

        if t.is_enum_type():

            try:
                if isinstance(arg, str) and arg in t.enum_values:
                    return
                elif arg.type.is_enum_type():
                    return
                else:
                    raise Exception(se)
            except:
                raise Exception(se)

        if t.is_bool_type():

            try:
                if isinstance(arg, bool):
                    return
                elif arg.type.is_bool_type():
                    return
                else:
                    raise Exception(se)
            except:
                raise Exception(se)

    def __call__(self, *args):

        
        if len(self.type) != len(args):
            raise Exception(f"Fluent {self.name} has {len(self.type)} arguments, but {len(args)} were given")

        if len(self.type) == 1:

            self._check_type(args[0], self.type, 0)
            return FLiteral(self, args)

        c : int = 0

        for arg, t in zip(args, self.type):

            self._check_type(arg, t, c)
            c += 1

        return FLiteral(self, list(args))


    
def main():

    pos_type = IntType(1,4)
    num = Fluent("position", pos_type)
    print(num)
    on_type = StructType([EnumType(["red", "blue", "yellow"]), EnumType(["Table", "Chair"])])
    on = Fluent("on", on_type)
    print(on)
    status = Fluent("ready")
    print(status)
    color = Fluent("color", EnumType(["red", "blue", "yellow"]))
    print(color)
    x = Variable("x", IntType(1, 2))
    print(x)

    num(1)
    num(x)
    status(True)
    #status("a")

    print(num(x))
    print(-num(x))

    

if __name__ == "__main__":
    main()
