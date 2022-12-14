import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, os.path.join(current_dir, "..", "model"))
from shortcuts import *

sys.path.insert(1, os.path.join(current_dir, "..", "engines", 'mae_epddl_planning'))
from epddl_engine import *


coininthebox = MEPlanningProblem()
#  types:
agents = AgentType(['a', 'b', 'c'])
#  variables:
i = Variable('i', agents)
j = Variable('j', agents)

#  fluents:
opened = Fluent('opened')
has_key = Fluent('has_key', agents)
looking = Fluent('looking', agents)
tail = Fluent('tail')

act_open = MEAction('open',
                      params = [i],
                      precondition=[B([i], has_key(i))],
                      effects=[opened()],
                      full_obs=[Forall(j, neq=neq(j, i),
                                         when=looking(j),
                                         who=j),
                                i])

peek = MEAction('peek',
                  params = [i],
                  precondition=[B([i], opened()),
                                B([i], looking(i))],
                  effects=[tail()],
                  full_obs=[i],
                  partial_obs=[Forall(j, neq=neq(i, j),
                                        when=looking(j),
                                        who=j)],
                  type=MEActionType.sensing)


announce = MEAction('announce',
                      params = [i],
                      precondition=[B([i], tail())],
                      effects=[tail()],
                      full_obs=[Forall(j, neq=neq(j, i),
                                         when=looking(j), who=j),
                                i],
                      type=MEActionType.announcement)

coinintheboxmename = 'coininthebox'
coininthebox.add_type(agents)

coininthebox.add_variable(i)
coininthebox.add_variable(j)

coininthebox.add_fluent(opened)
coininthebox.add_fluent(has_key)
coininthebox.add_fluent(looking)
coininthebox.add_fluent(tail)

coininthebox.add_action(act_open)
coininthebox.add_action(peek)
coininthebox.add_action(announce)

coininthebox.add_initial_values(tail(),
                                   has_key('a'),
                                   looking('a'),

                                   B(['a', 'b', 'c'], has_key('a')),
                                   B(['a', 'b', 'c'], -has_key('b')),
                                   B(['a', 'b', 'c'], -has_key('c')),

                                   B(['a', 'b', 'c'], -opened()),

                                   B(['a', 'b', 'c'], looking('a')),
                                   B(['a', 'b', 'c'], -looking('b')),
                                   B(['a', 'b', 'c'], -looking('c')))

coininthebox.add_goals(B(['a'], tail()))
res = solve(coininthebox)
for action, var_inst in res:
    print(action.name, f'{var_inst}')
