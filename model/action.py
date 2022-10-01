"""This modul contains Action datatypes"""

from typing import List, Union
from dataclasses import dataclass
from enum import Enum
from collections import namedtuple

from predicate import Literal, Predicate, BeliefLiteral, \
    ObservablePredicate
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


@dataclass(frozen=True)
class MEActionType(Enum):
    """Type of Multi-Agent Epistemic Actions"""
    ontic = 'ontic'
    sensing = 'sensing'
    announcement = 'announcement'


@dataclass(frozen=True)
class MEAction():
    """MEAction class introduced to represent Mulit-Agent Epistemic Actions"""
    name: str
    type: MEActionType
    params: List[Variable]
    preconditions: List[Union[Literal, BeliefLiteral]]
    effects: List[Literal]
    full_observers: List[Union[str, ObservablePredicate]]
    partial_observers: List[Union[str, ObservablePredicate]]

    def __init__(self, name, params, precond, effects,
                 full_obs=None, part_obs=None, _type=MEActionType.ontic):
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'type', _type)
        object.__setattr__(self, 'params', params)
        object.__setattr__(self, 'preconditions', precond)
        object.__setattr__(self, 'effects', effects)
        if full_obs is not None:
            assert all(map(self._observer_ok, full_obs))
        object.__setattr__(self, 'full_observers', full_obs)
        if part_obs is not None:
            assert all(map(self._observer_ok, part_obs))
        object.__setattr__(self, 'partial_observers', part_obs)

    @staticmethod
    def _observer_ok(observer: Union[str, Predicate]) -> bool:
        return isinstance(observer, (str, ObservablePredicate))

    def __repr__(self) -> str:
        return f'''action {self.name}({", ".join(map(str, self.params))}) 
        of type {self.type}
        preconditions: {self.preconditions}
        effects: {self.effects}
        full obersvers: {self.full_observers}
        partial obersvers: {self.partial_observers}'''
