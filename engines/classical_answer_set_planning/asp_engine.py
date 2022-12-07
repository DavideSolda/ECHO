from typing import Tuple, List, Dict, Union
import clingo
from clingo.application import clingo_main, Application, ApplicationOptions

from asp_compiler import compile_into_asp
from asp_iclingo_like import IncApp

import os
current_dir = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.insert(1, os.path.join(current_dir, '..', '..', 'model'))
from shortcuts import *


def action_2_instantiated_action(problem: ClassicalPlanningProblem, symbol_action: clingo.Symbol)-> InstantiatedIAction:

    action = next(act for act in problem.actions if act.name == symbol_action.name)
    symbol_parameters = symbol_action.arguments
    assert len(action.params) == len(symbol_parameters)
    var_val = {}
    for var, value in zip(action.params, symbol_parameters):
        var_val[var] = int(str(value)) if var.type.is_int_type() else str(value)
    return InstantiatedIAction(action, var_val)


class Context:
    pass

def on_model(m):
    return m

def solve(problem: ClassicalPlanningProblem) -> Tuple[List[Predicate], List[InstantiatedIAction]]:

    asp_encoding = compile_into_asp(problem)

    encoding_file_path = os.path.join(current_dir, 'asp_encoding.lp')
    print(asp_encoding)
    print(encoding_file_path)

    
    with open(encoding_file_path, 'w') as encoding_file:
        encoding_file.write(asp_encoding)

    inc_app = IncApp()
    clingo_main(inc_app, [encoding_file_path])

    model = inc_app.get_model()

    print('look at here')
    print(model)
    final_holds = []
    plan = []

    #get maximum timestamp
    max_timestamp = 1
    for fluent in model:
        print(fluent)
        if fluent.name == 'holds':
            max_timestamp = max(max_timestamp, fluent.arguments[1].number)
    print(f'maximum timestamp {max_timestamp}')
    for fluent in model:
        if fluent.name == 'holds' and fluent.arguments[1].number == max_timestamp:
            if fluent.arguments[0].name != 'neg' and fluent.positive:
                final_holds.append(str(fluent.arguments[0]))
        elif fluent.name == 'occurs' and fluent.positive:
            action = action_2_instantiated_action(problem, fluent.arguments[0])
            index = int(str(fluent.arguments[1]))
            plan.append((action, index))
    
    plan = [x[0] for x in sorted(plan, key=lambda x : x[1])]
    return final_holds, plan
