from typing import List, Union
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(1, os.path.join(current_dir, '..', '..'))

from model import *

def enum_values(enum_type: EnumType) -> str:
    """EnumType to its value separated by ;"""
    assert enum_type.is_enum_type()
    return ';'.join(enum_type)


def int_values(int_type: IntType) -> str:
    """IntType to min..max"""
    assert int_type.is_int_type()
    return f"{int_type.min}..{int_type.max}"


def struct_values(struct_type: StructType) -> str:
    """StructType to sub_types separated by ,"""
    assert struct_type.is_struct_type()
    sub_domains = []
    for sub_t in struct_type:
        if sub_t.is_enum_type():
            sub_domains.append(enum_values(sub_t))
        elif sub_t.is_int_type():
            sub_domains.append(int_values(sub_t))
        else:
            assert False
    return ','.join(sub_domains)


def title_section(title: str) -> str:
    """decorate section title with %"""
    new_lines = '\n\n'
    comments  = '%'*10
    return new_lines + comments + ' ' + title + ' ' + comments + new_lines


def literal(predicate: Literal) -> str:
    """Literal to asp representation"""
    neg = predicate.negated
    lit_str = ""
    if isinstance(predicate, Literal):
        f_name = f"{predicate.fluent.name}"
        lit_str = f_name
        if len(predicate.args) > 0:
            lit_str += '(' + ','.join(map(param_val_2_asp, predicate.args)) + ')'
        
        if neg:
            return "neg(" + lit_str + ")"

        return lit_str
    assert False

def equality_predicate(predicate: EqualityPredicate) -> str:
    """EqualityPredicate to asp representation"""
    if isinstance(predicate, EqualityPredicate):
        operator = predicate.operator.value
        left_val = param_val_2_asp(predicate.left_operand)
        right_val = param_val_2_asp(predicate.right_operand)
        return left_val + operator + right_val
    assert False
    return ''

def param_val_2_asp(param_val: Union[ArithmeticExpr, int, Variable, str]):

    if isinstance(param_val, str): return param_val
    elif isinstance(param_val, int): return str(param_val)
    elif isinstance(param_val, Variable): return param_val.name.upper()
    elif isinstance(param_val, ArithmeticExpr):
        left_val  = param_val_2_asp(param_val.values[0])
        right_val = param_val_2_asp(param_val.values[1])

        op = param_val.operator.value

        return '(' + left_val + op + right_val + ')'
    else:
        assert False

def to_asp_lines(lines: List[str]) -> str:
    if len(lines) == 0: return ""
    SEP = '.\n'
    return SEP.join(lines)+SEP

def next_alpha(s):
    return chr((ord(s.upper())+1 - 65) % 26 + 65)

def fluent_2_asp(f: Fluent) -> str:

    fluent_name = f.name
    if f.type.is_bool_type():
        return "fluent("+fluent_name+")"
    elif f.type.is_enum_type() or f.type.is_int_type():
        t = f.type
        return f"fluent({fluent_name}(X)):-{t.name}(X)"
    elif f.type.is_struct_type():
        l = []
        var = "A"
        s = f"fluent({fluent_name}("
        for sub_t in f.type:
            l.append((var, sub_t))
            var = next_alpha(var)
        vars = ", ".join([var for var, var_type in l])
        s += vars + ")):-"
        s += ",".join([f"{var_type.name}({var})" for var, var_type in l])
        return s

def action_to_asp(action: IAction, pre: str = None) -> str:
    name = action.name
    variables = action.params
    s = ''
    if len(action.params) == 0:
        s = f'action({name})'
        return s
    else:
        parameters = ','.join(map(param_val_2_asp, action.params))
        s = f'action({name}({parameters}))'
    if len(variables) > 0:
        if pre is None:
            return s + f':-{vars_to_asp(variables)}'
        else:
            return s + f':-{vars_to_asp(variables)}, {pre}'

def action_exec(action: IAction, exec_lit: Predicate) -> str:

    variables = set(action.params + exec_lit.variables)
    body = "" if len(variables) == 0 else ':-' + vars_to_asp(variables)
    if len(action.params) == 0:
        return f'exec({action.name},{literal(exec_lit)})' + body
    else:
        parameters = ','.join(map(param_val_2_asp, action.params))
        return f'exec({action.name}({parameters}),{literal(exec_lit)})' + body

