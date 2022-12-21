import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, os.path.join(current_dir, "..", "..", "..", "model"))
sys.path.insert(1, os.path.join(current_dir, "..", "..", "..", "engines", 'epicla_planning'))

from shortcuts import *
import epicla_engine

stack = IntType("stack", 1, 6)
agent = AgentType(['alice', 'bob'])
color = EnumType("color", ["red", "orange"])

color_pair = StructType("colorxcolor", [color, color])
color_stack = StructType("colorxstack", [color, stack])
agent_color = StructType("agentxcolor", [agent, color])
agent_stack = StructType("agentxstack", [agent, stack])

on_block     = Fluent("on_block", color_pair)
on_stack     = Fluent("on_stack", color_stack)
top          = Fluent("top_block", color)
gripped      = Fluent("gripped", agent_color)
free_gripper = Fluent("free_gripper", agent)
free_stack   = Fluent("free_stack", stack)
owner        = Fluent("owner", agent_color)
free_table   = Fluent("free_table")
on_table     = Fluent("table", color)
in_front_of  = Fluent("in_front_of", agent_stack)

C1 = Variable("C1", color)
C2 = Variable("C2", color)
C3 = Variable("C3", color)
S  = Variable("S", stack)
A1 = Variable("a1", agent)
A2 = Variable("a2", agent)
R  = Variable("R", agent)

