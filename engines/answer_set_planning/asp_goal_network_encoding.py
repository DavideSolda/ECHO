from typing import List, Union

import os
current_dir = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.insert(1, os.path.join(current_dir, '..', 'model'))
import shortcuts as sc

from classical_asp_encoding import enum_values, int_values, struct_values,\
    title_section, literal, to_asp_lines, action_causes, action_to_asp,\
    fluent_2_asp, param_val_2_asp, vars_to_asp, action_exec

def operation_exec(action: Union[sc.IAction, sc.Method], exec_lit: sc.Predicate) -> str:

    variables = set(action.params + exec_lit.variables)
    body = "" if len(variables) == 0 else ':-' + vars_to_asp(variables)
    s = ""
    if len(action.params) == 0:
        s = f'exec({action.name},{literal(exec_lit)})' + body
    else:
        parameters = ','.join(map(param_val_2_asp, set(action.params)))
        s = f'exec({action.name}({parameters}),{literal(exec_lit)})' + body
    if isinstance(action, sc.IAction):
        return 'action_' + s
    else:
        return 'method_' + s

def method_to_asp(action: sc.Method) -> str:
    name = action.name
    variables = action.params
    s = ''
    if len(action.params) == 0:
        s = f'method({name})'
        return s
    else:
        parameters = ','.join(map(param_val_2_asp, action.params))
        s = f'method({name}({parameters}))'
    if len(variables) > 0:
        s += f':-{vars_to_asp(variables)}'
    return s


def method_req(method: sc.Method, prec: sc.Goal, succ: sc.Goal) -> str:
    name = method.name
    s = 'method_req('
    if len(method.params) == 0:
        s += f'{name}'
    else:
        parameters = ','.join(map(param_val_2_asp, method.params))
        s += f'{name}({parameters})'

    s += ', ' + goal(prec) + ', ' + goal(succ) + ')'

    if len(method.params) > 0:
        s += f':-{vars_to_asp(method.params)}'

    return s


def goal(g: sc.Goal) -> str:
    name = g.name
    if len(g.arguments) == 0:
        return f'{name}'
    else:
        parameters = ','.join(map(param_val_2_asp, g.arguments))
        return f'{name}({parameters})'


def method_req_end(method: sc.Method, maximal_goal: sc.Goal) -> str:
    name = method.name
    s = 'method_req_end('
    if len(method.params) == 0:
        s += f'{name}'
    else:
        parameters = ','.join(map(param_val_2_asp, method.params))
        s += f'{name}({parameters})'

    s += ', ' + goal(maximal_goal) + ')'

    if len(method.params) > 0:
        s += f':-{vars_to_asp(method.params)}'

    return s


def goal_DNF(g: sc.Goal, l: sc.Literal) -> str:
    s = 'goal_DNF(' + goal(g) + ', ' + literal(l) + ')'
    variables = [v for v in g.arguments if isinstance(v, sc.Variable)]
    if len(variables) > 0:
        s += f':-{vars_to_asp(variables)}'
    return s
    
def goal_def(g: sc.Goal) -> str:
    variables = [v for v in g.arguments if isinstance(v, sc.Variable)]
    s = 'goal(' + goal(g) + ')'
    if len(variables) > 0:
        s += f':-{vars_to_asp(variables)}'
    return s


def goal_to_sat(g: sc.Goal) -> str:
    return 'goal_to_sat(' + goal(g) + ', 0, 0)'


def prec_to_sat(prec: sc.Goal, succ: sc.Goal) -> str:
    return 'prec_to_sat(' + goal(prec) + ', 0,' + goal(succ) + ', 0)'


