"""Module to compile an multi agent epistemic planning problem into epddl"""
from typing import Tuple, Union, List
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
    if isinstance(fluent_type, pd.AgentType):
        return f'?ag_{get_random_string(5)} - ' + 'agent'
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


def var_param(variable: pd.Variable) -> str:
    """replace agents with agent"""
    if variable.is_agent():
        return f'?{variable.name.lower()} - agent'
    return f'?{variable.name.lower()} - {variable.type.name.lower()}'


def parameters(variables: List[pd.Variable]) -> str:
    """from list of pd.Variable to epddl parameters"""
    variables = list(set(variables))
    return ' '.join([var_param(variable)
                     for variable in variables])


def param_val_to_epddl(param_val: Union[pd.ArithmeticExpr,
                                        int, pd.Variable, str],
                       prob) -> str:
    """from pd.ArithmeticExpr, int, pd.Variable, str to epddl parameters"""
    if isinstance(param_val, str):
        return param_val
    if isinstance(param_val, int):
        return str(param_val)
    if isinstance(param_val, pd.Variable):
        if prob:
            return f'{param_val.name.lower()}'
        return f'?{param_val.name.lower()}'
    if isinstance(param_val, pd.ArithmeticExpr):
        left_val = param_val_to_epddl(param_val.values[0], prob)
        right_val = param_val_to_epddl(param_val.values[1], prob)
        op = param_val.operator.value
        return '(' + left_val + op + right_val + ')'
    assert False


def literal(lit: pd.Literal, prob: bool) -> str:
    """from pd.Literal to epddl literal"""
    f_name = f"{lit.fluent.name}"
    return f_name + ' ' + ','.join(map(lambda x: param_val_to_epddl(x, prob)
                                       , lit.args))


def agent(ag: Union[str, pd.Variable], prob=False) -> str:
    """from agento to EPDDL agent"""
    if isinstance(ag, str):
        if prob:
            return ag
        return '?'+ag
    if isinstance(ag, pd.Variable):
        if prob:
            return ag.name.lower()
        return '?'+ag.name.lower()
    assert False


def negate(p: str, prob: bool) -> str:
    """neagte a predicate.If prob for the domain enc., else for problem enc."""
    if prob:
        return 'not (' + p + ')'
    return '-' + p


def pred(_predicate: pd.Predicate, prob=False) -> str:
    """from pd.Predicate to epddl's action predicate"""
    neg = _predicate.negated
    epddl_pred = ''
    if isinstance(_predicate, pd.Literal):
        epddl_pred = f'{literal(_predicate, prob)}'
    elif isinstance(_predicate, pd.BeliefLiteral):
        def to_agent(ag: Union[str, pd.Variable]):
            return agent(ag, prob)
        
        agents = '[' + ' '.join(map(to_agent, _predicate.agents)) + ']'
        prop = pred(_predicate.belief_proposition, prob)
        epddl_pred = f'{agents}({prop})'
    elif isinstance(_predicate, pd.BooleanPredicate):
        op = _predicate.op.value
        l_pred = pred(_predicate.left_predicate())
        r_pred = pred(_predicate.right_predicate())
        return op + ' (' + l_pred + ') (' + r_pred + ')'
    elif isinstance(_predicate, pd.When):
        epddl_pred = f'when ({pred(_predicate.body)}) ({pred(_predicate.head)})'
    else:
        assert False
    if neg:
        epddl_pred = negate(epddl_pred, prob=prob)
    return epddl_pred


def preds(predicates: List[pd.Predicate]) -> str:
    """from list of pd.Predicate to epddl's action predicates"""
    assert len(predicates) > 0
    if len(predicates) == 1:
        return f'{pred(predicates[0])}'
    return 'and ' + ' '.join(map(lambda x: '(' + x + ')',
                                 map(pred, predicates)))


def obss(full_observers: List[Union[pd.ObservablePredicate,
                                         str, pd.Variable]]) -> str:
    """from list of observer to epddl observers"""
    return ' '.join(map(obs, full_observers))


def forall(forall_obj: Union[pd.Variable, pd.EqualityPredicate]):
    if isinstance(forall_obj, pd.Variable):
        return f'{agent(forall_obj)}'
    if isinstance(forall_obj, pd.EqualityPredicate):

        assert forall_obj.operator == pd.EqualityOperator.neq
        vars = forall_obj.variables
        for var in vars:
            assert isinstance(var, pd.Variable)
        assert len(vars) == 2
        return f'diff({agent(vars[0])})({agent(vars[1])})'


