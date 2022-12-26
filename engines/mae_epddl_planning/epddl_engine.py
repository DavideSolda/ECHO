from typing import List, Union, TypeVar, Iterator
import re
import os
import sys

from .compiler_to_epddl import compile_into_epddl
from sofai.Planners.EPDDL.parser import EPDDL_Parser

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, os.path.join(CURRENT_DIR, '..', '..'))
from model import *


TEMP = 'temp'
DOMAIN_F = os.path.join(CURRENT_DIR, TEMP, 'domain.epddl')
PROBLEM_F = os.path.join(CURRENT_DIR, TEMP, 'problem.epddl')
EFP = os.path.join(CURRENT_DIR, 'sofai',
                   'Planners', 'EFP', 'bin', 'efp.out')
EFP_OUTPUT = os.path.join(CURRENT_DIR, TEMP, 'efp_output.txt')


def solve_mae(mepproblem: MEPlanningProblem) -> Iterator[Instantiated_Action]:

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
    mAp_f = os.path.join(CURRENT_DIR, TEMP,
                         parser.domain_name + "_" + parser.problem_name + '.tmp')
    file_name = parser.print_EFP(os.path.join(CURRENT_DIR, TEMP), mAp_f)

    print(mAp_f)

    os.system(f'''{EFP} {mAp_f} > {EFP_OUTPUT}''')
    #os.system(f'''{EFP} {mAp_f}  -st KRIPKE_OPT -h SUBGOALS > {EFP_OUTPUT}''')
    #  read mAp plan
    mAp_plan = []
    with open(EFP_OUTPUT) as mAp_solution:
        for line in mAp_solution:
            if 'Solution =' in line:
                print(line)
                s = line[len('Solution =  '):-1]
                mAp_plan = s.split(', ')

    print(mAp_plan)
    if mAp_plan == ['']:
        return zip([],[])

    action_name_plan = []
    #collect action names:
    for action in mAp_plan:
        action_name_plan.append(action.split('_')[0])

    instantiated = []
    #collect instantiations:
    for action in mAp_plan:
        instantiated.append(action.split('_')[1:])

    print(action_name_plan)
    print(instantiated)

    def find_in_domain(action_name: str) -> MEAction:
        dom = mepproblem.actions
        for act in dom:
            if act.name == action_name:
                return act
    maection_plan = [find_in_domain(action_name)
                     for action_name in action_name_plan]

    print(maection_plan)
    return zip(maection_plan, instantiated)
