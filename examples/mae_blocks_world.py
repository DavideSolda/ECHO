import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, os.path.join(current_dir, "..", "model"))
from shortcuts import *

sys.path.insert(1, os.path.join(current_dir, "..", "engines", 'answer_set_planning'))
import asp_engine

stack = IntType("stack", 1, 3)
color = EnumType("color", ["red", "orange", "yellow", "black"])
agent = AgentType(['alice', 'bob'])

color_pair = StructType("colorxcolor", [color, color])
color_stack = StructType("colorxstack", [color, stack])
agent_color = StructType("agentxcolor", [agent, color])

on_block     = Fluent("on_block", color_pair)
on_stack     = Fluent("on_stack", color_stack)
top          = Fluent("top_block", color)
gripped      = Fluent("gripped", agent_color)
free_gripper = Fluent("free_gripper", agent)
free_stack   = Fluent("free_stack", stack)
owner        = Fluent("owner", agent_color)
free_table   = Fluent("free_table")
on_table     = Fluent("table", color)

C1 = Variable("C1", color)
C2 = Variable("C2", color)
S  = Variable("S", stack)
A1 = Variable("a1", agent)
A2 = Variable("a2", agent)
R  = Variable("R", agent)

pick = IAction(name = "pick",
               params = [R, C1, C2],
               precondition = [top(C1), on_block(C1, C2), free_gripper(R), owner(R, C1)],
               effects = [-top(C1), -on_block(C1, C2), top(C2), -free_gripper(R), gripped(R, C1)])


pick_from_ground = IAction(name = "pick_from_ground",
                           params = [R, C1, S],
                           precondition = [top(C1), on_stack(C1, S), free_gripper(R), owner(R, C1)],
                           effects = [free_stack(S), -top(C1), -on_stack(C1, S), -free_gripper(R), gripped(R, C1)])

pick_from_table = IAction(name = "pick_from_table",
                          params = [R, C1],
                          precondition = [on_table(C1), -free_table(), free_gripper(R)],
                          effects = [-on_table(C1), free_table(), -free_gripper(R), gripped(R, C1), owner(R, C1)])

place = IAction(name = "place",
                params = [R, C1, C2],
                precondition = [top(C2), -free_gripper(R), gripped(R, C1), owner(R, C1)],
                effects = [top(C1), on_block(C1, C2), -top(C2), free_gripper(R), -gripped(R, C1)])

place_on_ground = IAction(name = "place_on_ground",
                params = [R, C1, S],
                precondition = [free_stack(S), -free_gripper(R), gripped(R, C1), owner(R, C1)],
                effects = [-free_stack(S), top(C1), free_gripper(R), -gripped(R, C1)])

place_on_table = IAction(name = "place_on_table",
                         params = [R, C1],
                         precondition = [free_table(), -free_gripper(R), gripped(R, C1), owner(R, C1)],
                         effects = [-free_table(), -owner(R, C1), on_table(C1), free_gripper(R), -gripped(R, C1)])

p = ClassicalPlanningProblem()
#add types:
p.add_type(agent)
p.add_type(stack)
p.add_type(color)
p.add_type(color_pair)
p.add_type(color_stack)
p.add_type(agent_color)
#add fluents:
p.add_fluent(on_block)
p.add_fluent(on_stack)
p.add_fluent(top)
p.add_fluent(gripped)
p.add_fluent(free_gripper)
p.add_fluent(free_stack)
p.add_fluent(owner)
p.add_fluent(free_table)
p.add_fluent(on_table)
#add variables:
p.add_variable(C1)
p.add_variable(C2)
p.add_variable(S)
p.add_variable(R)
#add action:
p.add_action(pick)
p.add_action(pick_from_ground)

p.add_action(place)
p.add_action(place_on_ground)

p.add_action(pick_from_table)
p.add_action(place_on_table)
#add initial values:
p.add_initial_values(on_stack('red', 1))
p.add_initial_values(on_block('black', 'red'))
p.add_initial_values(top('black'))
p.add_initial_values(on_stack('orange', 2))
p.add_initial_values(top('orange'))
p.add_initial_values(free_gripper('bob'))
p.add_initial_values(free_gripper('alice'))
p.add_initial_values(free_stack(3))
p.add_initial_values(owner('bob', 'red'))
p.add_initial_values(owner('bob', 'black'))
p.add_initial_values(owner('bob', 'orange'))
p.add_initial_values(free_table())
#add goals:
p.add_goals(on_block('black', 'orange'))
p.add_goals(on_table('red'))
p.add_goals(free_gripper('bob'))
#solve:
finally_holds, plan = asp_engine.solve(p)
print(f"plan of length {len(plan)}")
print(finally_holds)
print(plan)


look_up = MEAction('look_up',
                   params = [A1, C1],
                   precondition = [B([A1], free_table())],
                   effects=[When(owner(A1, C1), owner(A1, C1))],
                   full_obs=[A1])


sys.path.insert(1, os.path.join(current_dir, "..", "engines", 'mae_epddl_planning'))
import epddl_engine

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
e.add_action(look_up)
#add initial values:
e.add_initial_values(owner('bob', 'red'))
e.add_initial_values(owner('bob', 'orange'))
e.add_initial_values(owner('bob', 'black'))
e.add_initial_values(free_table())
e.add_initial_values(B(['bob', 'alice'], owner('bob', 'red')))
e.add_initial_values(B(['bob', 'alice'], owner('bob', 'orange')))
e.add_initial_values(B(['bob', 'alice'], owner('bob', 'black')))
e.add_initial_values(B(['bob', 'alice'], free_table()))
#add goals:
e.add_goals(B(['bob', 'alice'], free_table()))

epddl_engine.solve(e)
