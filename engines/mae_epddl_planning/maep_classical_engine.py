from typing import List, Union, TypeVar, Iterator
import re
import os
import sys
from compiler_to_epddl import compile_into_epddl
import epddl_engine
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

def solve(maep_classical: MEPClassical):
    solution = epddl_engine.solve(maep_classical)
