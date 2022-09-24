from enum import Enum
from dataclasses import field
from typing import List, Union

from arithmetic_expression import is_int_fvalue, is_enum_fvalue, ArithmeticExpr
from variable import Variable
from ftype import EnumType


class Predicate():

    negated: bool
    _types: List[Union[int, str, Variable]]
    _variables: List[Variable]

    def __init__(self):
        self.negated = False

    def __neg__(self):
        self.negated = not self.negated
        return self

    @property
    def types(self):
        return self._types

    @property
    def variables(self):
        return self._variables


class Literal(Predicate):

    fluent: 'Fluent'
    args: List[Union[ArithmeticExpr, int, str, Variable]] = field(
        default_factory=(lambda: []))

    def __init__(self, fluent: 'Fluent', args):

        super().__init__()
        self.fluent = fluent
        self.args = args
        self.negated = False
        self._types = [self.fluent.type]
        self._variables = [arg.variables for arg in args
                           if isinstance(arg, ArithmeticExpr)]
        self._variables += [arg for arg in args
                            if isinstance(arg, Variable)]

    def __repr__(self) -> str:
        return f"{self.fluent.name}({self.args})"


class BooleanOperator(Enum):
    Eq = "=="
    Neq = "!="


class EqualityPredicate(Predicate):

    op: BooleanOperator
    args: List[Union[ArithmeticExpr, int, Variable]]

    def __init__(self, op: BooleanOperator,
                 args: List[Union[ArithmeticExpr, int, Variable]]):
        assert len(args) == 2
        self._op = op
        self._args = args
        self._types = [arg.type for arg in args
                       if isinstance(arg, Variable) or
                       isinstance(arg, ArithmeticExpr)]
        self._variables = [arg.variables for arg in args
                           if isinstance(arg, ArithmeticExpr)]
        self._variables += [arg for arg in args
                            if isinstance(arg, Variable)]

    @property
    def operator(self) -> BooleanOperator:
        return self._op

    @property
    def args(self) -> List[Union[ArithmeticExpr, int, Variable]]:
        return self._args

    def __repr__(self) -> str:
        return f"{self.operator.value} {self._args}"


def eq(l: Union[ArithmeticExpr, int, Variable, str],
       r: Union[ArithmeticExpr, int, Variable, str]):

    if is_int_fvalue(l) and is_int_fvalue(r):
        return EqualityPredicate(BooleanOperator.Eq, [l, r])

    if is_enum_fvalue(l) and is_enum_fvalue(r):
        return EqualityPredicate(BooleanOperator.Eq, [l, r])

    raise Exception(f"{l} and {r} are not compatible")


def neq(l: Union[ArithmeticExpr, int, Variable, str],
        r: Union[ArithmeticExpr, int, Variable, str]):

    if is_int_fvalue(l) and is_int_fvalue(r):
        return EqualityPredicate(BooleanOperator.Eq, [l, r])

    if is_enum_fvalue(l) and is_enum_fvalue(r):
        return EqualityPredicate(BooleanOperator.Eq, [l, r])

    raise Exception(f"{l} and {r} are not compatible")


class BeliefLiteral(Predicate):
    """B_ag(current_position(4))"""
    agent: Union[EnumType, str]
    belief_proposition: Predicate

    def __init__(self, agent: Union[EnumType, str], proposition: Predicate):

        #  typing checks
        assert isinstance(agent, EnumType) or isinstance(agent, str)
        assert isinstance(proposition, Predicate)
        assert not isinstance(proposition, EqualityPredicate)

        self.agent = agent
        self.belief_proposition = proposition
