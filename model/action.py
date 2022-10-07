"""This modul contains Action datatypes"""

from typing import List, Union
from dataclasses import dataclass
from enum import Enum
from collections import namedtuple
from fluent import Fluent
from predicate import Literal, Predicate, BeliefLiteral, \
    ObservablePredicate
from variable import Variable

#  TODO: introduction of templates
#      needs of a fluent definition wich can be or
#      boolean or of a particular type
#      you should also be able to define new types
#  TODO: definition of a fixed set of actions that
#      have a direct encoding into moveit


def fluent_to_literal(fluent: Fluent) -> Literal:
    """from fluent to literal. Added for easy to use from a user perspective"""
    return Literal(fluent=fluent, args=[])


def correct_predicates(l: List[Union[Fluent, Predicate]]) -> List[Predicate]:
    """If there is any fluent, it is converted into a Literal"""
    already_predicates = [predicate for predicate in l
                          if isinstance(predicate, Predicate)]
    new_predicates = [fluent_to_literal(fluent) for fluent in l
                      if isinstance(fluent, Fluent)]
    return already_predicates + new_predicates


@dataclass(frozen=True)
class IAction():
    """IAction class introduced to represent classical planning actions"""
    name: str
    params: List[Variable]
    precondition: List[Predicate]
    effects: List[Literal]

    def __init__(self, name, params, precondition, effects):

        precond = correct_predicates(precondition)
        effects = correct_predicates(effects)

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
    preconditions: List[Union[Literal, BeliefLiteral]]
    effects: List[Literal]
    full_observers: List[Union[str, ObservablePredicate]]
    partial_observers: List[Union[str, ObservablePredicate]]
    params: List[Variable]

    def __init__(self, name, precond, effects,
                 full_obs=None, part_obs=None, _type=MEActionType.ontic):

        precond = correct_predicates(precond)
        effects = correct_predicates(effects)

        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'type', _type)
        object.__setattr__(self, 'preconditions', precond)
        object.__setattr__(self, 'effects', effects)
        if full_obs is not None:
            assert all(map(self._observer_ok, full_obs))
        else:
            full_obs = []
        object.__setattr__(self, 'full_observers', full_obs)
        if part_obs is not None:
            assert all(map(self._observer_ok, part_obs))
        else:
            part_obs = []
        object.__setattr__(self, 'partial_observers', part_obs)
        params = [var for pred in precond for var in pred.variables]
        params += [var for eff in effects for var in eff.variables]
        #  params += [var for obs in full_obs for var in obs.variables
        #           if isinstance(obs, Predicate)]
        #  params += [var for obs in part_obs for var in obs.variables
        #           if isinstance(obs, Predicate)]
        object.__setattr__(self, 'params', params)

    @staticmethod
    def _observer_ok(observer: Union[str, Predicate]) -> bool:
        return isinstance(observer, (str, ObservablePredicate, Variable))

    def __repr__(self) -> str:
        return f'''action {self.name}({", ".join(map(str, self.params))})
        of type {self.type}
        preconditions: {self.preconditions}
        effects: {self.effects}
        full obersvers: {self.full_observers}
        partial obersvers: {self.partial_observers}'''
