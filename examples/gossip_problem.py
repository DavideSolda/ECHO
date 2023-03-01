import os
import sys

from ECHO import *

all_agents  = ['alice', 'bob', 'mario', 'giangiovanni']
agent       = AgentType(all_agents)
agent_agent = StructType("agentxagent", [agent, agent])
integer     = EnumType("integer", ['uno', 'due'])
agent_integer = StructType("agentxinteger", [agent, integer])

p  = Fluent('p', integer)
connected  = Fluent('connected', agent_agent)
sees = Fluent('sees', agent_integer)

A1 = Variable("a1", agent)
A2 = Variable("a2", agent)
V  = Variable("v", integer)

peek_secret = MEAction('peek',
                       effects=[p('uno')],
                       full_obs=['giangiovanni'],
                       type = MEActionType.sensing)

share_secret = MEAction('share_secret',
                        params = [A1, A2, V],
                        precondition = [B([A1], p(V)), connected(A1, A2)],
                        effects=[p(V)],
                        full_obs=[A2],
                        type = MEActionType.announcement)

gossip = MEPlanningProblem()

#add types
for t in [agent, agent_agent, integer]:
    gossip.add_type(t)

#add fluents:
for f in [p, connected]:
    gossip.add_fluent(f)

#add variables:
for v in [A1, A2, V]:
    gossip.add_variable(v)

#add action:
for act in [share_secret, peek_secret]:
    gossip.add_action(act)

#add initial values:
for init in [connected('alice', 'bob'),
             connected('bob', 'mario'),
             connected('mario', 'giangiovanni'),
             connected('bob', 'giangiovanni'),
             connected('alice', 'mario'),
             connected('alice', 'giangiovanni'),
             connected('giangiovanni', 'alice'),
             p('uno'),
             B(all_agents, connected('alice', 'bob')),
             B(all_agents, connected('bob', 'mario')),
             B(all_agents, connected('mario', 'giangiovanni')),
             B(all_agents, connected('bob', 'giangiovanni')),
             B(all_agents, connected('alice', 'mario')),
             B(all_agents, connected('alice', 'giangiovanni')),
             B(all_agents, connected('giangiovanni', 'alice'))
             ]:
    gossip.add_initial_values(init)

#add goals:
for goal in [B(['bob'], p('uno'))]:
    gossip.add_goals(goal)

res = solve_mae(gossip)
