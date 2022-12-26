"""Module to compile an multi agent epistemic planning problem into epddl"""
from typing import Tuple, Union, List
import sys
import os
import string
import random
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, os.path.join(CURRENT_DIR, '..', '..'))

from model import *

def get_random_string(length: int) -> str:
    """choose from all lowercase letter"""
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def predicate_argument(fluent_type: Union[IntType,
                                          EnumType,
                                          StructType]) -> str:
    """from FType to epddl argument of predicates"""
    if isinstance(fluent_type, AgentType):
        return f'?ag_{get_random_string(5)} - ' + 'agent'
    type_name = fluent_type.name
    if isinstance(fluent_type, (IntType, EnumType)):
        return f'?{type_name}_{get_random_string(5)} - ' + type_name
    if isinstance(fluent_type, StructType):
        return ' '.join(map(predicate_argument, fluent_type))
    assert False
    return ''


def predicate(fluent: Fluent) -> str:
    """from Fluent to epddl predicate"""
    if fluent.type.is_bool_type():
        return f'{fluent.name}'
    return f'{fluent.name} ' + ' ' + predicate_argument(fluent.type)


def var_param(variable: Variable) -> str:
    """replace agents with agent"""
    if variable.is_agent():
        return f'?{variable.name.lower()} - agent'
    return f'?{variable.name.lower()} - {variable.type.name.lower()}'


def parameters(variables: List[Variable]) -> str:
    """from list of Variable to epddl parameters"""
    variables = variables
    return ' '.join([var_param(variable)
                     for variable in variables])


def param_val_to_epddl(param_val: Union[ArithmeticExpr,
                                        int, Variable, str],
                       prob) -> str:
    """from ArithmeticExpr, int, Variable, str to epddl parameters"""
    if isinstance(param_val, str):
        return param_val
    if isinstance(param_val, int):
        return str(param_val)
    if isinstance(param_val, Variable):
        if prob:
            return f'{param_val.name.lower()}'
        return f'?{param_val.name.lower()}'
    if isinstance(param_val, ArithmeticExpr):
        left_val = param_val_to_epddl(param_val.values[0], prob)
        right_val = param_val_to_epddl(param_val.values[1], prob)
        op = param_val.operator.value
        return '(' + left_val + op + right_val + ')'
    assert False


def literal(lit: Literal, prob: bool) -> str:
    """from Literal to epddl literal"""
    f_name = f"{lit.fluent.name}"
    return f_name + ' ' + ' '.join(map(lambda x: param_val_to_epddl(x, prob)
                                       , lit.args))


def agent(ag: Union[str, Variable], prob=False) -> str:
    """from agento to EPDDL agent"""
    if isinstance(ag, str):
        if prob:
            return ag
        return '?'+ag
    if isinstance(ag, Variable):
        if prob:
            return ag.name.lower()
        return '?'+ag.name.lower()
    assert False


def negate(p: str, prob: bool) -> str:
    """neagte a predicate.If prob for the domain enc., else for problem enc."""
    if prob:
        return 'not (' + p + ')'
    return '-' + p


def pred(_predicate: Predicate, prob=False) -> str:
    """from Predicate to epddl's action predicate"""
    neg = _predicate.negated
    epddl_pred = ''
    if isinstance(_predicate, Literal):
        epddl_pred = f'{literal(_predicate, prob)}'
    elif isinstance(_predicate, BeliefPredicate):
        def to_agent(ag: Union[str, Variable]):
            return agent(ag, prob)
        
        agents = '[' + ' '.join(map(to_agent, _predicate.agents)) + ']'
        prop = pred(_predicate.belief_proposition, prob)
        epddl_pred = f'{agents}({prop})'
    elif isinstance(_predicate, BooleanPredicate):
        op = _predicate.op.value
        l_pred = pred(_predicate.left_predicate, prob)
        r_pred = pred(_predicate.right_predicate, prob)
        return op + ' (' + l_pred + ') (' + r_pred + ')'
    elif isinstance(_predicate, When):
        epddl_pred = f'when ({pred(_predicate.body, prob)}) ({pred(_predicate.head, prob)})'
    else:
        assert False
    if neg:
        epddl_pred = negate(epddl_pred, prob=prob)
    return epddl_pred


def preds(predicates: List[Predicate]) -> str:
    """from list of Predicate to epddl's action predicates"""
    assert len(predicates) > 0
    if len(predicates) == 1:
        return f'{pred(predicates[0])}'
    return 'and ' + ' '.join(map(lambda x: '(' + x + ')',
                                 map(pred, predicates)))


