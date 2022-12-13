import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, os.path.join(current_dir, "..", "model"))
from shortcuts import *

sys.path.insert(1, os.path.join(current_dir, "..", "engines", 'answer_set_planning'))
from asp_engine import *


coinintheboxmep = p.MEPlanningProblem()
#  types:
agents = p.AgentType(['a', 'b', 'c'])
#  variables:
i = p.Variable('i', agents)
j = p.Variable('j', agents)

#  fluents:
opened = p.Fluent('opened')
has_key = p.Fluent('has_key', agents)
looking = p.Fluent('looking', agents)
tail = p.Fluent('tail')

act_open = p.MEAction('open',
                      params = [i],
                      precondition=[p.B([i], has_key(i))],
                      effects=[opened()],
                      full_obs=[p.Forall(j, neq=p.neq(j, i),
                                         when=looking(j),
                                         who=j),
                                i])


peek = p.MEAction('peek',
                  params = [i],
                  precondition=[p.B([i], opened()),
                                p.B([i], looking(i))],
                  effects=[tail()],
                  full_obs=[i],
                  partial_obs=[p.Forall(j, neq=p.neq(i, j),
                                        when=looking(j),
                                        who=j)],
                  type=p.MEActionType.sensing)


distract = p.MEAction('distract',
                      params = [ag, ag2],
                      precondition=[p.B([ag], looking(ag)),
                                    p.B([ag2], looking(ag2))],
                      effects=[-looking(ag2)],
                      full_obs=[p.Forall(ag3, neq=p.neq(ag2, ag3),
                                         when=looking(ag3), who=ag3),
                                ag2],
                      type=p.MEActionType.announcement)
coinintheboxmep.name = 'coininthebox'
coinintheboxmep.add_type(agents)
coinintheboxmep.add_variable(ag)
coinintheboxmep.add_variable(ag2)
coinintheboxmep.add_variable(ag3)
coinintheboxmep.add_fluent(opened)
coinintheboxmep.add_fluent(has_key)
coinintheboxmep.add_fluent(looking)
coinintheboxmep.add_fluent(tail)
coinintheboxmep.add_action(move_to_box)
coinintheboxmep.add_action(move_to_empty)
coinintheboxmep.add_action(_open)
coinintheboxmep.add_action(peek)
coinintheboxmep.add_action(signal)
coinintheboxmep.add_action(distract)

coinintheboxmep.add_initial_values(in_room_empty('a'),
                                   in_room_empty('b'),
                                   in_room_empty('c'),
                                   tail(),
                                   has_key('a'),
                                   looking('a'),
                                   p.B(['a', 'b', 'c'], has_key('a')),
                                   p.B(['a', 'b', 'c'], has_key('a')),
                                   p.B(['a', 'b', 'c'], -has_key('b')),
                                   p.B(['a', 'b', 'c'], -has_key('c')),
                                   p.B(['a', 'b', 'c'], -opened()),
                                   p.B(['a', 'b', 'c'], looking('a')),
                                   p.B(['a', 'b', 'c'], -looking('b')),
                                   p.B(['a', 'b', 'c'], -looking('c')),
                                   p.B(['a', 'b', 'c'], in_room_empty('a')),
                                   p.B(['a', 'b', 'c'], in_room_empty('b')),
                                   p.B(['a', 'b', 'c'], in_room_empty('c')),
                                   p.B(['a', 'b', 'c'], -in_room_box('a')),
                                   p.B(['a', 'b', 'c'], -in_room_box('b')),
                                   p.B(['a', 'b', 'c'], -in_room_box('c')))
coinintheboxmep.add_goals(p.B(['a'], opened()))
res = solve(coinintheboxmep)
for action, var_inst in res:
    print(action.name, f'{var_inst}')
