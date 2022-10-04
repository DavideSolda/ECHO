from typing import List, Union
from compiler_to_epddl import compile_into_epddl
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.insert(1, os.path.join(current_dir, '..', 'model'))
import shortcuts as pd


def solve(problem: pd.MEPlanningProblem) -> List[str]:

    epddl_encoding = compile_into_epddl(problem)
    print('>'*30)
    print(epddl_encoding)

    return []
