from enum import Enum
from dataclasses import field, dataclass
from typing import List, Union, ClassVar
import copy

from arithmetic_expression import is_int_fvalue, is_enum_fvalue, ArithmeticExpr
from variable import Variable
from ftype import Type, AgentType


@dataclass
class Predicate():


    negated: bool
    variables: List[Variable]
    types: List[Union[int, str, Variable]]

    def __post_init__(self):
        self.negated = False

    def __neg__(self) -> 'Predicate':
        negated_p = copy.deepcopy(self)
        negated_p.negated = not self.negated
        return negated_p

    def __and__(self, pl: 'Predicate', pr: 'Predicate') -> 'BooleanPredicate':
        return BooleanPredicate(BooleanOperator.AND, pl, pr)

    def __or__(self, pl: 'Predicate', pr: 'Predicate') -> 'BooleanPredicate':
        return BooleanPredicate(BooleanOperator.OR, pl, pr)


class BooleanOperator(Enum):

    AND = 'and'
    OR = 'or'


@dataclass
class BooleanPredicate(Predicate):

    op: BooleanOperator
    left_predicate: Predicate
    right_predicate: Predicate

    def __post_init__(self):
        """just add info about variables and types"""
        super().__post_init__()
        self.variables = left_predicate.variables + right_predicate.variables
        self.types = left_predicate.types + right_predicate.types


@dataclass
class When(Predicate):

    body: Predicate
    head: Predicate

    negated: bool
    variables: List[Variable]

    def __init__(self, body: Predicate, head: Predicate):

        variables = body.variables + head.variables
        types = body.types + head.types
        negated = False
        self.body = body
        self.head = head
        super().__init__(negated = negated, variables = variables, types = types)


@dataclass
class Literal(Predicate):

    fluent: 'Fluent'
    args: List[Union[ArithmeticExpr, int, str, Variable]] = field(
        default_factory=(lambda: []))

    def __post_init__(self):
        """just add info about variables and types"""
        super().__post_init__()

        self.types = [self.fluent.type]
        self.variables = [arg.variables for arg in self.args
                          if isinstance(arg, ArithmeticExpr)]
        self.variables += [arg for arg in self.args
                           if isinstance(arg, Variable)]


class EqualityOperator(Enum):

    eq = "=="
    neq = "!="


@dataclass
class EqualityPredicate(Predicate):


    operator: EqualityOperator
    left_operand: Union[ArithmeticExpr, int, Variable]
    right_operand:Union[ArithmeticExpr, int, Variable]

    def __post_init__(self):

        super().__post_init__()
        
        self.variables = get_fvalues_variable(self.left_operand) +\
            get_fvalues_variable(self.right_operand)
        self.types = get_fvalues_type(self.left_operand) +\
            get_fvalues_type(self.right_operand)
        if is_int_fvalue(self.left_operand) and is_int_fvalue(self.right_operand) or\
           is_enum_fvalue(self.left_operand) and is_enum_fvalue(self.right_operand):
            return
        else:
            raise Exception(f"{l} and {r} are not compatible")



def eq(l: Union[ArithmeticExpr, int, Variable, str],
       r: Union[ArithmeticExpr, int, Variable, str]):

    return EqualityPredicate(negated = False, types = [], variables = [],
                             operator = EqualityOperator.eq, left_operand = l,
                             right_operand = r)


def neq(l: Union[ArithmeticExpr, int, Variable, str],
        r: Union[ArithmeticExpr, int, Variable, str]):

    return EqualityPredicate(negated = False, types = [], variables = [],
                             operator = EqualityOperator.neq, left_operand = l,
                             right_operand = r)


def get_fvalues_type(fvalue: Union[ArithmeticExpr, int, Variable, str]) -> List[Type]:
    if isinstance(fvalue, ArithmeticExpr):
        return fvalue.types
    elif isinstance(fvalue, Variable):
        return [fvalue.type]
    return []


def get_fvalues_variable(fvalue: Union[ArithmeticExpr, int, Variable, str]) -> List[Variable]:
    if isinstance(fvalue, Variable):
        return [fvalue]
    if isinstance(fvalue, ArithmeticExpr):
        return fvalue.variables
    return []


class BeliefLiteral(Predicate):
    """B_ag(current_position(4))"""
    agents: List[Union[Variable, str]]
    belief_proposition: Union['BeliefLiteral', Literal]

    def __init__(self, agents: List[Union[Variable, str]],
                 proposition: Union['BeliefLiteral', Literal]):

        for agent in agents:
            assert isinstance(agent, (Variable, str))
        assert isinstance(proposition, Literal) or \
            proposition.__name__ == 'BeliefLiteral'

        types = proposition.types
        
        #  deal with variables
        variables = proposition.variables
        for agent in agents:
            if isinstance(agent, Variable):
                variables.append(agent)

        super().__init__(negated=False, variables=variables, types=types)
        #  typing checks
        for agent in agents:
            assert isinstance(agent, Variable) and agent.is_agent() or \
                isinstance(agent, str)

        assert isinstance(proposition, Literal) \
            or type(proposition) == type(self)

        self.agents = agents
        self.belief_proposition = proposition


    def __repr__(self) -> str:
        s = f'B_{self.agents} ({self.belief_proposition})'
        return f'not {s}' if self.negated else s


def B(agents, proposition) -> BeliefLiteral:
    if type(proposition).__name__ == 'Fluent':
        proposition = Literal(fluent=proposition, args=[])
    return BeliefLiteral(agents=agents, proposition=proposition)


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
            if not all(map(self.is_an_agent, forall.variables)):
                raise ValueError(f'''forall should talk about agents only''')
            if forall.operator == EqualityOperator.eq or who not in forall.variables:
                raise ValueError(f'''forall {forall.variables[0]} == 
                {forall.variables[1]} {who} does not make sense)''')
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
            if isinstance(self.forall, Predicate):
                return f'''forall({self.forall.variables[0]} != {self.forall.variables[1]})
                {s}'''
            elif isinstance(self.forall, Variable):
                return f'''forall({self.forall.name})'''
        return s
