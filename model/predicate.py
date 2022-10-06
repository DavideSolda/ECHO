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
    when: Predicate

    def __init__(self, fluent: 'Fluent', args, when=None):

        super().__init__()
        self.fluent = fluent
        self.args = args
        self.negated = False
        self._types = [self.fluent.type]
        self._variables = [arg.variables for arg in args
                           if isinstance(arg, ArithmeticExpr)]
        self._variables += [arg for arg in args
                            if isinstance(arg, Variable)]
        self.when = None

    def __repr__(self) -> str:
        return f"{self.fluent.name}({self.args})"


class EqualityOperator(Enum):
    eq = "=="
    neq = "!="


class EqualityPredicate(Predicate):

    op: EqualityOperator
    args: List[Union[ArithmeticExpr, int, Variable]]

    def __init__(self, op: EqualityOperator,
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
    def operator(self) -> EqualityOperator:
        return self._op

    @property
    def args(self) -> List[Union[ArithmeticExpr, int, Variable]]:
        return self._args

    def __repr__(self) -> str:
        return f"{self.operator.value} {self._args}"


def eq(l: Union[ArithmeticExpr, int, Variable, str],
       r: Union[ArithmeticExpr, int, Variable, str]):

    if is_int_fvalue(l) and is_int_fvalue(r):
        return EqualityPredicate(EqualityOperator.eq, [l, r])

    if is_enum_fvalue(l) and is_enum_fvalue(r):
        return EqualityPredicate(EqualityOperator.eq, [l, r])

    raise Exception(f"{l} and {r} are not compatible")


def neq(l: Union[ArithmeticExpr, int, Variable, str],
        r: Union[ArithmeticExpr, int, Variable, str]):

    if isinstance(l, int) and isinstance(l, int):
        raise Exception(f'{l} and {r} are both integer')

    if isinstance(l, str) and isinstance(l, str):
        raise Exception(f'{l} and {r} are both strings')

    if is_int_fvalue(l) and is_int_fvalue(r):
        return EqualityPredicate(EqualityOperator.neq, [l, r])

    if is_enum_fvalue(l) and is_enum_fvalue(r):
        return EqualityPredicate(EqualityOperator.neq, [l, r])

    raise Exception(f"{l} and {r} are not compatible")


class BeliefLiteral(Predicate):
    """B_ag(current_position(4))"""
    agents: List[Union[Variable, str]]
    belief_proposition: Predicate
    when: Predicate

    def __init__(self, agents: List[Union[Variable, str]],
                 proposition: Predicate, when=None):

        super().__init__()
        #  typing checks
        for agent in agents:
            assert isinstance(agent, Variable) and agent.is_agent() or \
                isinstance(agent, str)
        assert isinstance(proposition, Literal) \
            or type(proposition) == type(self)

        self.agents = agents
        self.belief_proposition = proposition
        self.when = when

        #  deal with variables
        self._variables = proposition.variables
        for agent in self.agents:
            if isinstance(agent, Variable):
                self._variables.append(agent)
        if when is not None:
            self._variables += when.variables

        #  deal with types
        self._types = proposition.types
        if when is not None:
            self._types += when.types

    def __repr__(self) -> str:  # TODO WHEN
        s = f'B_{self.agents} ({self.belief_proposition})'
        return f'not {s}' if self.negated else s


class ObservablePredicate(Predicate):
    """Predicate to express observability"""

    forall: Union[Variable, EqualityPredicate]
    when: Predicate
    who: Union[str, Variable]

    def __init__(self, who, forall=None, when=None):
        if not self.is_an_agent(who):
            raise ValueError(f'''{who} is neither the name of an agent,
            nor an agent variable''')
        if isinstance(forall, EqualityPredicate):
            if not all(map(self.is_an_agent, forall.args)):
                raise ValueError(f'''forall should talk about agents only''')
            if forall.operator == EqualityOperator.eq or who not in forall.args:
                raise ValueError(f'''forall {forall.args[0]} == 
                {forall.args[1]} {who} does not make sense)''')
        if when is not None and not isinstance(when, Predicate):
            raise ValueError(f'when should be a predicate: {when}')
        self.forall = forall
        self.who = who
        self.when = when
        self.collect_variables()

    def collect_variables(self):
        self._variables = []
        if isinstance(self.who, Variable):
            self._variables.append(self.who)
        #  TODO:check forall
        """
        if self.when is not None:  # TODO remove?
            self._variables
            self._variables += [lit.variables for lit in self.when]
        """

    @staticmethod
    def is_an_agent(agent: Union[str, Variable]) -> bool:
        return isinstance(agent, str) or \
           isinstance(agent, Variable) and agent.is_agent()

    def negated(self) -> bool:
        return False

    def __repr__(self) -> str:
        s = str(self.who)
        if self.when is not None:
            s += f'when {self.when}'
        if self.forall is not None:
            return f'''forall({self.forall.args[0]} != {self.forall.args[1]})
            {s}'''
        return s
