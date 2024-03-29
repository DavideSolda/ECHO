""" Testing epistemic planning model generation """
import unittest
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, os.path.join(current_dir, '..', 'model'))
import shortcuts as p


class Test_epistemicPlanningProblem(unittest.TestCase):

    def setUp(self):
        self.position = p.IntType('position', 1, 3)
        self.vpos = p.Variable('P', self.position)
        self.cpos = p.Fluent('current_position', self.position)

        self.agent_names = p.EnumType('agents', ['agent_1', 'agent_2'], agent=True)
        self.vagent = p.Variable('agent', self.agent_names, agent=True)
        self.vagent2 = p.Variable('agent2', self.agent_names, agent=True)
        self.obs1 = p.ObservablePredicate(self.vagent)
        self.b_pos = p.BeliefLiteral([self.vagent], self.cpos(self.vpos))
        self.move_action = p.MEAction(name='move',
                                      precond=[self.b_pos],
                                      effects=[- self.b_pos])

    def test_obs(self):
        obs1 = p.ObservablePredicate(self.vagent)
        obs2 = p.ObservablePredicate(who=self.vagent,
                                     forall=p.neq(self.vagent, 'agent_1'))

        with self.assertRaises(Exception):
            p.ObservablePredicate(who=self.vagent,
                                  forall=p.neq('agent_2', 'agent_1'))

        obs3 = p.ObservablePredicate(who=self.vagent,
                                     forall=p.neq(self.vagent, self.vagent2))
        print(obs1)
        print(obs2)
        print(obs3)

        obs4 = p.ObservablePredicate(who=self.vagent,
                                     forall=p.neq(self.vagent, 'agent_1'),
                                     when=self.cpos(self.vpos))
        print(obs4)

    def test_beliefPredicate(self):

        b = p.BeliefLiteral([self.vagent], self.cpos(self.vpos))
        print(b)

    def test_MEAction(self):

        move_action = p.MEAction(name='move',
                                 precond=[self.b_pos],
                                 effects=[- self.b_pos])

        move_action2 = p.MEAction(name='move',
                                  precond=[self.b_pos],
                                  effects=[- self.b_pos],
                                  full_obs=[self.obs1],
                                  part_obs=[])

    def test_meproblem(self):

        meproblem = p.MEPlanningProblem()
        #  add types:
        meproblem.add_type(self.position)
        meproblem.add_type(self.agent_names)
        #  add variables:
        meproblem.add_variable(self.vpos)
        meproblem.add_variable(self.vagent)
        meproblem.add_variable(self.vagent2)
        #  add fluents:
        meproblem.add_fluent(self.cpos)
        #  add actions:
        meproblem.add_action(self.move_action)

        print(meproblem)
