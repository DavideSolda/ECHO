"""Test definition of the problem and its subcomponents"""
import unittest
import os
import sys


current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, os.path.join(current_dir, "..", "model"))


from ftype import IntType, BoolType, EnumType, StructType, Type
from goal import Goal, Poset
from method import Method

class TestGoalAndMethods(unittest.TestCase):

    def setUp(slef):
        
        self.color  = EnumType("table", ["table1", "table2", "table3"])
        self.C = Variable('TABLE', self.color)
        
        self.loaded = Fluent("loaded", self.color)
        self.moved = Fluent("moved", self.color)
        self.moved = Fluent("ready", self.color)

        #goal definitions
        
        self.method = Method(name='lighten_up',
                             params=self.C,
                             precondition=[self.loaded(self.C)],
                             goal_poset=)

        self.s = StructType("s", [self.e, self.integer])
        self.f1 = Fluent("f1", self.s)
        self.f2 = Fluent("f1", self.s)
        self.f3 = Fluent("f3", self.e)

        self.goal = Goal('goal1', set(self.f3('red')))
        print(self.goal)

        
if __name__ == "__main__":
    unittest.main()
