"""Test definition of the problem and its subcomponents"""
import unittest
import os
import sys


current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, os.path.join(current_dir, "..", "model"))


from ftype import IntType, BoolType, EnumType, StructType, Type


class TestFTypeModule(unittest.TestCase):

    """Test ftype.Type"""
    def setUp(self):

        self.integer = IntType("integer", 1, 3)
        self.b = BoolType("b")
        self.enum_values = ["red", "orange", "yellow"]
        self.enum_values_subset = ['red']
        self.e = EnumType("color", self.enum_values)
        self.e2 = EnumType("color2", self.enum_values_subset)
        self.s = StructType("s", [self.e, self.integer])

    def test_is_bool_type(self):
        """test is_bool_type method"""
        self.assertTrue(self.b.is_bool_type())
        self.assertFalse(self.integer.is_bool_type())

    def test_is_int_type(self):
        """test is_int_type method"""
        self.assertTrue(self.integer.is_int_type())
        self.assertFalse(self.e.is_int_type())

    def test_is_enum_type(self):
        """test is_enum_type method"""
        self.assertTrue(self.e.is_enum_type())

    def test_is_struct_type(self):
        """test is_struct_type method"""
        self.assertTrue(self.s.is_struct_type())

    def test_int_interval(self):
        """test equal operator intervals"""
        self.assertTrue(self.integer.interval == (1, 3))

    def test_enum_iter(self):
        """test iterate over values"""
        for val in self.e:
            self.assertTrue(val in self.enum_values)

    def test_contained_in(self):
        """test contained_in method"""
        self.e2.contained_in(self.e)

    def test_enum_values(self):

        self.assertTrue(self.enum_values == self.e.enum_values)

    def test_struct_iter(self):

        for t in self.s:
            self.assertTrue(isinstance(t, Type))
            self.assertFalse(isinstance(t, StructType))

from fluent import Fluent
from predicate import eq, neq
from variable import Variable


class TestFluentModule(unittest.TestCase):


    def setUp(self):

        self.integer = IntType("integer", 1, 3)
        self.enum_values = ["red", "orange", "yellow"]
        self.e = EnumType("colors", self.enum_values)
        self.s = StructType("s", [self.e, self.integer])
        self.f1 = Fluent("f1", self.s)
        self.f2 = Fluent("f1", self.s)
        self.f3 = Fluent("f3", self.e)

        self.x = Variable("x", self.integer)
        self.color_var = Variable("c", self.e)

    def test_fluent_equality(self):

        self.assertTrue(self.f1 == self.f2)
        self.assertFalse(self.f1 == self.f3)

    def test_Literal(self):

        self.f1('red', 2)

        with self.assertRaises(Exception):
            self.f1("red")
        with self.assertRaises(Exception):
            self.f1("blue", 1)
        with self.assertRaises(Exception):
            self.f1(1, "red")

        self.f1('red', self.x)
        self.f1('red', self.x + 1)
        self.f1('red', 1 + self.x + 1)
        self.f1('red', 1 - self.x)

        with self.assertRaises(Exception):
            self.f1('red', 'red' - self.x)

        self.f3(self.color_var)

    def test_EqualityPredicate(self):

        eq(3, 3)
        with self.assertRaises(Exception):    
            neq(3, "red")


from action import *

class TestAction(unittest.TestCase):

    def setUp(self):
        self.integer = IntType("integer", 1, 3)
        self.enum_values = ["red", "orange", "yellow"]
        self.e = EnumType("color", self.enum_values)
        self.s = StructType("s", [self.e, self.integer])
        self.f1 = Fluent("f1", self.s)
        self.f2 = Fluent("f1", self.s)
        self.f3 = Fluent("f3", self.e)

        self.x = Variable("x", self.integer)
        self.color_var = Variable("c", self.e)

    def test_action(self):

        l_pre = self.f1('red', self.x)
        l_effect = self.f1('yellow', self.x)
        IAction(name="action", params=[self.x], precondition=[l_pre], effects=[l_effect])

from problem import ClassicalPlanningProblem

class TestProblem(unittest.TestCase):

    def setUp(self):
        self.integer = IntType("integer", 1, 3)
        self.enum_values = ["red", "orange", "yellow"]
        self.e = EnumType("color", self.enum_values)
        self.s = StructType("s", [self.e, self.integer])
        self.f1 = Fluent("f1", self.s)
        self.f2 = Fluent("f2", self.s)
        self.f3 = Fluent("f3", self.e)
        self.p = ClassicalPlanningProblem()
        #add fluents:
        p.add_fluent(self.f1)
        p.add_fluent(self.f3)
        #add variables:
        p.add_variable(self.x)
        #add action:
        p.add_action(self.action)


        
if __name__ == "__main__":
    unittest.main()
