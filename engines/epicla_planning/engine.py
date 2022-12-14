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

def solve(epicla: pd.EpiCla) -> Iterator[Union[pd.IstantiatedMEAction, pd.InstantiatedIAction]]:

    epicla_plan = []
    epistemic_plan = epddl_engine.solve(meap_problem)
    for epistemic_action in epistemic_plan:
        if epistemic_action.type == pd.MEActionType.ontic:
            pass
        else:
            epicla_plan.append(epistemic_action)

    return epicla_plan
