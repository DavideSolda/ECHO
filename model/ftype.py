"""
module for the definiton of Types of parameters in the planning problem
***This way to proceed means that we :require :typing
"""
from typing import List, Tuple
from dataclasses import dataclass
from abc import abstractmethod


@dataclass(frozen=True)
class Type:
    """Definition of the Type class"""
    name: str

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

    def is_agent_type(self) -> bool:
        """we reserve a particular type for agents"""
        return False

    def __eq__(self, _type):
        return self is _type or \
            _type.is_bool_type() and self.is_bool_type()

    def __len__(self):
        return 1

    @abstractmethod
    def __hash__(self) -> int:
        pass


@dataclass(frozen=True)
class BoolType(Type):
    """Definition of boolean type"""
    def is_bool_type(self) -> bool:
        return True

    def __repr__(self) -> str:
        return f"{self.name} bool"

    def __hash__(self) -> int:
        return 100

    def __len__(self):
        return 0

@dataclass(frozen=True)
class IntType(Type):
    """Definition of integer type"""
    name: str
    min_val: int
    max_val: int

    def __post_init__(self):

        if self.max < self.min:
            raise Exception(f"max : {self.max} > min : {self.min}")

        if not isinstance(self.min, int) or not isinstance(self.max, int):
            raise Exception(f"integer type ill-defined: IntType({self.min}, {self.max})")

    @property
    def min(self) -> int:
        """Returns the minimum range value"""
        return self.min_val

    @property
    def max(self) -> int:
        """Returns the maximum range value"""
        return self.max_val

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

    def __hash__(self) -> int:
        h_name = hash(self.name)
        return 31**self.min**self.max+h_name % 256


@dataclass(frozen=True)
class EnumType(Type):
    """Definition of enumerate type"""
    name: str
    domain: List[str]

    def __post_init__(self):

        if not isinstance(self.domain, list):
            raise Exception(f"{domain} is not a list of strings")
        for enum_val in self.domain:
            if not isinstance(enum_val, str):
                raise Exception(f"{enum_val} is not a string")

    def __repr__(self) -> str:
        return f"{self.name} : {self.domain}"

    def is_enum_type(self) -> bool:
        return True

    def __iter__(self):
        for val in self.domain:
            yield val

    def contained_in(self, other: "EnumType") -> bool:
        """Returns if the domain is contained"""
        for s in self.domain:
            if s not in other.domain:
                return False
        return True

    @property
    def enum_values(self) -> List[str]:
        """Return the domain"""
        return self.domain

    def __hash__(self) -> int:
        return 1
        h = 1
        prime = 31
        for val in self.domain[1:]:
            h = prime*h+hash(val)
        return hash(self.name) % 256 + h


@dataclass(frozen=True)
class AgentType(EnumType):
    """A type suited for agents"""
    name: str
    domain: List[str]

    def __init__(self, domain):
        super().__init__('agent', domain)

    def __post_init__(self):
        super().__post_init__()

    def is_agent_type(self):
        return True

    def __repr__(self):
        return super().__repr__()


@dataclass(frozen=True)
class StructType(Type):
    """Definition of struct type"""
    name: str
    subtypes: List[Type]

    def __post_init__(self):

        if not isinstance(self.subtypes, list):
            raise Exception(f"""{self.subtypes} is not a list of plan ftype.Type
 {{ftype.EnumType, ftype.BoolType, ftype.IntType}}""")

        for sub_type in self.subtypes:
            if not isinstance(sub_type, Type):
                raise Exception(f"{sub_type} is not an instance of ftype.Type")
            if isinstance(sub_type, StructType):
                raise Exception(f"nested StructType are not supported")
            if isinstance(sub_type, BoolType):
                raise Exception(f"""ftype.BoolType cannot be a field in a
fType.StructType""")

    def __repr__(self):
        return f"{self.name} : {self.subtypes}"

    def is_struct_type(self) -> bool:
        return True

    def __iter__(self):
        for subtype in self.subtypes:
            yield subtype

    def __len__(self):
        return len(self.subtypes)

    def __hash__(self) -> int:#TODO
        h = 1
        return h
