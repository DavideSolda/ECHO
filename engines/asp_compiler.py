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
            return "not " + lit_str

        return lit_str
    elif isinstance(lit, BELiteral):
        operator = lit.operator.value
        left_val = param_val_2_asp(lit._args[0])
        right_val = param_val_2_asp(lit._args[1])
        return left_val + operator + right_val
        

def param_val_2_asp(param_val : Union[ArithmeticExpr, int, Variable, str]):

    if isinstance(param_val, str): return param_val
    elif isinstance(param_val, int): return str(param_val)
    elif isinstance(param_val, Variable):
        name = param_val.name
        t = param_val.type.name
        return f"{t}({name.upper()})"#TODO check uniqueness
    elif isinstance(param_val, ArithmeticExpr):
        left_val  = param_val_2_asp(param_val.values[0])
        right_val = param_val_2_asp(param_val.values[1])

        op = param_val.operator.value

        return '(' + left_val + op + right_val + ')'
    else:
        assert False

def to_asp_lines(lines : List[str]) -> str:
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
        s += vars + "):-"
        s += ",".join([f"{var_type.name}({var})" for var, var_type in l])
        return s
            

def compile_into_asp(problem : Problem) -> str:


    s =  "%Answer set planning.\n\n"
    s += "%Answer set planning: A Survey. E. Pontelli et al. For a survey.\n"
    s += "%Epistemic Multiagent Reasoning with Collaborative Robots: D. Solda' el al. For a practical use-case."

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

    s += title('EXECUTABLE')

    executabilities = []

    for action in problem.actions:
        action_name = action.name
        params = ','.join(map(param_val_2_asp, action.params))
        precond = ','.join(map(literal, action.precondition))
        executabilities.append(action_name + '(' + params + ') :- ' + precond)

    s += to_asp_lines(executabilities)
    print(s)
    return s
