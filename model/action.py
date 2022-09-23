from typing import List
from dataclasses import dataclass
from fluent import *
from literal import *
from fvalue import *
from ftype import *

#TODO: introduction of templates
#      needs of a fluent definition wich can be or boolean or of a particular type
#      you should also be able to define new types
#TODO: definition of a fixed set of actions that have a direct encoding into moveit

@dataclass(frozen=True)
class I_Action():
    name: str
    params: List[Variable]
    precondition: List[Literal]
    effects: List[FLiteral]

    def __init__(self, name, params, precondition, effects):

        for param in params:
            assert isinstance(param, Variable)
        for precond in precondition:
            assert isinstance(precond, Literal)
        for effect in effects:
            assert isinstance(effect, FLiteral)

        object.__setattr__(self, "name", name)
        object.__setattr__(self, "params", params)
        object.__setattr__(self, "precondition", precondition)
        object.__setattr__(self, "effects", effects)

from collections import namedtuple

Instantiated_I_Action = namedtuple('Instantiated_I_Action', ['action', 'variable_mapping'])
