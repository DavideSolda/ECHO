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
        self.integer = IntType("integer", 1, 3)
        self.enum_values = ["red", "orange", "yellow"]
        self.e = EnumType("color", self.enum_values)
        self.s = StructType("s", [self.e, self.integer])
        self.f1 = Fluent("f1", self.s)
        self.f2 = Fluent("f1", self.s)
        self.f3 = Fluent("f3", self.e)

        self.goal = Goal('goal1', set(self.f3('red')))
        print(self.goal)

        
if __name__ == "__main__":
    unittest.main()