def run(color: EnumType, initially: List[Literal],
        epistemic_initially: List[Predicate], goals:List[Predicate], macro: bool) -> None:

    pick = IAction(name = "pick",
                   params = [R, C1, C2],
                   precondition = [top(C1), on_block(C1, C2), free_gripper(R), owner(R, C1)],
                   effects = [-top(C1), -on_block(C1, C2), top(C2), -free_gripper(R), gripped(R, C1)])


    pick_from_ground = IAction(name = "pick_from_ground",
                               params = [R, C1, S],
                               precondition = [in_front_of(R, S), top(C1), on_stack(C1, S), free_gripper(R), owner(R, C1)],
                               effects = [free_stack(S), -top(C1), -on_stack(C1, S), -free_gripper(R), gripped(R, C1)])

    pick_from_table = IAction(name = "pick_from_table",
                              params = [R, C1],
                              precondition = [on_table(C1), -free_table(), free_gripper(R)],
                              effects = [-on_table(C1), free_table(), -free_gripper(R), gripped(R, C1), owner(R, C1)])

    place = IAction(name = "place",
                    params = [R, C1, C2],
                    precondition = [top(C2), -free_gripper(R), gripped(R, C1), owner(R, C1), owner(R, C2)],
                    effects = [top(C1), on_block(C1, C2), -top(C2), free_gripper(R), -gripped(R, C1)])

    place_on_ground = IAction(name = "place_on_ground",
                              params = [R, C1, S],
                              precondition = [free_stack(S), -free_gripper(R), gripped(R, C1), owner(R, C1), in_front_of(R, S)],
                              effects = [-free_stack(S), top(C1), free_gripper(R), -gripped(R, C1)])

    place_on_table = IAction(name = "place_on_table",
                         params = [R, C1],
                             precondition = [free_table(), -free_gripper(R), gripped(R, C1), owner(R, C1)],
                             effects = [-free_table(), -owner(R, C1), on_table(C1), free_gripper(R), -gripped(R, C1)])

    top_g      = Goal('top_g', [C1], [top(C1)])
    picked_g   = Goal('picked_g', [R, C1], [gripped(R, C1)])
    on_g       = Goal('on_g', [C1, C2], [on_block(C1, C2)])
    on_table_g = Goal('on_table_g', [C1], [on_table(C1)])
    on_stack_g = Goal('on_stack_g', [C1, S], [on_stack(C1, S)])

    move_to_top = Method('move_to_top',
                     [R, C1, C2, C3],
                     [on_block(C1, C2), top(C3), neq(C3, C2)],
                     Poset([top_g([C1]),
                            picked_g([R, C1]),
                            on_g([C1, C3]),
                            picked_g([R, C2])])
                     )

    move_to_ground = Method('move_to_ground',
                        [R, C1, C2, S],
                        [on_block(C1, C2), free_stack(S)],
                        Poset([top_g([C1]),
                               picked_g([R, C1]),
                               on_stack_g([C1, S]),
                               picked_g([R, C2])]
                        ))

    p = HierarchicalGoalNetworkProblem()
    #add types:
    for t in [agent, stack, color, color_pair, color_stack, agent_color, agent_stack]:
        p.add_type(t)

    #add fluents:
    for f in [on_block, on_stack, top, gripped, free_gripper,
              free_stack, owner, free_table, on_table, in_front_of]:
        p.add_fluent(f)

    #add variables:
    for v in [C1, C2, S, R]:
        p.add_variable(v)

    #add action:

    for act in [pick, pick_from_ground, place, place_on_ground, pick_from_table, place_on_table]:
        p.add_action(act)

    #add initial values:
    p.add_initial_values(*initially)    

    #add goals:
    for goal in [top_g, picked_g, on_g, on_table_g, on_stack_g]:
        p.add_goal(goal)

    #add methods:
    for method in [move_to_top, move_to_ground]:
        p.add_method(method)

    #Macro definition:
    pick_from_stack_place_on_table_ann = MEAction('announcepickfromstackplaceontablemacro',
                                                  params = [A1, C1],
                                                  precondition = [owner(A1, C1), free_table(),
                                                                  B([A1], owner(A1, C1))],
                                                  effects=[-owner(A1, C1), on_table(C1), -free_table()],
                                                  full_obs=[Forall(A2, who=A2)])

    pt = Poset([picked_g([A1, C1]), on_table_g([C1])])

    pick_from_stack_place_on_table_ann.classical_sub_goals(pt)

    pick_from_table_place_on_stack_ann = MEAction('announcepickfromtableplaceonstackmacro',
                                                  params = [A1, C1],
                                                  precondition = [-owner(A1, C1), -free_table(),
                                                                  on_table(C1), B([A1], on_table(C1))],
                                                  effects=[owner(A1, C1), -on_table(C1), free_table()],
                                                  full_obs=[Forall(A2, who=A2)])

    tp = Poset([picked_g([A1, C1]), top_g([C1])])
    pick_from_table_place_on_stack_ann.classical_sub_goals(tp)
    
    #Sensing action to collect info:
    look_up = MEAction('lookup',
                       type = MEActionType.sensing,
                       params = [A1, C1],
                       precondition = [],
                       effects=[When(owner(A1, C1), owner(A1, C1))],
                       full_obs=[A1])

    #ontic actions to move blocks:
    pick_from_table_place_on_stack = MEAction('pickfromtableplaceonstack',
                                              params = [A1, C1],
                                              precondition = [-free_table(), -owner(A1, C1), -free_table(),
                                                              on_table(C1), B([A1], on_table(C1))],
                                              effects=[owner(A1, C1), -on_table(C1), free_table()],
                                              full_obs=[A1])

    pick_from_table_place_on_stack.classical_sub_goals(tp)
    pick_from_stack_place_on_table = MEAction('pickfromstackplaceontable',
                                              params = [A1, C1],
                                              precondition = [owner(A1, C1), free_table(),
                                                              B([A1], free_table()),
                                                              B([A1], owner(A1, C1))],
                                              effects=[-owner(A1, C1), on_table(C1), -free_table()],
                                              full_obs=[A1])
    pick_from_stack_place_on_table.classical_sub_goals(pt)
    #annoucements:
    announce_on_table = MEAction('announceontable',
                                 type = MEActionType.announcement,
                                 params = [A1, C1],
                                 precondition = [on_table(C1), B([A1], on_table(C1))],
                                 effects=[-owner(A1, C1), on_table(C1), -free_table()],
                                 full_obs=[Forall(A2, who=A2)])

    announce_free_table = MEAction('announcefreetable',
                                 type = MEActionType.announcement,
                                 params = [A1],
                                 precondition = [free_table(), B([A1], free_table())],
                                 effects=[free_table()],
                                 full_obs=[Forall(A2, who=A2)])

    
    e = MEPlanningProblem()

    #add types:
    e.add_type(agent)
    e.add_type(color)
    e.add_type(agent_color)

    #add fluents:
    e.add_fluent(owner)
    e.add_fluent(free_table)
    e.add_fluent(on_table)

    #add variables:
    e.add_variable(C1)
    e.add_variable(A1)
    e.add_variable(A2)

    #add action:
    for act in [look_up,
                pick_from_table_place_on_stack, pick_from_stack_place_on_table,
                announce_on_table, announce_free_table]:
        e.add_action(act)

    #add macro:
    if macro:
        for act in [pick_from_stack_place_on_table_ann, pick_from_table_place_on_stack_ann]:
            e.add_action(act)

    
    #add initial values:
    e.add_initial_values(*epistemic_initially)

    #add goals:
    for goal in goals:
        e.add_goals(goal)
    
    epicla = EpiCla(p, e)
    
    
    epicla_plan = epicla_engine.solve(epicla)
    print('epicla_plan')
    pretty_print_epica_plan(epicla_plan)        
    
