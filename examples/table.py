import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, os.path.join(current_dir, "..", "model"))
from shortcuts import *

sys.path.insert(1, os.path.join(current_dir, "..", "engines", 'answer_set_planning'))
from asp_engine import *

color  = EnumType("table", ["table1", "table2", "table3"])
TABLE = Variable('TABLE', color)
        
loaded = Fluent("loaded", color)
moved  = Fluent("moved", color)
ready  = Fluent("ready", color)

goal_picked = Goal("picked_g", [TABLE], [-loaded(TABLE)])
goal_moved  = Goal("moved_g", [TABLE], [moved(TABLE)])
goal_placed = Goal("placed_g", [TABLE], [loaded(TABLE),
ready(TABLE)])
goal_ready  = Goal("ready_g", [TABLE], [ready(TABLE)])

poset = Poset([goal_picked, goal_moved, goal_placed])

lighten_up = Method(name='lighten_up',
 params=[TABLE],
 precondition=[loaded(TABLE)],
 goal_poset=poset)

pick = IAction('pick', params=[TABLE], precondition=[loaded(TABLE)],
    effects=[-loaded(TABLE)])

move = IAction('move', params=[TABLE], precondition=[-loaded(TABLE)],
    effects=[moved(TABLE)])

place = IAction('place', params=[TABLE], precondition=[-loaded(TABLE)],
     effects=[loaded(TABLE), ready(TABLE)])


hgnp = HierarchicalGoalNetworkProblem()

hgnp.add_type(color)

hgnp.add_variable(TABLE)

hgnp.add_fluent(loaded)
hgnp.add_fluent(moved)
hgnp.add_fluent(ready)

hgnp.add_method(lighten_up)

hgnp.add_action(pick)
hgnp.add_action(move)
hgnp.add_action(place)


hgnp.add_goal(goal_moved)
hgnp.add_goal(goal_placed)
hgnp.add_goal(goal_ready)
hgnp.add_goal(goal_picked)

hgnp.add_poset(Poset([Goal("ready_g", ["table1"], [ready("table1")]), Goal("ready_g", ["table2"], [ready("table2")])]))

hgnp.add_initial_values(loaded("table1"), loaded("table2"))

print(hgnp)
finally_holds, plan = solve(hgnp)
print(f"plan of length {len(plan)}")
for inst_action in plan:
    print(inst_action.action.name)
