import unittest
import os
import sys


current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, os.path.join(current_dir, "..", "model"))
import shortcuts as p

sys.path.insert(1, os.path.join(current_dir, "..", "engines", 'mae_epddl_planning'))
from epddl_engine import solve


class TestProblem2EPDDL(unittest.TestCase):

    def setUp(self):
        self.position = p.IntType('position', 1, 3)
        self.double_position = p.StructType('double_position', [self.position,
                                                               self.position])
        self.vpos = p.Variable('P', self.position)
        self.cpos = p.Fluent('current_position', self.position)
        self.safe = p.Fluent('safe')
        self.position_in_plain = p.Fluent('pos_in_plain', self.double_position)
        self.agent_names = p.EnumType('agent_variable', ['agent_1', 'agent_2'])
        self.vagent = p.Variable('agent', self.agent_names, agent=True)
        self.vagent2 = p.Variable('agent2', self.agent_names, agent=True)
        self.obs1 = p.ObservablePredicate(self.vagent)
        self.b_pos = p.BeliefLiteral(self.vagent, self.cpos(self.vpos))
        self.move_action = p.MEAction(name='move', params=[self.vagent],
                                      precond=[self.b_pos],
                                      effects=[- self.b_pos])

    def test_problem_1(self):

        meproblem = p.MEPlanningProblem()
        #  set domain name
        meproblem.name = 'problem_1'
        #  add types:
        meproblem.add_type(self.position)
        meproblem.add_type(self.agent_names)
        meproblem.add_type(self.double_position)
        #  add variables:
        meproblem.add_variable(self.vpos)
        meproblem.add_variable(self.vagent)
        meproblem.add_variable(self.vagent2)
        #  add fluents:
        meproblem.add_fluent(self.cpos)
        meproblem.add_fluent(self.safe)
        meproblem.add_fluent(self.position_in_plain)
        #  add actions:
        meproblem.add_action(self.move_action)

        solve(meproblem)
