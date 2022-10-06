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
        self.position = p.EnumType('position', ['one', 'two', 'three'])
        self.double_position = p.StructType('double_position', [self.position,
                                                                self.position])
        self.vpos = p.Variable('P', self.position)
        self.cpos = p.Fluent('current_position', self.position)
        self.safe = p.Fluent('safe')
        self.position_in_plain = p.Fluent('pos_in_plain', self.position)
        self.agent_names = p.EnumType('agents', ['agent_1', 'agent_2'], agent=True)
        self.vagent = p.Variable('agent', self.agent_names, agent=True)
        self.vagent2 = p.Variable('agent2', self.agent_names, agent=True)
        self.obs1 = p.ObservablePredicate(self.vagent)
        self.b_pos = p.BeliefLiteral([self.vagent], self.cpos('one'))
        self.move_action = p.MEAction(name='move',
                                      precond=[self.b_pos, self.cpos(self.vpos)],
                                      effects=[- self.b_pos],
                                      full_obs=[self.obs1])

    def test_problem_1(self):

        meproblem = p.MEPlanningProblem()
        #  set domain name
        meproblem.name = 'problem_1'
        #  add types:
        meproblem.add_type(self.position)
        meproblem.add_type(self.agent_names)
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
        #  add inits:
        meproblem.add_initial_values(self.cpos('one'))
        meproblem.add_initial_values(self.b_pos)
        #  add goals:
        meproblem.add_goals(self.cpos('two'))
        solve(meproblem)
