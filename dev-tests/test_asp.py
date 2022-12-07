import unittest
import os
import sys


current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, os.path.join(current_dir, "..", "model"))
from shortcuts import *

sys.path.insert(1, os.path.join(current_dir, "..", "engines", 'answer_set_planning'))
from asp_engine import *

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
        self.boolean_fluent = Fluent('boolean_fluent')
        self.f_bool = Fluent("f_b")

        self.x = Variable("x", self.integer)
        self.color_var = Variable("c", self.e)

        l_pre = [self.f1('red', self.x), self.f3("orange")]
        l_effect = [self.f1('yellow', self.x), - self.f1('red', self.x)]
        self.action_1 = IAction(name = "action_1", params = [self.x], precondition = l_pre, effects = l_effect)
        self.action_2 = IAction(name = "action_2", params = [], precondition = [], effects = [- self.f3("orange"), self.boolean_fluent()])

    def test_problem_2_asp(self):
        p = ClassicalPlanningProblem()
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
        p.add_action(self.action_1)
        p.add_action(self.action_2)
        #add initial values:
        p.add_initial_values(self.f1('red', 1))
        p.add_initial_values(self.f3('orange'))
        p.add_initial_values(self.f1('orange', 1 + 1))
        #add goals:
        p.add_goals(self.f1('yellow', 1))
        p.add_goals(- self.f3("orange"))

        #solve:
        finally_holds, plan = solve(p)
        print(f'plan of length {len(plan)}:\n{plan}')
        print("\n\n")
        print(f'finally the following fluents hold:\n{finally_holds}')

if __name__ == "__main__":
    unittest.main()
