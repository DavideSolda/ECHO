from typing import Tuple, List, Dict, Union
import clingo

from asp_compiler import compile_into_asp

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
    ctl = clingo.Control(["-c", "l=10"])
    ctl.add("base", [], asp_encoding)

    ctl.ground([("base", [])], context=Context())
    ctl.solve(on_model=on_model)

    models = []
    with ctl.solve(yield_=True) as handle:
        for model in handle:
            models.append(model.symbols(atoms=True))
            break
    sorted(models)
    fluents = models[0]
    final_holds = []
    plan = []

    for fluent in fluents:
        if fluent.name == 'finally':
            if fluent.arguments[0].name != 'neg' and fluent.positive:
                final_holds.append(str(fluent.arguments[0]))
        elif fluent.name == 'occurs' and fluent.positive:
            action = action_2_instantiated_action(problem, fluent.arguments[0])
            index = int(str(fluent.arguments[1]))
            plan.append((action, index))
    plan = [x[0] for x in sorted(plan, key=lambda x : x[1])]
    return final_holds, plan
