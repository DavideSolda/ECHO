from dataclasses import dataclass, field
from typing import List, Union

class Literal():

    negated : bool
    _types : List[Union[int, str, "Variable"]]

    def __init__(self):
        negated = False
        
    def __neg__(self):
        self.negated = not self.negated
        return self

    @property
    def types(self):
        return self._types

@dataclass
class FLiteral(Literal):

    fluent : "Fluent"
    negated : bool
    args : List[Union[int, str, "Variable"]] = field(default_factory = (lambda : []))
    _types : field(default_factory = (lambda : []))

    def __init__(self, fluent : "Fluent", args):

        super().__init__()
        self.fluent = fluent
        self.args = args
        self.negated = False
        self._types.append(self.fluent.type)

@dataclass
class BELiteral(Literal):

    op : "BooleanOperator"
    args : List[Union["ArithmenticExpr", int, "Variable"]]
    #_types : field(default_factory = (lambda : []))

    def __init__(self, op : "BooleanOperator", \
                 args : List[Union["ArithmenticExpr", int, "Variable"]]):
        self.op = op
        self.args = args
        self._types = []
        for arg in args:
            try:
                self._types.append(arg.type)
            except:
                pass
        
