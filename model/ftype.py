from typing import List, Union
from dataclasses import dataclass
from random import randint

from typing import Tuple

@dataclass(frozen=True)
class Type:

    _name : str
    def __init__(self, name : str):
        object.__setattr__(self, "_name", name)
    def is_bool_type(self) -> bool:
        return False    
    def is_enum_type(self) -> bool:
        return False
    def is_int_type(self) -> bool:
        return False
    def is_struct_type(self) -> bool:
        return False
    def __eq__(self, _type):
        return self is _type
    def __len__(self):
        return 1
    @property
    def name(self) -> str:
        return self._name

@dataclass(frozen=True)
class BoolType(Type):


    def __init__(self, name : str):
        super().__init__(name)
        
    def is_bool_type(self) -> bool:
        return True
    def __repr__(self) -> str:
        return f"{self.name} bool"

@dataclass(frozen=True)
class IntType(Type):
    
    _max : int
    _min : int
    _name : str

    def __init__(self, name : str, _min : int, _max : int):


        super().__init__(name)

        if (_max < _min):
            raise Exception(f"max : {_max} > min : {_min}")

        if isinstance(_min, int) and isinstance(_max, int):

            object.__setattr__(self, "_max", _max)
            object.__setattr__(self, "_min", _min)
            object.__setattr__(self, "_name", name)
            return
        else:

            raise Exception(f"integer type ill-defined: IntType({_min}, {_max})")

    @property
    def min(self) -> int:
        return self._min

    @property
    def max(self) -> int:
        return self._max

    def __contains__(self, i : int):
        return i >= self.min and i <= self.max
    
    def __repr__(self) -> str:
        return f"{self.name} : [{self.min}, {self.max}]"

    def is_int_type(self) -> bool:
        return True

    def contained_in(self, other : "IntType") -> bool:
        return self.min >= other.min and self.max <=other.max

    @property
    def interval(self) -> Tuple[int]:
        return (self.min, self.max)
    
@dataclass(frozen=True)
class EnumType(Type):

    def __init__(self, name : str, domain : List[str]):

        super().__init__(name)

        try:
            for enum_val in domain:
                if(not isinstance(enum_val, str)):
                    raise Exception(f"{enum_val} is not a string")
        except:
            raise Exception(f"{domain} is not a list of strings")
                
        object.__setattr__(self, "domain", domain)

    def __repr__(self) -> str:
        return f"{self.name} : {self.domain}"

    def is_enum_type(self) -> bool:
        return True

    def __iter__(self):
        for val in self.domain:
            yield val
    @property
    def enum_values(self) -> List[str]:
        return self.domain
    
@dataclass(frozen=True)
class StructType(Type):

    def __init__(self, name : str, types : List[Type]):

        super().__init__(name)

        try:

            for t in types:
                if not isinstance(t, Type):
                    raise Exception(f"{t} is not an instance of ftype.Type")
                elif isinstance(t, StructType):
                    raise Exception(f"nested StructType are not supported")
                elif isinstance(t, BoolType):
                    raise Exception(f"ftype.BoolType cannot be a field in a structType")
                
            object.__setattr__(self, "domain", types)
        except:
            raise Exception(f"{types} is not a list of plan ftype.Type {{ftype.EnumType, ftype.BoolType, ftype.IntType}}")

    def __repr__(self):

        return f"{self.name} : {self.domain}"
        
    def is_struct_type(self) -> bool:

        return True

    def __iter__(self):

        for t in self.domain:
            yield t

    def __len__(self):

        return len(self.domain)
    @property
    def filed_types(self) -> List[Type]:

        return self.domain

def main():

    b = BoolType("b")
    print(b)

    i1 = IntType("i1", 2, 3)
    print(i1)

    e = EnumType("colors", ["red", "white"])
    print(e)
    """
    print(i1.name())
    print(i1)
    """

if __name__ == "__main__":
    main()
