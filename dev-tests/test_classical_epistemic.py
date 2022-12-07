import unittest
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, os.path.join(current_dir, "..", "model"))
import shortcuts as p

sys.path.insert(1, os.path.join(current_dir, "..", "engines", 'mae_epddl_planning'))
from epddl_engine import solve

class TestSolving2Levels(unittest.TestCase):

    def setUp(self):
        #EPISTEMIC DESCRIPTION
        self.agent_type = p.EnumType('agents', ['agent_1', 'agent_2'], agent=True)
        self.position_type = p.EnumType('position', ['one', 'two', 'three'])
        self.current_pos = p.Fluent('current_position', self.position)
        



        #CLASSICALL DESCRIPTION
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
        self.classical_boolean = p.Fluent('classical_boolean')
        self.move_action.insert([- self.classical_boolean])

    def test_
