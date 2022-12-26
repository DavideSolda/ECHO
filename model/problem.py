"""class for the definition of a planning problem"""
import sys, os
from typing import List, Union, Any, Iterator
from dataclasses import dataclass
import logging
from abc import abstractmethod
from enum import Enum

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, current_dir)

from .action import IAction, MEAction
from .fluent import Fluent
from .predicate import Literal, Predicate, Predicate
from .variable import Variable
from .ftype import Type
from .method import Method
from .goal import Goal, Poset

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
        self._name = 'no_name'

    @property
    def name(self) -> str:
        """domain name"""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

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
            if isinstance(arg, Fluent):
                self._inits.append(Literal(fluent=arg, args=[]))
                continue
            self._inits.append(arg)

    def reset_initial_values(self):
        """Remove initial literals"""
        self._inits = []
            
    def add_goals(self, *args):
        """Add final literal to the problem"""
        for arg in args:
            self._goals.append(arg)

    def reset_goals(self):
        """Remove final literals"""
        self._goals = []

    @staticmethod
    def _stringy(objs: List[Any]) -> List[str]:
        return map(lambda obj: str(obj), objs)

    def __repr__(self):

        sep = "\n\n-----------------------\n\n"
        prob_repr = "Problem domain:"
        prob_repr += sep
        prob_repr += "Types\n"
        prob_repr += "\n".join(self._stringy(self._types))
        prob_repr += sep
        prob_repr += "Variables\n"
        prob_repr += "\n".join(self._stringy(self._variables))
        prob_repr += sep
        prob_repr += "Fluents\n"
        prob_repr += "\n".join(self._stringy(self._fluents))
        prob_repr += sep
        prob_repr += "Actions\n"
        prob_repr += "\n".join(self._stringy(self.actions))
        prob_repr += sep + sep
        prob_repr += "Problem instance:"
        prob_repr += sep
        prob_repr += "Initial values\n"
        prob_repr += "\n".join(self._stringy(self._inits))
        prob_repr += sep
        prob_repr += "Goals\n"
        prob_repr += "\n".join(self._stringy(self._goals))
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
        #TODO ADD CHECK ON THE FLUENTS: IF THEY ARE ADDED TO THE PROBLEM
        for pre in action.precondition:
            for sub_type in pre.types:
                if sub_type not in self._types and not sub_type.is_bool_type():
                    raise Exception(f"""{sub_type} not added,
                    from {pre} in preconditions""")

        for eff in action.effects:
            for sub_type in eff.types:
                if sub_type not in self._types and not sub_type.is_bool_type():
                    raise Exception(f"""{sub_type} not added,
                    from {eff} in effects""")

        self._domain.append(action)


@dataclass
class HierarchicalGoalNetworkProblem(ClassicalPlanningProblem):
    """definition of a classical planning problem"""

    _domain: List[IAction]
    _methods: List[Method]
    _goals: List[Goal]
    _poset: Poset

    def __init__(self):
        super().__init__()
        self._domain = []
        self._methods = []

    @property
    def methods(self) -> List[Method]:
        """Returns list of actions involved in the problem"""
        return self._methods

    def add_method(self, method: Method):
        """Add action to the problem"""
        #TODO ADD CHECK ON THE FLUENTS: IF THEY ARE ADDED TO THE PROBLEM
        for pre in method.precondition:
            for sub_type in pre.types:
                if sub_type not in self._types and not sub_type.is_bool_type():
                    raise Exception(f"""{sub_type} not added,
                    from {pre} in preconditions""")

        for goal in method.goal_poset.get_goals():
            for literal in goal.literals:
                for sub_type in literal.types:
                    if sub_type not in self._types and not sub_type.is_bool_type():
                        raise Exception(f"""{sub_type} not added,
                        from {eff} in effects""")

        self._methods.append(method)

    def add_poset(self, poset: Poset):
        """Add a poset to satisfy"""
        self._poset = poset

    def add_goal(self, goal: Goal):
        """Add subgoals of the domain"""
        self._goals.append(goal)

    @property
    def initial_poset(self) -> Poset:
        """Add initial poset to the domain"""
        return self._poset

    def reset_poset(self) -> None:
        """Remove initial poset to the domain"""
        self._poset = None

    @property
    def goals(self) -> List[Goal]:
        return self._goals
        
@dataclass(repr=False)
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
                if sub_type not in self._types and not sub_type.is_bool_type():
                    raise Exception(f"""{sub_type} not added,
                    from {pre} in preconditions""")

        for eff in action.effects:
            for sub_type in eff.types:
                if sub_type not in self._types and not sub_type.is_bool_type():
                    raise Exception(f"""{sub_type} not added,
                    from {eff} in effects""")

        self._domain.append(action)

@dataclass(repr=False)
class ECHOPlanningProblem():

    classical_problem: ClassicalPlanningProblem
    meap_problem: MEPlanningProblem
