"""Test definition of the problem and its subcomponents"""
import unittest
import os
import sys


current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, os.path.join(current_dir, "..", "model"))

sys.path.insert(1, os.path.join(current_dir, "..", "engines", 'answer_set_planning'))
from asp_engine import *

from ftype import IntType, BoolType, EnumType, StructType, Type
from goal import Goal, Poset
from method import Method
from fluent import Fluent
from variable import Variable
from action import IAction
from problem import HierarchicalGoalNetworkProblem
from asp_engine import solve

class TestGoalAndMethods(unittest.TestCase):

    def setUp(self):
        
        self.color  = EnumType("table", ["table1", "table2", "table3"])
        self.TABLE = Variable('TABLE', self.color)
        
        self.loaded = Fluent("loaded", self.color)
        self.moved  = Fluent("moved", self.color)
        self.ready  = Fluent("ready", self.color)

        self.goal_picked = Goal("picked_g", [self.TABLE], [-self.loaded(self.TABLE)])
        self.goal_moved  = Goal("moved_g", [self.TABLE], [self.moved(self.TABLE)])
        self.goal_placed = Goal("placed_g", [self.TABLE], [self.loaded(self.TABLE),
                                                        self.ready(self.TABLE)])
        self.goal_ready  = Goal("ready_g", [self.TABLE], [self.ready(self.TABLE)])

        self.poset = Poset([self.goal_picked, self.goal_moved, self.goal_placed])
        
        self.lighten_up = Method(name='lighten_up',
                                 params=[self.TABLE],
                                 precondition=[self.loaded(self.TABLE)],
                                 goal_poset=self.poset)

        self.pick = IAction('pick', params=[self.TABLE], precondition=[self.loaded(self.TABLE)],
                            effects=[-self.loaded(self.TABLE)])

        self.move = IAction('move', params=[self.TABLE], precondition=[-self.loaded(self.TABLE)],
                            effects=[self.moved(self.TABLE)])

        self.place = IAction('place', params=[self.TABLE], precondition=[-self.loaded(self.TABLE)],
                             effects=[self.loaded(self.TABLE), self.ready(self.TABLE)])


        self.hgnp = HierarchicalGoalNetworkProblem()

        self.hgnp.add_type(self.color)

        self.hgnp.add_variable(self.TABLE)

        self.hgnp.add_fluent(self.loaded)
        self.hgnp.add_fluent(self.moved)
        self.hgnp.add_fluent(self.ready)

        self.hgnp.add_method(self.lighten_up)

        self.hgnp.add_action(self.pick)
        self.hgnp.add_action(self.move)
        self.hgnp.add_action(self.place)


        self.hgnp.add_goal(self.goal_moved)
        self.hgnp.add_goal(self.goal_placed)
        self.hgnp.add_goal(self.goal_ready)
        self.hgnp.add_goal(self.goal_picked)
        
        self.hgnp.add_poset(Poset([Goal("ready_g", ["table1"], [self.ready("table1")])]))

        self.hgnp.add_initial_values(self.loaded("table1"), self.loaded("table2"))

        print(self.hgnp)
        #finally_holds, plan = solve(p)

    def test_solution(self):
        solve(self.hgnp)
if __name__ == "__main__":
    unittest.main()
