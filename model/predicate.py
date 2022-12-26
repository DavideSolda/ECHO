import sys, os
from dataclasses import field, dataclass
from typing import List, Union, ClassVar, Optional, Dict
import copy
from enum import Enum

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, current_dir)

from .arithmetic_expression import is_int_fvalue, is_enum_fvalue, ArithmeticExpr
from .variable import Variable
from .ftype import Type, AgentType


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
        print(BooleanPredicate(BooleanOperator.OR, pl, pr))
        quit()
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
        self.variables = self.left_predicate.variables + self.right_predicate.variables
        self.types = self.left_predicate.types + self.right_predicate.types


def conj(lp, rp) -> BooleanPredicate:
    return BooleanPredicate(False, [], [], BooleanOperator.AND, lp, rp)


def disj(lp, rp) -> BooleanPredicate:
    return BooleanPredicate(False, [], [], BooleanOperator.OR, lp, rp)


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

    def instatiate(self, var_val: Dict[Variable, Union[str, int]]) -> 'Literal':

        args = copy.deepcopy(self.args)
        for idx, arg in enumerate(args):
            if isinstance(arg, Variable):
                args[idx] = var_val[arg]
        if self.negated:
            return -self.fluent(*args)
        else:
            return self.fluent(*args)

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

    def __repr__(self) -> str:
        return f'sc.EqualityPredicate: {self.left_operand}' + str(self.operator) + f'{self.right_operand}'


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


class BeliefPredicate(Predicate):
    """B_ag(current_position(4))"""
    agents: List[Union[Variable, str]]
    belief_proposition: Predicate

    def __init__(self, agents: List[Union[Variable, str]],
                 proposition: Predicate):

        for agent in agents:
            assert isinstance(agent, (Variable, str))
        assert isinstance(proposition, Predicate)

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


def B(agents, proposition) -> BeliefPredicate:
    if type(proposition).__name__ == 'Fluent':
        proposition = Literal(fluent=proposition, args=[])
    return BeliefPredicate(agents=agents, proposition=proposition)


@dataclass
class When(Predicate):
    body: Predicate
    head: Predicate

    def __init__(self, body, head):

        negate = False
        variables = body.variables + head.variables
        types = body.types + head.types

        super().__init__(negate, variables, types)

        assert isinstance(body, Predicate)
        assert isinstance(head, Predicate)

        self.variables = body.variables + head.variables
        self.types = body.types + head.types

        self.body = body
        self.head = head

class Forall():
    """Predicate to express forall formulae"""

    quantified_variable: Variable
    disequality_predicate: Optional[EqualityPredicate]
    when: Optional[When]
    who: Union[Variable, str]

    variables: List[Variable]
    types: List[Type]

    def __init__(self, quantified_variable: Variable, neq: EqualityPredicate=None,
                 when: Predicate=None, who: Union[Variable, str]=None):

        self.quantified_variable = quantified_variable
        self.disequality_predicate = neq
        self.when = when
        self.who = who


    def __post_init__(self):

        self.variables = []
        self.types = []

        #check that the quantified variable is an agent
        if not isinstance(self.quantified_variable, Variable):
            raise ValueError(f'''{quantified_variable} is neither the name of an agent,
            nor an agent variable''')
        else:
            self.variables.append(self.quantified_variable)

        #if specified, equality_predicate should contain the quantified variable
        if self.equality_predicate is not None:
            assert isinstance(self.equality_predicate, EqualityPredicate)

            if disequality_predicate.operator == EqualityOperator.eq or \
               quantified_variable not in disequality_predicate.variables:
                raise ValueError(f'''forall {disequality_predicate.variables[0].name} == 
                {disequality_predicate.variables[1].name} {quantified_variable.name} does not make sense)''')
            self.variables = disequality_predicate.variables

        #if specified, when should be an instance of Predicate
        if when is not None and not isinstance(when, Predicate):
            raise ValueError(f'when should be a predicate: {when}')
        elif when is not None:
            self.variables += [var for var in when.variables
                               if var != self.quantified_variable]


    def __repr__(self) -> str:
        
        s = f'forall {self.quantified_variable.name} '
        if self.disequality_predicate is not None:
            s += f'{self.disequality_predicate} '
        if self.when is not None:
            s += f'(when {self.when} )'
        s += f'{self.quantified_variable.name}' 
        return s
