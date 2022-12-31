import os
import sys

from ECHO import *

stack = IntType("stak", 1, 3)
color = EnumType("color", ["red", "orange", "yellow", "black"])
color_pair = StructType("colorxcolor", [color, color])
color_stack = StructType("colorxstack", [color, stack])

on_block     = Fluent("on_block", color_pair)
on_stack     = Fluent("on_stack", color_stack)
top          = Fluent("top_block", color)
gripped      = Fluent("gripped", color)
free_gripper = Fluent("free_gripper")
free_stack   = Fluent("free_stack", stack)

C1 = Variable("C1", color)
C2 = Variable("C2", color)
S  = Variable("S", stack)

pick = IAction(name = "pick",
               params = [C1, C2],
               precondition = [top(C1), on_block(C1, C2), free_gripper()],
               effects = [-top(C1), -on_block(C1, C2), top(C2), -free_gripper(), gripped(C1)])


pick_from_ground = IAction(name = "pick_from_ground",
                           params = [C1, S],
                           precondition = [top(C1), on_stack(C1, S), free_gripper()],
                           effects = [free_stack(S), -top(C1), -on_stack(C1, S), -free_gripper(), gripped(C1)])

place = IAction(name = "place",
                params = [C1, C2],
                precondition = [top(C2), -free_gripper(), gripped(C1)],
                effects = [top(C1), on_block(C1, C2), -top(C2), free_gripper(), -gripped(C1)])

place_on_ground = IAction(name = "place_on_ground",
                params = [C1, S],
                precondition = [free_stack(S), -free_gripper(), gripped(C1)],
                effects = [-free_stack(S), top(C1), free_gripper(), -gripped(C1)])


p = ClassicalPlanningProblem()
#add types:
p.add_type(stack)
p.add_type(color)
p.add_type(color_pair)
p.add_type(color_stack)
#add fluents:
p.add_fluent(on_block)
p.add_fluent(on_stack)
p.add_fluent(top)
p.add_fluent(gripped)
p.add_fluent(free_gripper)
p.add_fluent(free_stack)
#add variables:
p.add_variable(C1)
p.add_variable(C2)
p.add_variable(S)
#add action:
p.add_action(pick)
#p.add_action(pick_from_ground)
p.add_action(place)
p.add_action(place_on_ground)
#add initial values:
p.add_initial_values(on_stack('red', 1))
p.add_initial_values(on_block('black', 'red'))
p.add_initial_values(top('black'))
p.add_initial_values(on_stack('orange', 2))
p.add_initial_values(top('orange'))
p.add_initial_values(free_gripper())
p.add_initial_values(free_stack(3))
#add goals:
p.add_goals(on_block('black', 'orange'))
p.add_goals(free_gripper())
#solve:
finally_holds, plan = solve_classical(p)
print(f"plan of length {len(plan)}")
print(finally_holds)
print(plan)
