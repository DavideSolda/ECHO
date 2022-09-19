import unittest
import os
import sys


current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, os.path.join(current_dir, "..", "model"))
from shortcuts import *

sys.path.insert(1, os.path.join(current_dir, "..", "engines"))
from asp_compiler import compile_into_asp 

class TestProblem2ASP(unittest.TestCase):

    def setUp(self):
        self.integer = IntType("integer", 1, 3)
        self.integer2 = IntType("integer", 2, 3)
        self.enum_values = ["red", "orange", "yellow"]
        self.e = EnumType("color", self.enum_values)
        self.s = StructType("s", [self.e, self.integer])
        self.f1 = Fluent("f1", self.s)
        self.f2 = Fluent("f1", self.s)
        self.f3 = Fluent("f3", self.e)
        self.f_bool = Fluent("f_b")

        self.x = Variable("x", self.integer)
        self.color_var = Variable("c", self.e)

        l_pre = [self.f1('red', self.x), self.f3("orange")]
        l_effect = self.f1('yellow', self.x)
        self.action = I_Action(name = "from_red_to_yellow", params = [self.x], precondition = l_pre, effects = [l_effect])

    def test_problem_2_asp(self):
        p = Problem()
        #add types:
        p.add_type(self.integer)
        p.add_type(self.e)
        p.add_type(self.s)
        #add fluents:
        p.add_fluent(self.f1)
        p.add_fluent(self.f3)
        p.add_fluent(self.f_bool)
        #add variables:
        p.add_variable(self.x)
        #add action:
        p.add_action(self.action)
        #add initial values:
        p.add_initial_values(self.f1('red', 1))
        p.add_initial_values(self.f1('orange', self.x + 1))

        compile_into_asp(p)