def obss(observers: List[Union[Forall, str, Variable]]) -> str:
    """from list of observer to epddl observers"""
    return ' '.join(map(obs, observers))


def obs(observer: Union[Forall, str, Variable]) -> str:

    print(observer)
    if isinstance(observer, str):
        return f'({agent(observer)})'

    if isinstance(observer, Variable):
        return f'({agent(observer.name.lower())})'

    if isinstance(observer, Forall):
        who = f'{agent(observer.who)}'
        if observer.when is not None:
            who = f'when ({pred(observer.when)}) ({who})'

        forall = who
        if observer.disequality_predicate is not None:
            neq = observer.disequality_predicate
            agentl = agent(neq.left_operand.name.lower())
            agentr = agent(neq.right_operand.name.lower())
            if observer.who == neq.left_operand:
                forall = f'diff ({agentl}) ({agentr})'
            else:
                forall = f'diff ({agentr}) ({agentl})'

        return f'(forall ({forall}) ({who}))'




def action(mep_action: MEAction) -> str:
    """from MEAction to epddl action"""
    action_enc = f'\t(:action {mep_action.name}\n'
    action_enc += f'\t\t:act_type {mep_action.type.value}\n'
    if len(mep_action.params) > 0:
        action_enc += f'\t\t:parameters ({parameters(mep_action.params)})\n'
    if len(mep_action.precondition) > 0:
        action_enc += f'\t\t:precondition ({preds(mep_action.precondition)})\n'
    if len(mep_action.effects) > 0:
        action_enc += f'\t\t:effect ({preds(mep_action.effects)})\n'
    if len(mep_action.full_obs) > 0:
        action_enc += f'\t\t:observers (and {obss(mep_action.full_obs)})\n'
    if len(mep_action.partial_obs) > 0:
        action_enc += f'\t\t:p_observers (and {obss(mep_action.partial_obs)})'
    return action_enc + '\n\t)'


def agent_names(problem: MEPlanningProblem) -> str:
    """serach for the type of agents and returns a list of agent names"""
    agent_type = next(iter([t for t in problem.types
                            if t.is_agent_type()]))
    return ' '.join(agent_type.domain)


def enclose_into_brackets(p: str) -> str:
    return '(' + p + ')'


def problem_predicate_encoding(p: Predicate) -> str:
    return pred(p, prob=True)


def init(problem: MEPlanningProblem) -> str:
    """obtain sequence of epddl initial predicates"""
    return ' '.join(map(enclose_into_brackets,
                        map(problem_predicate_encoding,
                            problem.init_values)))

def goal(problem: MEPlanningProblem) -> str:
    """obtain sequence of epddl goal predicates"""
    return ' '.join(map(enclose_into_brackets,
                        map(problem_predicate_encoding,
                            problem.goals)))

#  TODO till now only enums are supported
def process_type(t: Type) -> str:
    return '\t\t' + ' '.join(t.domain) + ' - ' + t.name.lower()


def types(problem: MEPlanningProblem) -> str:
    """from types to PDDL types"""
    if len(problem.types) > 1:
        types = map(process_type, [t for t in problem.types if not t.is_agent_type() and not t.is_struct_type()])
        return '\t(:objects\n' + '\n'.join(types) + '\n\t)\n'
    return ''


def compile_into_epddl(problem: MEPlanningProblem) -> Tuple[str, str]:
    """from pd.MEPlanningProblem to epddl domain and problem files"""
    p_dom = f'(define (domain {problem.name})\n'
    p_dom += '\t(:requirements :strips :typing :negative-preconditions :mep :no-duplicates)\n'
    #  fluents:
    p_dom += '\t(:predicates '
    p_dom += ' '.join(map(lambda fluent: f'({predicate(fluent)})',
                          problem.fluents)) + ')\n'

    # actions:
    p_dom += '\n'.join(map(action, problem.actions))

    p_dom += '\n)\n'
    p_inst = f'(define (problem {problem.name})\n'
    p_inst += types(problem)
    p_inst += f'\t(:domain {problem.name})\n'
    p_inst += f'\t(:agents {agent_names(problem)})\n'
    p_inst += '\t(:depth 2)\n'
    p_inst += '\t(:dynck false)\n'
    p_inst += f'\t(:init {init(problem)})\n'
    p_inst += f'\t(:goal {goal(problem)})\n'
    p_inst += ')'
    return p_dom, p_inst
