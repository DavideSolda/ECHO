"""This modul contains Action datatypes"""
import os, sys
from typing import List, Union, TypeVar
from dataclasses import dataclass
from enum import Enum
from collections import namedtuple

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, current_dir)

from .fluent import Fluent
from .predicate import Literal, Predicate, BeliefPredicate, Forall
from .variable import Variable
from .goal import Poset

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

    def __post_init__(self):

        for param in self.params:
            assert isinstance(param, Variable)
        for precond in self.precondition:
            assert isinstance(precond, Predicate)
        for effect in self.effects:
            assert isinstance(effect, Literal)

    def __repr__(self):
        return self.name + '(' + str(self.params) + ')'


@dataclass(frozen=True)
class MEActionType(Enum):
    """Type of Multi-Agent Epistemic Actions"""
    ontic = 'ontic'
    sensing = 'sensing'
    announcement = 'announcement'


@dataclass#(frozen=True)
class MEAction():
    """MEAction class introduced to represent Mulit-Agent Epistemic Actions"""
    
    name: str
    params: List[Variable]
    type: MEActionType
    precondition: List[Predicate]
    effects: List[Predicate]
    full_obs: List[Union[str, Variable, Forall]]
    partial_obs: List[Union[str, Variable, Forall]]

    def __init__(self, name, params = [], type = MEActionType.ontic,
                 precondition = [], effects = [], full_obs = [], partial_obs = []):
        self.name = name
        self.params = params
        self.type = type
        self.precondition = precondition
        self.effects = effects
        self.full_obs = full_obs
        self.partial_obs = partial_obs
    
    def __post_init__(self):

        for param in self.params:
            assert isinstance(param, Variable)
        for precond in self.precondition:
            assert isinstance(precond, Predicate)
        for effect in self.effects:
            assert isinstance(effect, Predicate)
        for obs in self.full_obs + self.partial_obs:
            assert isinstance(obs, (str, Variable, Forall))

    def classical_sub_goals(self, sub_goal: Union[Poset, List[Literal]]):
        #only ontic actions can be refined:
        assert self.type == MEActionType.ontic
        self._sub_goal = sub_goal

    @property
    def sub_goals(self) -> Union[Poset, List[Literal]]:
        return self._sub_goal

Instantiated_Action = namedtuple('Instantiated_Action',
                                 ['action', 'var_map'])
