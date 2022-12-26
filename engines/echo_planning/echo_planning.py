"""Module to solve an EpiCla problem"""
from typing import Tuple, Union, List, Iterator, Dict
import sys
import os
import string
import random
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, os.path.join(CURRENT_DIR, '..', '..', 'model'))
import shortcuts as pd
sys.path.insert(1, os.path.join(CURRENT_DIR, '..', 'mae_epddl_planning'))
import epddl_engine
sys.path.insert(1, os.path.join(CURRENT_DIR, '..', 'answer_set_planning'))
import asp_engine
import copy


from predicate import Literal
from variable import Variable
from goal import Poset
from action import Instantiated_Action
from problem import EpiCla, HierarchicalGoalNetworkProblem

def extract_classical_effects(effects: List[Literal], var_val: Dict[Variable, str]) -> List[Literal]:

    effects = copy.deepcopy(effects)

    for idx, effect in enumerate(effects):
        effects[idx] = effect.instatiate(var_val)

    return effects


def extract_classical_poset(poset: Poset, var_val: Dict[Variable, str]) -> List[Literal]:

    return poset.instatiate(var_val)


def solve_echo(echo: ECHO) -> Iterator[Union[
        Instantiated_Action,
        Tuple[Instantiated_Action, List[Instantiated_Action]]
]]:

    meap_problem = echo.meap_problem
    classical_problem = echo.classical_problem

    echo_plan = []
    epistemic_plan = epddl_engine.solve_mae(meap_problem)

    for epistemic_action, instatiated_variables in epistemic_plan:

        if epistemic_action.type is pd.MEActionType.ontic:

            var_val = dict(zip(epistemic_action.params, instatiated_variables))
            if isinstance(classical_problem, HierarchicalGoalNetworkProblem):
                poset = extract_classical_poset(epistemic_action.sub_goals, var_val)
                classical_problem.add_poset(poset)

            else:
                effects = extract_classical_effects(epistemic_action.effects, var_val)
                classical_problem.add_goals(*effects)

            final_state, plan = asp_engine.solve_classical(classical_problem)

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
