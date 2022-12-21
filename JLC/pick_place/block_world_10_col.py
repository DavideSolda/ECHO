import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, os.path.join(current_dir, "..", "..", "model"))
from shortcuts import *

sys.path.insert(1, os.path.join(current_dir, "..", "..", "engines", 'answer_set_planning'))
from asp_engine import *

stack = IntType("stack", 1, 3)
color = EnumType("color", ["red", "orange", "yellow", "black", "violet", "brown", "white",
                           "green", "blue", "gray"])
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
                effects = [-free_stack(S), top(C1), free_gripper(), -gripped(C1), on_stack(C1, S)])


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
p.add_action(pick_from_ground)
#add initial values:
#"red", "orange", "yellow", "black",
#"violet", "brown", "white", "green",
#"blue", "gray"
p.add_initial_values(on_stack('red', 1))
p.add_initial_values(on_block('orange', 'red'))
p.add_initial_values(on_block('yellow', 'orange'))
p.add_initial_values(on_block('black', 'yellow'))
p.add_initial_values(top('black'))

p.add_initial_values(on_stack('violet', 2))
p.add_initial_values(on_block('brown', 'violet'))
p.add_initial_values(on_block('white', 'brown'))
p.add_initial_values(on_block('green', 'white'))
p.add_initial_values(top('green'))

p.add_initial_values(free_gripper())

#p.add_initial_values(free_stack(3))
p.add_initial_values(on_stack('blue', 3))
p.add_initial_values(on_block('gray', 'blue'))
p.add_initial_values(top('gray'))

#add goals:
#p.add_goals(on_block('green', 'black'))
p.add_goals(on_block('blue', 'red'))
#p.add_goals(free_gripper())
#solve:
finally_holds, plan = solve(p)
print(f"plan of length {len(plan)}")
print(finally_holds)
print(plan)
for act in plan:
    print(act.action.name)
    print(act.var_map.values())
