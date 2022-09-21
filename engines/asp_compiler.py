from typing import List, Union

import os
current_dir = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.insert(1, os.path.join(current_dir, '..', 'model'))
from shortcuts import *

#holds(F,T)
#occ(A,T)
#possible(A,T)

def enum_values(t : EnumType) -> str:
    assert t.is_enum_type()
    return ';'.join(t)

def int_values(t : IntType) -> str:
    assert t.is_int_type()
    return f"{t.min}..{t.max}"

def struct_values(t : StructType) -> str:
    assert t.is_struct_type()
    sub_domains = []
    for sub_t in t:
        if sub_t.is_enum_type(): sub_domains.append(enum_values(sub_t))
        elif sub_t.is_int_type(): sub_domains.append(int_values(sub_t))
        else: assert False
    return ','.join(sub_domains)

def title(title : str) -> str:
    new_lines = '\n\n'
    comments  = '%'*10
    return new_lines + comments + ' ' + title + ' ' + comments + new_lines

def literal(lit : Literal) -> str:
    neg = lit.negated
    lit_str = ""
    if isinstance(lit, FLiteral):
        f_name = f"{lit.fluent.name}"
        lit_str = f_name + '(' + ','.join(map(param_val_2_asp, lit.args)) + ')'
        if neg :
            return "neg " + lit_str

        return lit_str
    elif isinstance(lit, BELiteral):
        operator = lit.operator.value
        left_val = param_val_2_asp(lit._args[0])
        right_val = param_val_2_asp(lit._args[1])
        return left_val + operator + right_val
        

def param_val_2_asp(param_val : Union[ArithmeticExpr, int, Variable, str]):

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

def to_asp_lines(lines : List[str]) -> str:
    if len(lines) == 0 : return "" 
    SEP = '.\n'
    return  SEP.join(lines)+SEP

def next_alpha(s):
    return chr((ord(s.upper())+1 - 65) % 26 + 65)

def fluent_2_asp(f : Fluent) -> str:

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

def action_to_asp(action : I_Action) -> str:
    name = action.name
    variables = action.params_var
    s = ''
    if len(action.params) > 1:
        s = f'action({name})'
        return s
    else:
        parameters = ','.join(map(param_val_2_asp, action.params))
        s = f'action({name}({parameters}))'
    if len(variables) > 0:
        s += f':-{vars_to_asp(variables)}'
    return s

def action_exec(action : I_Action, exec_lit : Literal) -> str:

    variables = action.params_var + exec_lit.variables
    body = "" if len(variables) == 0 else ':-' + vars_to_asp(variables)
    if len(action.params) == 0:
        return f'exec({action.name},{literal(exec_lit)})' + body
    else:
        parameters = ','.join(map(param_val_2_asp, action.params))
        return f'exec({action.name}({parameters}),{literal(exec_lit)})' + body 

def action_causes(action : I_Action, effect_lit : Literal) -> str:

    variables = action.params_var + effect_lit.variables
    body = "" if len(variables) == 0 else ':-' + vars_to_asp(variables)
    if len(action.params) == 0:
        return f'causes({action.name},{literal(effect_lit)})' + body
    else:
        parameters = ','.join(map(param_val_2_asp, action.params))
        return f'causes({action.name}({parameters}),{literal(effect_lit)})' + body 

def vars_to_asp(variables : List[Variable]) -> str:

    return ",".join([f"{var.type.name}({var.name.upper()})" for var in variables])

def independent_rules() -> List[str]:

    return [
        #TIME:
        "time(0..l)",
        #OPPOSITE:
        "opposite(F, neg(F)) :- fluent(F)",
        "opposite(neg(f), F) :- fluent(F)",
        #INERTIA:
        "holds(F,T+1) :- opposite(F,G), T < l, holds(F,T), not holds(G, T+1)",
        #GOALS:
        "not_goal_at(T) :- time(T), not holds(F, T), goal(F), fluent(F)",
        ":- not_goal_at(l)",
        #EXECUTABILITY:
        "not_executable(A,T) :- exec(A,F), not holds(F,T), time(T)",
        "executable(A,T) :- T < l, not not_executable(A,T), time(T), action(A)",
        "holds(F, T+1) :- T < l, executable(A,T), occurs(A,T), causes(A,F)",
        "#show executable/2",
        #OCCURS
        "{occurs(A,T) : action(A)}1 :- time(T)",
        ":- action(A), time(T), occurs(A,T), not executable(A,T)"]
    """
        #OCCURS:
        "occurs(A,T) :- action(A), time(T), not goal(T), not not_occurs(A,T)",
        "not_occurs(A,T) :- action(A), action(B), time(T), occurs(B,T), A!=B",
        ":- action(A), time(T), occurs(A,T), not executable(A,T)",
        "#show holds/2",
        "#show goal/1"
    ]
    """
def compile_into_asp(problem : Problem) -> str:


    s =  "%Answer set planning.\n\n"
    s += "%Answer set planning: A Survey. E. Pontelli et al. For a survey.\n"
    s += "%Epistemic Multiagent Reasoning with Collaborative Robots: D. Solda' el al. For a practical use-case.\n\n"

    s += title("[[\tPROBLEM DEPENDENT RULES\t]]")
    
    s += title('TYPES')
    type_asp_convertion = []
    for t in problem.types:
        if t.is_enum_type() or t.is_int_type() or t.is_struct_type():
            if t.is_enum_type():
                type_asp_convertion.append(f"{t.name}({enum_values(t)})")
            elif t.is_int_type():
                type_asp_convertion.append(f"{t.name}({int_values(t)})")
            elif t.is_struct_type():
                type_asp_convertion.append(f"{t.name}({struct_values(t)})")
                

    s += to_asp_lines(type_asp_convertion)

    s += title('FLUENTS')

    fluent_asp = []
    for fluent in problem.fluents:
        fluent_asp.append(fluent_2_asp(fluent))

    s += to_asp_lines(fluent_asp)
    
    s += title('INITIALLY')

    init_values = []
    for lit in problem.init_values:
        init_values.append("holds(" + literal(lit) + ", 0)")

    s += to_asp_lines(init_values)

    s += title('ACTIONS')

    actions = []
    for action in problem.actions:
        actions.append(action_to_asp(action))

    s += to_asp_lines(actions)

    s += title('EXECUTABLE')

    executabilities = []

    for action in problem.actions:
        action_name = action.name
        params = ','.join(map(param_val_2_asp, action.params))
        for precond in action.precondition:
            executabilities.append(action_exec(action, precond))

    s += to_asp_lines(executabilities)

    s += title('CAUSES')

    causes = []
    for action in problem.actions:
        action_name = action.name
        params = ','.join(map(param_val_2_asp, action.params))
        for effect in action.effects:
            causes.append(action_causes(action, effect))

    s += to_asp_lines(causes)

    s += title('GOALS')
    goals = []
    for goal in problem.goals:
        goals.append('goal(' + literal(goal) + ')')

    s += to_asp_lines(goals)
    
    s += title("[[\tPROBLEM INDEPENDENT RULES\t]]")

    s += to_asp_lines(independent_rules())

    return s
