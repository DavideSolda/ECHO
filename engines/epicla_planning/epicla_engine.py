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

    print(var_val)
    effects = copy.deepcopy(effects)
    print(effects)
    for idx, effect in enumerate(effects):
        effects[idx] = effect.instatiate(var_val)
        print(effects[idx])
    return effects


def extract_classical_poset(poset: Poset, params: List[Variable],
                            values: List[str]) -> List[Literal]:
    var_val = dict(zip(params, values))
    return poset.instatiate(var_val)


def solve(epicla: EpiCla) -> Iterator[Union[
        Instantiated_Action,
        Tuple[Instantiated_Action, List[Instantiated_Action]]
]]:

    meap_problem = epicla.meap_problem
    classical_problem = epicla.classical_problem

    epicla_plan = []
    epistemic_plan = epddl_engine.solve(meap_problem)

    for epistemic_action, instatiated_variables in epistemic_plan:

        if epistemic_action.type == pd.MEActionType.ontic:

            var_val = dict(zip(epistemic_action.params, instatiated_variables))
            if isinstance(classical_problem, HierarchicalGoalNetworkProblem):
                poset = extract_classical_poset(epistemic_action.effects, var_val)
                classical_problem.add_poset(poset)

            else:
                effects = extract_classical_effects(epistemic_action.effects, var_val)
                print(effects)
                classical_problem.add_goals(*effects)

            final_state, plan = asp_engine.solve(classical_problem)

            epicla_plan.append((epistemic_action, plan))

            if isinstance(classical_problem, HierarchicalGoalNetworkProblem):
                classical_problem.reset_poset()
            else:
                classical_problem.reset_goals()

            classical_problem.reset_initial_values()    

            classical_problem.add_initial_values(*final_state)

        else:
            epicla_plan.append(epistemic_action)

    return epicla_plan