def obs(full_observer: Union[pd.ObservablePredicate,
                             str, pd.Variable]) -> str:
    if isinstance(full_observer, str):
        return f'({agent(full_observer)})'
    if isinstance(full_observer, pd.Variable):
        return f'({agent(full_observer.name.lower())})'
    if isinstance(full_observer, pd.ObservablePredicate):
        who = f'({agent(full_observer.who)})'
        s = who
        if full_observer.when is not None:
            when = f'({pred(full_observer.when)})'
            s = who + ' ' + when
        if full_observer.forall is not None:
            s = f'(forall ({forall(full_observer.forall)}) {s})'
    return s


def action(mep_action: pd.MEAction) -> str:
    """from pd.MEAction to epddl action"""
    action_enc = f'\t(:action {mep_action.name}\n'
    action_enc += f'\t\t:act_type {mep_action.type.value}\n'
    if len(mep_action.params) > 0:
        action_enc += f'\t\t:parameters ({parameters(mep_action.params)})\n'
    if len(mep_action.preconditions) > 0:
        action_enc += f'\t\t:precondition ({preds(mep_action.preconditions)})\n'
    if len(mep_action.effects) > 0:
        action_enc += f'\t\t:effect ({preds(mep_action.effects)})\n'
    if len(mep_action.full_observers) > 0:
        action_enc += f'\t\t:observers (and {obss(mep_action.full_observers)})\n'
    if len(mep_action.partial_observers) > 0:
        action_enc += f'\t\t:p_observers (and {obss(mep_action.partial_observers)})'
    return action_enc + '\n\t)'


def agent_names(problem: pd.MEPlanningProblem) -> str:
    """serach for the type of agents and returns a list of agent names"""
    agent_type = next(iter([t for t in problem.types
                            if t.is_agent_type()]))
    return ' '.join(agent_type.domain)


def enclose_into_brackets(p: str) -> str:
    return '(' + p + ')'


def problem_predicate_encoding(p: pd.Predicate) -> str:
    return pred(p, prob=True)


def init(problem: pd.MEPlanningProblem) -> str:
    """obtain sequence of epddl initial predicates"""
    return ' '.join(map(enclose_into_brackets,
                        map(problem_predicate_encoding,
                            problem.init_values)))

def goal(problem: pd.MEPlanningProblem) -> str:
    """obtain sequence of epddl goal predicates"""
    return ' '.join(map(enclose_into_brackets,
                        map(problem_predicate_encoding,
                            problem.goals)))

#  TODO till now only enums are supported
def process_type(t: pd.Type) -> str:
    return '\t\t' + ' '.join(t.domain) + ' - ' + t.name.lower()


def types(problem: pd.MEPlanningProblem) -> str:
    """from types to PDDL types"""
    if len(problem.types) > 1:
        types = map(process_type, [t for t in problem.types if not t.is_agent_type()])
        return '\t(:types\n' + '\n'.join(types) + '\n\t)\n'
    return ''


def compile_into_epddl(problem: pd.MEPlanningProblem) -> Tuple[str, str]:
    """from pd.MEPlanningProblem to epddl domain and problem files"""
    p_dom = f'(define (domain {problem.name})\n'
    p_dom += '\t(:requirements :strips :negative-preconditions :mep :no-duplicates)\n'

    #  fluents:
    p_dom += '\t(:predicates '
    p_dom += ' '.join(map(lambda fluent: f'({predicate(fluent)})',
                          problem.fluents)) + ')\n'

    # actions:
    p_dom += '\n'.join(map(action, problem.actions))

    p_dom += '\n)\n'
    p_inst = f'(define (problem {problem.name})\n'
    p_inst += f'\t(:domain {problem.name})\n'
    p_inst += f'\t(:agents {agent_names(problem)})\n'
    p_inst += types(problem)
    p_inst += '\t(:depth 2)\n'
    p_inst += '\t(:dynck false)\n'
    p_inst += f'\t(:init {init(problem)})\n'
    p_inst += f'\t(:goal {goal(problem)})\n'
    p_inst += ')'
    return p_dom, p_inst
