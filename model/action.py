"""This modul contains Action datatypes"""

from typing import List, Union
from dataclasses import dataclass
from enum import Enum
from collections import namedtuple

from predicate import Literal, Predicate, BeliefLiteral
from variable import Variable

#  TODO: introduction of templates
#      needs of a fluent definition wich can be or
#      boolean or of a particular type
#      you should also be able to define new types
#  TODO: definition of a fixed set of actions that
#      have a direct encoding into moveit


@dataclass(frozen=True)
class IAction():
    """IAction class introduced to represent classical planning actions"""
    name: str
    params: List[Variable]
    precondition: List[Predicate]
    effects: List[Literal]

    def __init__(self, name, params, precondition, effects):

        for param in params:
            assert isinstance(param, Variable)
        for precond in precondition:
            assert isinstance(precond, Predicate)
        for effect in effects:
            assert isinstance(effect, Literal)

        object.__setattr__(self, "name", name)
        object.__setattr__(self, "params", params)
        object.__setattr__(self, "precondition", precondition)
        object.__setattr__(self, "effects", effects)


InstantiatedIAction = namedtuple('Instantiated_I_Action',
                                 ['action', 'var_map'])


class MEActionType(Enum):
    """Type of Multi-Agent Epistemic Actions"""
    Ontic = 'ontic'
    Sensing = 'sensing'
    Announcement = 'announcement'


@dataclass(frozen=True)
class MEAction():
    """MEAction class introduced to represent Mulit-Agent Epistemic Actions"""
    name: str
    type: MEActionType
    params: List[Variable]
    preconditions: List[Union[Literal, BeliefLiteral]]
    effects: List[Literal]
    full_observers: List[str]
    partial_observers: List[str]
