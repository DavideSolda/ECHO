"""Module to compile an multi agent epistemic planning problem into epddl"""
from typing import Tuple, Union
import sys
import os
import string
import random
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, os.path.join(CURRENT_DIR, '..', 'model'))
import shortcuts as pd


def get_random_string(length: int) -> str:
    """choose from all lowercase letter"""
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def predicate_argument(fluent_type: Union[pd.IntType,
                                          pd.EnumType,
                                          pd.StructType]) -> str:
    """from pd.FType to epddl argument of predicates"""
    type_name = fluent_type.name
    if isinstance(fluent_type, (pd.IntType, pd.EnumType)):
        return f'?{type_name}_{get_random_string(5)} - ' + type_name
    if isinstance(fluent_type, pd.StructType):
        return ' '.join(map(predicate_argument, fluent_type))
    assert False
    return ''


def predicate(fluent: pd.Fluent) -> str:
    """from pd.Fluent to epddl predicate"""
    if fluent.type.is_bool_type():
        return f'{fluent.name}'
    return f'{fluent.name} ' + ' ' + predicate_argument(fluent.type)


def compile_into_epddl(problem: pd.MEPlanningProblem) -> Tuple[str, str]:
    """from pd.MEPlanningProblem to epddl domain and problem files"""
    s = f'define( domain {problem.name})\n'
    s += '  (:requirements :strips :negative-preconditions :mep)\n'

    #  fluents:
    s += '(:predicates '
    s += ' '.join(map(lambda fluent: f'({predicate(fluent)})',
                      problem.fluents)) + ')\n'

    return s
