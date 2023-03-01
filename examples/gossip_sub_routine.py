import os
import sys
from time import time

from ECHO import *

all_agents  = ['alice', 'bob', 'mario', 'giangiovanni']
agent       = AgentType(all_agents)
agent_agent = StructType("agentxagent", [agent, agent])

connected_via_phone  = Fluent('connected_via_phone', agent_agent)

digited    = Fluent('digited', agent_agent)
calling    = Fluent('calling', agent_agent)
closed     = Fluent('closed', agent_agent)

phisically_connected = Fluent('phisically_connected', agent_agent)

R1 = Variable("R1", agent)
R2 = Variable("R2", agent)


digit = IAction(name = "digit",
                params = [R1, R2],
                precondition = [connected_via_phone(R1, R2)],
                effects = [digited(R1, R2)])

call = IAction(name = "call",
               params = [R1, R2],
               precondition = [connected_via_phone(R1, R2), digited(R1, R2)],
               effects = [-digited(R1, R2), calling(R1, R2)])

close = IAction(name = "close",
               params = [R1, R2],
               precondition = [connected_via_phone(R1, R2), calling(R1, R2)],
               effects = [-calling(R1, R2), closed(R1, R2)])

communicate_g = Goal('communicated', [R1, R2], [closed(R1, R2)])
digited_g     = Goal('digited_g', [R1, R2], [digited(R1, R2)])
calling_g     = Goal('calling_g', [R1, R2], [calling(R1, R2)])


communicate_via_phone = Method('communicate_via_phone',
                               [R1, R2],
                               [connected_via_phone(R1, R2)],
                               Poset([digited_g,
                                      calling_g,
                                      communicate_g])
                               )


#TRY:
# 0) to see if it works properly. It seems.
# 1) try classicaly and goal-network based.
# 1) add dummy actions. 
# 2) different communications

p = HierarchicalGoalNetworkProblem()
#add types:
p.add_type(agent)
p.add_type(agent_agent)
#add fluents:
p.add_fluent(connected_via_phone)
p.add_fluent(digited)
p.add_fluent(calling)
p.add_fluent(closed)
#add variables:
p.add_variable(R1)
p.add_variable(R2)
#add action:
p.add_action(digit)
p.add_action(call)
p.add_action(close)
#add initial values:
p.add_initial_values(connected_via_phone('alice', 'bob'))
p.add_initial_values(connected_via_phone('alice', 'mario'))
p.add_initial_values(connected_via_phone('mario', 'giangiovanni'))
#add initial poset:
p.add_method(communicate_via_phone)
#add goals:
p.add_goal(communicate_g)
p.add_goal(digited_g)
p.add_goal(calling_g)

#add poset goal:
p.add_poset(Poset([Goal("communicated", ["alice", "bob"], [closed("alice", "bob")]),
                   Goal("communicated", ["alice", "mario"], [closed("alice", "mario")])
                   ]))

#SOLVE:
t = time()
fin_holds, plan = solve_classical(p)
hgn = time()-t
for action in plan:
    print(action)
    print()


#CLASSICAL VERSION
c = ClassicalPlanningProblem()
#add types:
c.add_type(agent)
c.add_type(agent_agent)
#add fluents:
c.add_fluent(connected_via_phone)
c.add_fluent(digited)
c.add_fluent(calling)
c.add_fluent(closed)
#add variables:
c.add_variable(R1)
c.add_variable(R2)
#add action:
c.add_action(digit)
c.add_action(call)
c.add_action(close)
#add initial values:
c.add_initial_values(connected_via_phone('alice', 'bob'))
c.add_initial_values(connected_via_phone('alice', 'mario'))
c.add_initial_values(connected_via_phone('mario', 'giangiovanni'))

#add poset goal:
c.add_goals(closed("alice", "bob"),
            closed("alice", "mario"))

#SOLVE:
t = time()
fin_holds, plan = solve_classical(c)
classical = time() - t
for action in plan:
    print(action)
    print()

print(f"Goal network: {hgn}")
print(f"Classical: {classical}")

quit()
#TRY to compute the differnt solving times adding dummy actions
color       = EnumType('color', ['red', 'black', 'gray', 'red', 'violet'])
color_color = StructType("colorxcolor", [color, color])
C1 = Variable("C1", color)
C2 = Variable("C2", color)
p.add_type(color)
p.add_type(color_color)
p.add_variable(C1)
p.add_variable(C2)
c.add_type(color)
c.add_type(color_color)
c.add_variable(C1)
c.add_variable(C2)

#cc  = Fluent('cc', color_color)


for act_name in range(1, 60):
    name = 'a_' + str(act_name)
    dummy = IAction(name = name,
                    params = [R1, R2],
                    precondition = [connected_via_phone(R1, R2)],
                    effects = [digited(R1, R2)])

    c.add_action(dummy)
    p.add_action(dummy)

#SOLVE:
t = time()
fin_holds, plan = solve_classical(p)
hgn = time()-t

t = time()
fin_holds, plan = solve_classical(c)
classical = time() - t

print(f"Goal network: {hgn}")
print(f"Classical: {classical}")
