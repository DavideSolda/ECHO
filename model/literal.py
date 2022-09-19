from dataclasses import dataclass, field
from typing import List, Union

class Literal():

    negated : bool
    _types : List[Union[int, str, "Variable"]]
    _variables : List["Variable"]

    def __init__(self):
        negated = False
        
    def __neg__(self):
        self.negated = not self.negated
        return self

    @property
    def types(self):
        return self._types

    @property
    def variables(self):
        return self._variables

class FLiteral(Literal):

    fluent : "Fluent"
    args : List[Union[int, str, "Variable"]] = field(default_factory = (lambda : []))

    def __init__(self, fluent : "Fluent", args):

        super().__init__()
        self.fluent = fluent
        self.args = args
        self.negated = False
        self._types = [self.fluent.type]
        self._variables = []
        for arg in args:
            try:
                self.variables.append(arg.variables)
            except:
                pass

    def __repr__(self) -> str:
        return f"{self.fluent.name}({self.args})"

class BELiteral(Literal):

    op : "BooleanOperator"
    args : List[Union["ArithmenticExpr", int, "Variable"]]

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
        self._variables = []
        for arg in args:
            try:
                self.variables.append(arg.variables)
            except:
                pass
        