def independent_rules() -> List[str]:

    return [
        "#program step(t)",
        "%creation of new subgoals",
        "goal_to_sat(G, t+1, t+1):-occurs(M, t), method_req(M, G, G2), goal(G)",
        "goal_to_sat(G, t+1, t+1):-occurs(M, t), method_req_end(M, G), goal(G)",
        "prec_to_sat(G1, t+1, G2, t+1):-occurs(M, t), method_req(M, G1, G2)",

        "%definition of minimal goal",
        "not_minimal(G2, T2, t):-prec_to_sat(G1, T1, G2, T2), goal_to_sat(G1,T1,t), goal_to_sat(G2, T2, t)",
        "not_minimal(G2, T2, t):-goal_to_sat(G1,T1,t), goal_to_sat(G2, T2, t), T2<T1",

        "minimal(G, T1, t):-goal_to_sat(G, T1, t), not not_minimal(G, T1, t)",

        "0{selected_sub_goal(G, T1, t):minimal(G, T1, t)}1",

        "%executability for methods:",
        "not_executable(M, t):-method_exec(M,F), fluent(F), not holds(F,t)",
        "not_executable(M, t):-method_exec(M,F), opposite(F, NOTF), holds(NOTF,t)",

        "not_relevant(M,t):-method(M), goal_DNF(MG,F), method_req_end(M, MG), selected_sub_goal(SG, ST, t), goal_DNF(SG, NOTF), opposite(F,NOTF)",
        "relevant(M,t):-method(M), selected_sub_goal(SG, ST, t), goal_DNF(SG, F), method_req_end(M, MG), goal_DNF(MG, F), not not_relevant(M,t)",
        "executable(M,t):-method(M), not not_executable(M,t), relevant(M,t)",
        ":- not executable(M,t), occurs(M,t), method(M)",

        "%executability for actions:",
        "not_executable(A,t):-action_exec(A,F), fluent(F), not holds(F,t)",
        "not_executable(A,t):-action_exec(A,NOTF), opposite(F, NOTF), holds(F,t)",

        "not_relevant(A,t):-action(A), selected_sub_goal(SG, ST, t), goal_DNF(SG, NOTF), causes(A,F), opposite(F, NOTF)",
        "relevant(A,t):-action(A), selected_sub_goal(SG, ST, t), goal_DNF(SG, F), causes(A,F), not not_relevant(A,t)",
        "executable(A, t):-action(A), not not_executable(A, t), relevant(A, t)",
        ":- not executable(A, t), occurs(A, t), action(A)",

        "%inertia for fluents:",
        "holds(F, t+1):-holds(F, t), opposite(F, G), not holds(G, t+1)",

        "%opposite definition",
        "opposite(F, neg(F)):-fluent(F)",
        "opposite(neg(F), F):-fluent(F)",

        "%at most one action/method at a time:",
        "{occurs(A,t):action(A)}",
        "{occurs(M,t):method(M)}",
        ":-occurs(A,t), occurs(M,t), A!=M",

        "%action effects:",
        "holds(F, t+1):-action(A), occurs(A,t), causes(A,F)",

        "%inertia for subgoals",
        "action_occurs(t):-occurs(A,t), action(A)",

        "not_sat(G, t+1):-goal_DNF(G, F), holds(NOTF, t+1), opposite(NOTF ,F), goal(G)",
        "not_sat(G, t+1):-goal_DNF(G, F), fluent(F), not holds(F, t+1), goal(G)",

        "goal_to_sat(G, T1, t+1):- goal_to_sat(G, T1, t), not action_occurs(t)",
        "goal_to_sat(G, T1, t+1):- not_sat(G, t+1), goal_to_sat(G, T1, t), action_occurs(t)",
        "#program check(t)",
        ":- goal_to_sat(G, T, t), query(t)"
    ]

def compile_HGN_into_asp(problem: sc.ClassicalPlanningProblem) -> str:


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
            elif t.is_struct_type():
                type_asp_convertion.append(f"{t.name}({struct_values(t)})")
                

    s += to_asp_lines(type_asp_convertion)

    s += title_section('FLUENTS')

    fluent_asp = []
    for fluent in problem.fluents:
        fluent_asp.append(fluent_2_asp(fluent))

    s += to_asp_lines(fluent_asp)
    
    s += title_section('INITIALLY')

    init_values = []
    for lit in problem.init_values:
        init_values.append("holds(" + literal(lit) + ", 0)")

    s += to_asp_lines(init_values)

    s += title_section('ACTIONS')

    actions = []
    for action in problem.actions:
        actions.append(action_to_asp(action))

    s += to_asp_lines(actions)

    s += title_section('EXECUTABLE')

    executabilities = []

    for action in problem.actions:
        for precond in action.precondition:
            executabilities.append(operation_exec(action, precond))

    s += to_asp_lines(executabilities)

    s += title_section('CAUSES')

    causes = []
    for action in problem.actions:
        for effect in action.effects:
            causes.append(action_causes(action, effect))

    s += to_asp_lines(causes)

    s += title_section('METHODS')

    methods = []
    for method in problem.methods:
        methods.append(method_to_asp(method))

    s += to_asp_lines(methods)

    s += title_section('EXECUTABLE')

    executabilities = []

    for method in problem.methods:
        for precond in method.precondition:
            executabilities.append(operation_exec(method, precond))

    s += to_asp_lines(executabilities)

    s += title_section('METHOD_GOAL_REFINEMENT')

    method_goal_refinement = []

    for method in problem.methods:
        for prec, succ in method.goal_poset.get_precedence_relations():
            method_goal_refinement.append(method_req(method, prec, succ))
        for maximal_goal in method.goal_poset.get_maximal_goals():
            method_goal_refinement.append(method_req_end(method, maximal_goal))
    s += to_asp_lines(method_goal_refinement)

    s += title_section('GOAL DNF')

    goal_dnf = []
    for g in problem.goals:
        for l in g.literals:
            goal_dnf.append(goal_DNF(g, l))

    s += to_asp_lines(goal_dnf)

    s += title_section('GOAL')

    goals = []
    for g in problem.goals:
        goals.append(goal_def(g))

    s += to_asp_lines(goals)

    s += title_section('GOAL TO SAT')

    init_poset = []
    initial_poset = problem.initial_poset
    for prec, succ in initial_poset.get_precedence_relations():
        init_poset.append(prec_to_sat(prec, succ))
    for maximal_goal in initial_poset.get_maximal_goals():
        init_poset.append(goal_to_sat(maximal_goal))

    s += to_asp_lines(init_poset)
    
    print(s + to_asp_lines(independent_rules()))

    return s + to_asp_lines(independent_rules())