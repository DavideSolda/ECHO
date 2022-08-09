import unittest


from interval import *
class TestIntervalModule(unittest.TestCase):

    def test_equality(self):
        self.assertTrue(Interval(1, 3), Interval(1, 3))

    def test_overlaps(self):
        i1 = Interval(1, 3)
        i2 = Interval(2, 5)
        i3 = Interval(2, 2)
        i4 = Interval(10, 15)
        self.assertTrue(i1.overlaps(i2))
        self.assertTrue(i2.overlaps(i3))
        self.assertFalse(i1.overlaps(i4))

from ftype import *
class TestFTypeModule(unittest.TestCase):

    def setUp(self):

        self.integer = IntType(1, 3)
        self.b = BoolType()
        self.enum_values = ["red", "orange", "yellow"]
        self.e = EnumType(self.enum_values)
        self.s = StructType([self.e, self.integer])

    
    def test_is_bool_type(self):
        
        self.assertTrue(self.b.is_bool_type())
        self.assertFalse(self.integer.is_bool_type())

    def test_is_int_type(self):
        
        self.assertTrue(self.integer.is_int_type())
        self.assertFalse(self.e.is_int_type())

    def test_is_enum_type(self):
        
        self.assertTrue(self.e.is_enum_type())

    def test_is_struct_type(self):

        self.assertTrue(self.s.is_struct_type())

    def test_int_interval(self):

        self.assertTrue(self.integer.interval == (1,3))
    def test_enum_iter(self):

        for val in self.e:
            self.assertTrue(val in self.enum_values)

    def test_enum_values(self):

        self.assertTrue(self.enum_values == self.e.enum_values)

    def test_struct_iter(self):

        for t in self.s:
            self.assertTrue(isinstance(t, Type))
            self.assertFalse(isinstance(t, StructType))

            
from fluent import *
class TestFluentModule(unittest.TestCase):


    def setUp(self):

        self.integer = IntType(1, 3)
        self.enum_values = ["red", "orange", "yellow"]
        self.e = EnumType(self.enum_values)
        self.s = StructType([self.e, self.integer])
        self.f1 = Fluent("f1", self.s)
        self.f2 = Fluent("f1", self.s)
        self.f3 = Fluent("f3", self.e)

    def test_fluent_equality(self):

        self.assertTrue(self.f1 == self.f2)
        self.assertFalse(self.f1 == self.f3)

if __name__ == "__main__":
    unittest.main()
        
