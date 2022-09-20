from typing import List
from dataclasses import dataclass
from fluent import *
from literal import *
from fvalue import *
from ftype import *

#TODO: introduction of templates
#      needs of a fluent definition wich can be or boolean or of a particular type
#      you should also be able to define new types
#TODO: definition of a fixed set of actions that have a direct encoding into moveit

@dataclass(frozen=True)
class I_Action():
    name : str
    params : List[Union[int, str, Variable, ArithmeticExpr]]
    precondition : List[Literal]
    effects : List[FLiteral]
    params_var : List[Variable]
    precondition_var : List[Variable]
    effects_var : List[Variable]

    def __init__(self, name, params, precondition, effects):
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "params", params)
        object.__setattr__(self, "precondition", precondition)
        object.__setattr__(self, "effects", effects)

        #extract variables from action parameters:
        par_vars = []
        for param in self.params:
            if isinstance(param, Variable):
                par_vars.append(param)
            elif isinstance(param, ArithmeticExpr):
                par_vars = par_vars + param.variables
        object.__setattr__(self, "params_var", par_vars)

        #extract variables from action preconditions:
        precond_vars = []
        for literal in self.precondition:
            precond_vars += literal.variables
        object.__setattr__(self, "precondition_var", precond_vars)

        #extract variables from action effects:
        effect_vars = []
        for literal in self.effects:
            effect_vars += literal.variables
        object.__setattr__(self, "effects_var", effect_vars)

@dataclass
class inst_I_Action():
    action : I_Action
    ID : int
