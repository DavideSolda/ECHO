from typing import List, Union, TypeVar, Iterator
import re
import os
import sys
from compiler_to_epddl import compile_into_epddl
from sofai.Planners.EPDDL.parser import EPDDL_Parser
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, os.path.join(CURRENT_DIR, '..', 'model'))
import shortcuts as pd
TEMP = 'temp'
DOMAIN_F = os.path.join(CURRENT_DIR, TEMP, 'domain.epddl')
PROBLEM_F = os.path.join(CURRENT_DIR, TEMP, 'problem.epddl')
EFP = os.path.join(CURRENT_DIR, 'sofai',
                   'Planners', 'EFP', 'build', 'efp.out')
EFP_OUTPUT = os.path.join(CURRENT_DIR, TEMP, 'efp_output.txt')
EX_DOMAIN_F = os.path.join(CURRENT_DIR, TEMP,
                           'coin_in_the_box', 'coininthebox.epddl')
EX_PROBLEM_F = os.path.join(CURRENT_DIR, TEMP,
                            'coin_in_the_box', 'pb01_01.epddl')


IstantiatedMEAction = TypeVar("Istantiated_MEAction")


def solve(mepproblem: pd.MEPlanningProblem) -> Iterator[IstantiatedMEAction]:

    domain_s, problem_s = compile_into_epddl(mepproblem)
    print('>'*30)
    print('>'*30)
    print('>'*30)
    print(domain_s)
    print(problem_s)
    with open(DOMAIN_F, 'w') as domain:
        domain.write(domain_s)
    with open(PROBLEM_F, 'w') as problem:
        problem.write(problem_s)
    parser = EPDDL_Parser()
    parser.parse_domain(DOMAIN_F)  # EX_DOMAIN_F)
    parser.parse_problem(PROBLEM_F)  # EX_PROBLEM_F)
    parser.print_EFP(os.path.join(CURRENT_DIR, TEMP))
    mAp_f = os.path.join(CURRENT_DIR, TEMP,
                         parser.domain_name + "_" + parser.problem_name + '.tmp')
    os.system(f'''{EFP} {mAp_f}  -st KRIPKE_OPT -h SUBGOALS > {EFP_OUTPUT}''')
    #  read mAp plan
    mAp_plan = []
    with open(EFP_OUTPUT) as mAp_solution:
        for line in mAp_solution:
            if 'Executed actions: ' in line:
                s = line[len('Executed actions: '):-1]
                mAp_plan = s.split(', ')

    action_name_plan = [re.split('_PARAMS_', act)[0] for act in mAp_plan]
    instantiated = [re.split('PARAMS_', act)[1].split('_') for act in mAp_plan]

    def find_in_domain(action_name: str) -> pd.MEAction:
        dom = mepproblem.actions
        for act in dom:
            if act.name == action_name:
                return act
    maection_plan = [find_in_domain(action_name)
                     for action_name in action_name_plan]

    return zip(maection_plan, instantiated)
