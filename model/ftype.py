from typing import List, Union
from dataclasses import dataclass
from random import randint

from typing import Tuple
from interval import Interval

@dataclass(frozen=True)
class Type:
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

@dataclass(frozen=True)
class BoolType(Type):

    def __init__(self):
        super().__init__()
        
    def is_bool_type(self) -> bool:
        return True
    def __repr__(self) -> str:
        return "bool"

@dataclass(frozen=True)
class IntType(Type):

    _max : int
    _min : int
    def __init__(self, _min : int, _max : int):

        super().__init__()

        if (_max < _min):
            raise Exception(f"max : {_max} > min : {_min}")

        if isinstance(_min, int) and isinstance(_max, int):

            object.__setattr__(self, "_max", _max)
            object.__setattr__(self, "_min", _min)
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
        return f"int : [{self.min}, {self.max}]"

    def is_int_type(self) -> bool:
        return True

    def contained_in(self, other : "IntType") -> bool:
        return self.min >= other.min and self.max <=other.max

    @property
    def interval(self) -> Tuple[int]:
        return (self.min, self.max)
    
@dataclass(frozen=True)
class EnumType(Type):

    def __init__(self, domain : List[str]):

        super().__init__()

        try:
            for enum_val in domain:
                if(not isinstance(enum_val, str)):
                    raise Exception(f"{enum_val} is not a string")
        except:
            raise Exception(f"{domain} is not a list of strings")
                
        object.__setattr__(self, "domain", domain)

    def __repr__(self) -> str:
        return f"enum : {self.domain}"

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

    def __init__(self, types : List[Type]):

        super().__init__()

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

        return f"struct : {self.domain}"
        
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
    
    i1 = IntType(Interval(2,3))
    print(i1)
    i2 = IntType(Interval(2,3))
    print(i2)
    st = StructType([i1, i2])
    print(st)
    i3 = IntType(Interval(2,5))
    print()
    #i2 = IntType()

if __name__ == "__main__":
    main()
