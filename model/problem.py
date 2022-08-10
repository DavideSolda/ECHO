from typing import List, Dict
from dataclasses import dataclass
from enum import Enum

from action import I_Action
from fluent import *
from literal import *
from fvalue import *
from ftype import *

class Solving_Algorithm(Enum):
    PARTIAL_ORDER_PLANNING = 1
    ANSWER_SET_PLANNING = 2

@dataclass
class Problem():

    init     : List[FLiteral]
    goal     : List[FLiteral]
    ftype    : Dict[str, Type]
    variable : Dict[str, Variable]
    domain   : Dict[str, I_Action]
    

    def add_type(self, type_name : str, t : Type):

        self.ftype[type_name] = t

    def add_variable(self, variable_name : str, v : Variable):
        
    def add_action(self, action_name : str, action : I_Action):

        self.domain[action_name] = action

    

    
    def solve(self, solving_algorithm : Solving_Algorithm = Solving_Algorithm.PARTIAL_ORDER_PLANNING):
        if (solving_algorithm == Solving_Algorithm.PARTIAL_ORDER_PLANNING):
            self._solve_POP()
        return

    def _solve_POP(self):
        return

def main():
    p = Symbol("p")
    q = Symbol("q")
    a = I_Action(name = "a_1",\
                 precondition = [p,q],\
                 effects = [NOT(p)])
    domain = {"a_1" : a}
    problem = Problem(init = [p,q],\
                      goal = [NOT(p)],\
                      domain = domain)

    a2 = I_Action(name = "a_2",\
                  precondition = [p,q],\
                  effects = [NOT(q)])
    problem.add_action("a_2", a2)
    print(problem)
    problem.solve()

if __name__ == "__main__":
  main()
