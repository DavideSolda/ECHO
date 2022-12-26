from typing import Tuple, List, Dict, Union
import clingo
from clingo.application import clingo_main, Application, ApplicationOptions
import copy
import os
import sys

from .classical_asp_encoding import compile_classical_into_asp
from .asp_goal_network_encoding import compile_HGN_into_asp

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, os.path.join(current_dir, '..', '..'))

from model import *
                                                                                           
MAX_STEP = 30

class Context:
    def id(self, x):
        return x
    def seq(self, x, y):
        return [x, y]

def on_model(m):
    print(m)
    pass


def action_2_instantiated_action(problem: ClassicalPlanningProblem, symbol_action: clingo.Symbol)-> Instantiated_Action:

    action = next(act for act in problem.actions if act.name == symbol_action.name)
    action = copy.deepcopy(action)
    symbol_parameters = symbol_action.arguments
    assert len(action.params) == len(symbol_parameters)
    var_val = {}
    for var, value in zip(action.params, symbol_parameters):
        var_val[var] = int(str(value)) if var.type.is_int_type() else str(value)
    return Instantiated_Action(action, var_val)


def correct_argument(struct_type: Type, arguments: clingo.Symbol) -> Union[str, int]:

    params = []
    for sub_type, argument in zip(struct_type, arguments):
        if sub_type.is_int_type():
            params.append(argument.number)
        elif sub_type.is_enum_type():
            params.append(argument.name)
    return params

def to_problem_literal(fluents: List[Fluent], c_symbol: clingo.Symbol) -> Literal:

    fluent = next(iter([f for f in fluents if f.name == c_symbol.name]))
    if fluent.type.is_bool_type():
        return fluent()
    elif fluent.type.is_int_type():
        return fluent(c_symbol.arguments[0].number)
    elif fluent.type.is_enum_type():
        return fluent(c_symbol.arguments[0].name)
    elif fluent.type.is_struct_type():
        return fluent(*correct_argument(fluent.type, c_symbol.arguments))
    assert False


def solve_classical(problem: Union[ClassicalPlanningProblem, HierarchicalGoalNetworkProblem]) -> Tuple[List[Predicate], List[Instantiated_Action]]:

    if isinstance(problem, HierarchicalGoalNetworkProblem):
        asp_encoding = compile_HGN_into_asp(problem)
    elif isinstance(problem, ClassicalPlanningProblem):
        asp_encoding = compile_classical_into_asp(problem)
        
    else:
        raise Exception(f'{type(problem)} is not handled in asp')

    encoding_file_path = os.path.join(current_dir, 'asp_encoding.lp')
    print(asp_encoding)
    print(encoding_file_path)

    with open(encoding_file_path, 'w') as encoding_file:
        encoding_file.write(asp_encoding)
    
    ctl = clingo.Control()

    ctl.load(encoding_file_path)
    ctl.ground([("base", [])], context=Context())
    ctl.add("check", ["t"], "#external query(t).")

    print("solving phase:")

    model = []
    for step in range(1,MAX_STEP):
        print(f'step number: {step}')
        ctl.ground([("step", [clingo.Number(step)])])
        ctl.ground([("check", [clingo.Number(step)])])
        ctl.assign_external(clingo.Function("query", [clingo.Number(step)]), True)
        with ctl.solve(yield_=True) as handle:
            for m in handle:
                if len(m.symbols(atoms=True)) == 0:
                    print('no module')
                else:
                    model = m.symbols(atoms=True)

        ctl.release_external(clingo.Function("query", [clingo.Number(step)]))
        if len(model) >0:
            break

    final_holds = []
    plan = []

    #get maximum timestamp
    max_timestamp = 1
    for fluent in model:
        if fluent.name == 'holds':
            max_timestamp = max(max_timestamp, fluent.arguments[1].number)
    print(f'maximum timestamp {max_timestamp}')
    for fluent in model:
        if fluent.name == 'holds' and fluent.arguments[1].number == max_timestamp:
            if fluent.arguments[0].name != 'neg' and fluent.positive:

                #here!
                final_holds.append(to_problem_literal(problem.fluents, fluent.arguments[0]))
                #final_holds.append(str(fluent.arguments[0]))
        elif fluent.name == 'occurs' and fluent.positive:
            operation_name = fluent.arguments[0].name
            if operation_name in [act.name for act in problem.actions]:
                action = action_2_instantiated_action(problem, fluent.arguments[0])
                index = int(str(fluent.arguments[1]))
                plan.append((action, index))
    
    plan = [x[0] for x in sorted(plan, key=lambda x : x[1])]
    #print(final_holds, plan)
    return final_holds, plan
