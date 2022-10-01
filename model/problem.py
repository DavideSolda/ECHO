"""class for the definition of a planning problem"""
from typing import List, Union
from dataclasses import dataclass
from enum import Enum
import logging
from abc import abstractmethod

from action import IAction, MEAction
from fluent import Fluent
from predicate import Literal, Predicate
from variable import Variable
from ftype import Type


class SolvingClassicalPlanningOption(Enum):  # TODO: to move?
    """Types of classical planning solving problems"""
    PARTIAL_ORDER_PLANNING = 1  # not yet implemented
    ANSWER_SET_PLANNING = 2


@dataclass
class PlanningProblem():
    """definition of a planning problem"""
    _inits: List[Predicate]
    _goals: List[Predicate]
    _types: List[Type]
    _variables: List[Variable]
    _fluents: List[Fluent]

    def __init__(self):
        self._inits: List[Literal] = []
        self._goals: List[Literal] = []
        self._types: List[Type] = []
        self._variables: List[Variable] = []
        self._fluents: List[Fluent] = []

    @property
    def types(self) -> List[Type]:
        """Returns list of problems types"""
        return self._types

    @property
    def fluents(self) -> List[Fluent]:
        """Returns list of problems fluents"""
        return self._fluents

    @property
    def goals(self) -> List[Predicate]:
        """Returns list of goals of the problem"""
        return self._goals

    @property
    def init_values(self) -> List[Literal]:
        """Returns list of initial values of the problem"""
        return self._inits

    @property
    @abstractmethod
    def actions(self) -> List[Union[IAction, MEAction]]:
        """Returns list of actions involved in the problem"""

    @abstractmethod
    def add_action(self, action: List[Union[IAction, MEAction]]):
        """Add action to the problem"""

    def add_type(self, _type: Type) -> None:
        """Add type to the problem"""
        for _t in self._types:
            if _type == _t:
                logging.info(f"{_type} already inserted")
            elif _t.name == _type.name:
                raise Exception(f"{_t} has name {_t.name} as {_type}")
        self._types.append(_type)

    def add_variable(self, variable: Variable) -> None:
        """Add variable to the problem"""
        if variable.type not in self._types:
            raise Exception(f"{variable.type} not added")
        self._variables.append(variable)

    def add_fluent(self, fluent: Fluent):
        """Add fluent to the problem"""
        if fluent.type not in self._types and not fluent.type.is_bool_type():
            raise Exception(f"{fluent.type} not added")
        self._fluents.append(fluent)

    def add_initial_values(self, *args):
        """Add initial literal to the problem"""
        for arg in args:
            if len(arg.variables) > 0:
                assert False
                #  TODO: add check on the types
            self._inits.append(arg)

    def add_goals(self, *args):
        """Add final literal to the problem"""
        for arg in args:
            self._goals.append(arg)

    def __repr__(self):

        sep = "\n\n-----------------------\n\n"
        prob_repr = "Problem domain:"
        prob_repr += sep
        prob_repr += "Types\n"
        prob_repr += "\n".join(map(lambda x: str(x), self._types))
        prob_repr += sep
        prob_repr += "Variables\n"
        prob_repr += "\n".join(self._variables)
        prob_repr += sep
        prob_repr += "Fluents\n"
        prob_repr += "\n".join(self._fluents)
        prob_repr += sep
        prob_repr += "Actions\n"
        prob_repr += "\n".join(self.actions)
        prob_repr += sep + sep
        prob_repr += "Problem instance:"
        prob_repr += sep
        prob_repr += "Initial values\n"
        prob_repr += "\n".join(self._inits)
        prob_repr += sep
        prob_repr += "Goals\n"
        prob_repr += "\n".join(self._goals)
        return prob_repr


@dataclass
class ClassicalPlanningProblem(PlanningProblem):
    """definition of a classical planning problem"""

    _domain: List[IAction]

    def __init__(self):
        super().__init__()
        self._domain = []

    @property
    def actions(self) -> List[IAction]:
        """Returns list of actions involved in the problem"""
        return self._domain

    def add_action(self, action: IAction):
        """Add action to the problem"""
        for pre in action.precondition:
            for sub_type in pre.types:
                if sub_type not in self._types:
                    raise Exception(f"""{sub_type} not added,
                    from {pre} in preconditions""")

        for eff in action.effects:
            for sub_type in eff.types:
                if sub_type not in self._types:
                    raise Exception(f"""{sub_type} not added,
                    from {eff} in effects""")

        self._domain.append(action)


@dataclass
class MEPlanningProblem(PlanningProblem):
    """definition of an epistemic multiagent planning problem"""
    _domain: List[MEAction]

    def __init__(self):
        super().__init__()
        self._domain = []

    @property
    def actions(self) -> List[MEAction]:
        """Returns list of actions involved in the problem"""
        return self._domain

    def add_action(self, action: MEAction):
        """Add action to the problem"""
        for pre in action.precondition:
            for sub_type in pre.types:
                if sub_type not in self._types:
                    raise Exception(f"""{sub_type} not added,
                    from {pre} in preconditions""")

        for eff in action.effects:
            for sub_type in eff.types:
                if sub_type not in self._types:
                    raise Exception(f"""{sub_type} not added,
                    from {eff} in effects""")

        self._domain.append(action)
