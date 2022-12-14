"""Module to solve an EpiCla problem"""
from typing import Tuple, Union, List, Iterator
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

def extract_classical_effects(effects: List[Literal], params: List[Variables],
                              values: List[str]) -> List[Literal]:

    effects = copy.deepcopy(effects)
    for effect in effects:
        for idx, arg in enumerate(effect.args):
            if isinstance(arg, Variable):
                parameter_index = params.index(arg)
                effect.args[parameter_index] = values[parameter_index]
    return effects


def extract_classical_poset(poset: Poset, params: List[Variables],
                            values: List[str]) -> List[Literal]:
    var_val = dict(zip(params, values))
    return poset.instatiate(var_val)


def solve(epicla: pd.EpiCla) -> Iterator[Union[pd.IstantiatedMEAction, pd.InstantiatedIAction]]:

    meap_problem = epicla.meap_problem
    classical_problem = epicla.classical_problem

    epicla_plan = []
    epistemic_plan = epddl_engine.solve(meap_problem)

    for epistemic_action, instatiated_variables in epistemic_plan:

        if epistemic_action.type == pd.MEActionType.ontic:

            if isinstance(classical_problem, HierarchicalGoalNetworkProblem):
                poset = extract_classical_poset(epistemic_action.effects,
                                                epistemic_action.params,
                                                instatiated_variables)
                classical_problem.add_poset(poset)

            else:
                effects = extract_classical_effects(epistemic_action.effects,
                                                    epistemic_action.params,
                                                    instatiated_variables)
                classical_problem.add_goals(effects)

            plan, final_state = asp_engine.solve(classical_problem)
            epicla_plan.append((epistemic_action, plan))

            if isinstance(classical_problem, HierarchicalGoalNetworkProblem):
                classical_problem.reset_poset()
            else:
                classical_problem.reset_initial_values()
            classical_problem.reset_initial_goals()

            for el in final_state:
                classical_problem.add_initial_values(*final_state)

        else:
            epicla_plan.append(epistemic_action)

    return epicla_plan