def action_causes(action: IAction, cause_lit: Literal) -> str:

    variables = set(action.params + cause_lit.variables)
    body = "" if len(variables) == 0 else ':-' + vars_to_asp(variables)
    if len(action.params) == 0:
        return f'causes({action.name},{literal(cause_lit)})' + body
    else:
        parameters = ','.join(map(param_val_2_asp, action.params))
        return f'causes({action.name}({parameters}),{literal(cause_lit)})' + body

def vars_to_asp(variables: List[Variable]) -> str:

    print(variables)
    return ",".join([f"{var.type.name}({var.name.upper()})" for var in variables])

def independent_rules() -> List[str]:

    return [
        #OPPOSITE:
        "opposite(F, neg(F)) :- fluent(F)",
        "opposite(neg(F), F) :- fluent(F)",
        "#program step(t)",
        #INERTIA:
        "holds(F,t+1) :- opposite(F,G), holds(F,t), not holds(G, t+1)",
        #"holds(F,t):- not holds(G,t), opposite(F,G)",
        #EXECUTABILITY:
        "not_executable(A,t) :- fluent(F), exec(A,F), not holds(F,t)",
        "not_executable(A,t) :- exec(A,G), opposite(F,G), holds(F,t)",
        "executable(A,t) :- not not_executable(A,t), action(A)",
        "holds(F, t+1) :- executable(A,t), occurs(A,t), causes(A,F)",
        #OCCURS
        "1{occurs(A,t) : action(A)}1",
        ":- action(A), occurs(A,t), not executable(A,t)",
        #LAST STEP
        "#program check(t)",
        ":- goal(F), not holds(F,t+1), query(t)",
        ":- goal(neg(F)), holds(F,t+1), query(t)",
        "#program base"
    ]

def compile_classical_into_asp(problem: HierarchicalGoalNetworkProblem) -> str:


    s =  "%Answer set planning.\n\n"
    s += "%Answer set planning: A Survey. E. Pontelli et al. For a survey.\n"
    s += "%Epistemic Multiagent Reasoning with Collaborative Robots: D. Solda' el al. For a practical use-case.\n\n"

    s += title_section("[[\tPROBLEM DEPENDENT RULES\t]]")
    
    s += title_section('TYPES')
    type_asp_convertion = []
    for t in problem.types:
        if t.is_enum_type() or t.is_int_type() or t.is_struct_type():
            if t.is_enum_type():
                type_asp_convertion.append(f"{t.name}({enum_values(t)})")
            elif t.is_int_type():
                type_asp_convertion.append(f"{t.name}({int_values(t)})")
            #elif t.is_struct_type():
            #    type_asp_convertion.append(f"{t.name}({struct_values(t)})")
                

    s += to_asp_lines(type_asp_convertion)

    s += title_section('FLUENTS')

    fluent_asp = []
    for fluent in problem.fluents:
        fluent_asp.append(fluent_2_asp(fluent))

    s += to_asp_lines(fluent_asp)
    
    s += title_section('INITIALLY')

    init_values = []
    for lit in problem.init_values:
        init_values.append("holds(" + literal(lit) + ", 1)")

    s += to_asp_lines(init_values)

    s += title_section('ACTIONS')

    actions = []
    for action in problem.actions:
        action_equality_conds = []
        for precond in action.precondition:
            if isinstance(precond, EqualityPredicate):
                action_equality_conds.append(equality_predicate(precond))
        if len(action_equality_conds) == 0:
            actions.append(action_to_asp(action))
        else:
            actions.append(action_to_asp(action, ", ".join(action_equality_conds)))

    s += to_asp_lines(actions)

    s += title_section('EXECUTABLE')

    executabilities = []

    for action in problem.actions:
        for precond in action.precondition:
            if isinstance(precond, Literal):
                executabilities.append(action_exec(action, precond))

    s += to_asp_lines(executabilities)

    s += title_section('CAUSES')

    causes = []
    for action in problem.actions:
        for effect in action.effects:
            causes.append(action_causes(action, effect))

    s += to_asp_lines(causes)

    s += title_section('GOALS')
    goals = []
    for goal in problem.goals:
        goals.append('goal(' + literal(goal) + ')')

    s += to_asp_lines(goals)
    
    s += title_section("[[\tPROBLEM INDEPENDENT RULES\t]]")

    s += to_asp_lines(independent_rules())

    return s
