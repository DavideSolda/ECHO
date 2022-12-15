from typing import List, Union, Tuple
from action import IAction, Instantiated_Action, \
    MEAction, MEActionType
from fluent import Fluent
from variable import Variable
from arithmetic_expression import ArithmeticExpr
from problem import ClassicalPlanningProblem, MEPlanningProblem, HierarchicalGoalNetworkProblem, EpiCla
from ftype import Type, BoolType, IntType, EnumType, StructType, AgentType
from predicate import Predicate, Literal, EqualityPredicate,\
    BeliefPredicate, Forall, eq, neq, B,\
    BooleanPredicate, BooleanOperator, EqualityOperator, When, Forall
from method import Method
from goal import Goal, Poset


def pretty_print_epica_plan(epicla_plan: List[Union[Instantiated_Action,
                                                    Tuple[Instantiated_Action,
                                                          List[Instantiated_Action]]]]) -> None:
    for action in epicla_plan:
        if isinstance(action, Instantiated_Action):
            print(action)
        else:
            for sub_action in action[1]:
                print(sub_action)

