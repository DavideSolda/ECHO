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

        precond = precond
        effects = effects

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
    classical_effects: List[Literal]
    pure_epddl: bool

    def __init__(self, name, precond, effects,
                 full_obs=None, part_obs=None, _type=MEActionType.ontic):

        precond = precond
        effects = effects

        object.__setattr__(self, 'pure_epddl', True)
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

    def insert(self, classical_fluents:List[Literal]):
        object.__setattr__(self, 'classical_effects', classical_fluents)
        object.__setattr__(self, 'pure_epddl', False)
