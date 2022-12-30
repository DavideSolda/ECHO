"""Module to solve an EpiCla problem"""
from typing import Tuple, Union, List, Iterator, Dict
import sys
import os
import string
import random
import copy

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

print(CURRENT_DIR)

#import solvers:
sys.path.insert(1, os.path.join(CURRENT_DIR, '..'))
from mae_epddl_planning import solve_mae
sys.path.insert(1, os.path.join(CURRENT_DIR, '..'))
from answer_set_planning import solve_classical

#import modeling objects:
sys.path.insert(1, os.path.join(CURRENT_DIR, '..', '..'))
from model import *


def extract_classical_effects(effects: List[Literal], var_val: Dict[Variable, str]) -> List[Literal]:

    effects = copy.deepcopy(effects)

    for idx, effect in enumerate(effects):
        effects[idx] = effect.instatiate(var_val)

    return effects


def extract_classical_poset(poset: Poset, var_val: Dict[Variable, str]) -> List[Literal]:

    return poset.instatiate(var_val)


def solve_echo(echo: ECHOPlanningProblem) -> Iterator[Union[
        Instantiated_Action,
        Tuple[Instantiated_Action, List[Instantiated_Action]]
]]:

    meap_problem = echo.meap_problem
    classical_problem = echo.classical_problem

    echo_plan = []
    epistemic_plan = solve_mae(meap_problem)

    for epistemic_action, instatiated_variables in epistemic_plan:

        if epistemic_action.type is MEActionType.ontic:

            var_val = dict(zip(epistemic_action.params, instatiated_variables))
            if isinstance(classical_problem, HierarchicalGoalNetworkProblem):
                poset = extract_classical_poset(epistemic_action.sub_goals, var_val)
                classical_problem.add_poset(poset)

            else:
                effects = extract_classical_effects(epistemic_action.effects, var_val)
                classical_problem.add_goals(*effects)

            final_state, plan = solve_classical(classical_problem)

            echo_plan.append(epistemic_action)
            #epicla_plan += plan

            if isinstance(classical_problem, HierarchicalGoalNetworkProblem):
                classical_problem.reset_poset()
            else:
                classical_problem.reset_goals()

            classical_problem.reset_initial_values()    

            classical_problem.add_initial_values(*final_state)

        else:
            echo_plan.append(epistemic_action)

    return echo_plan
