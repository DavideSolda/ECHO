"""module for the definiton of Types of parameters in the planning problem"""
from typing import List, Tuple
from dataclasses import dataclass


@dataclass(frozen=True)
class Type:
    """Definition of the Type class"""
    _name: str

    def __init__(self, name : str):
        object.__setattr__(self, "_name", name)

    def is_bool_type(self) -> bool:
        """is boolean?"""
        return False

    def is_enum_type(self) -> bool:
        """is enum?"""
        return False

    def is_int_type(self) -> bool:
        """is int?"""
        return False

    def is_struct_type(self) -> bool:
        """is struct ?"""
        return False

    def __eq__(self, _type):
        return self is _type or \
            _type.is_bool_type() and self.is_bool_type()

    def __len__(self):
        return 1

    @property
    def name(self) -> str:
        """Get name of the type"""
        return self._name


@dataclass(frozen=True)
class BoolType(Type):
    """Definition of boolean type"""
    def is_bool_type(self) -> bool:
        return True

    def __repr__(self) -> str:
        return f"{self.name} bool"


@dataclass(frozen=True)
class IntType(Type):
    """Definition of integer type"""
    _max: int
    _min: int
    _name: str

    def __init__(self, name: str, _min: int, _max: int):

        super().__init__(name)

        if _max < _min:
            raise Exception(f"max : {_max} > min : {_min}")

        if isinstance(_min, int) and isinstance(_max, int):

            object.__setattr__(self, "_max", _max)
            object.__setattr__(self, "_min", _min)
            object.__setattr__(self, "_name", name)
            return
        raise Exception(f"integer type ill-defined: IntType({_min}, {_max})")

    @property
    def min(self) -> int:
        """Returns the minimum range value"""
        return self._min

    @property
    def max(self) -> int:
        """Returns the maximum range value"""
        return self._max

    def __contains__(self, i: int):
        return self.min <= i <= self.max

    def __repr__(self) -> str:
        return f"{self.name} : [{self.min}, {self.max}]"

    def is_int_type(self) -> bool:
        return True

    def contained_in(self, other: "IntType") -> bool:
        """Returns if the range is contained"""
        return self.min >= other.min and self.max <= other.max

    @property
    def interval(self) -> Tuple[int]:
        """Returns the interval"""
        return (self.min, self.max)


@dataclass(frozen=True)
class EnumType(Type):
    """Definition of enumerate type"""
    domain: List[str]
    def __init__(self, name: str, domain: List[str]):

        super().__init__(name)

        if not isinstance(domain, list):
            raise Exception(f"{domain} is not a list of strings")
        for enum_val in domain:
            if not isinstance(enum_val, str):
                raise Exception(f"{enum_val} is not a string")

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
        """Return the domain"""
        return self.domain


@dataclass(frozen=True)
class StructType(Type):
    """Definition of struct type"""
    domain: List[Type]
    def __init__(self, name: str, types: List[Type]):

        super().__init__(name)

        if not isinstance(types, list):
            raise Exception(f"""{types} is not a list of plan ftype.Type
 {{ftype.EnumType, ftype.BoolType, ftype.IntType}}""")

        for sub_type in types:
            if not isinstance(sub_type, Type):
                raise Exception(f"{sub_type} is not an instance of ftype.Type")
            if isinstance(sub_type, StructType):
                raise Exception(f"nested StructType are not supported")
            if isinstance(sub_type, BoolType):
                raise Exception(f"""ftype.BoolType cannot be a field in a
fType.StructType""")

        object.__setattr__(self, "domain", types)

    def __repr__(self):
        return f"{self.name} : {self.domain}"

    def is_struct_type(self) -> bool:
        return True

    def __iter__(self):
        for sub_type in self.domain:
            yield sub_type

    def __len__(self):
        return len(self.domain)
