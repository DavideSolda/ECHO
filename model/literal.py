from dataclasses import dataclass, field
from typing import List, Union

class Literal():

    negated : bool

    def __init__(self):
        negated = False
        
    def __neg__(self):
        self.negated = not self.negated
        return self

@dataclass
class FLiteral(Literal):

    fluent : "Fluent"
    negated : bool
    args : List[Union[int, str, "Variable"]] = field(default_factory = (lambda : []))

    def __init__(self, fluent : "Fluent", args):

        super().__init__()
        self.fluent = fluent
        self.args = args
        self.negated = False

@dataclass
class BELiteral(Literal):

    op : "BooleanOperator"
    args : List[Union["ArithmenticExpr", int, "Variable"]]
