from typing import List, Dict
from dataclasses import dataclass
from enum import Enum

from boolean import Expression, Symbol, NOT
from action import I_Action

class Solving_Algorithm(Enum):
    PARTIAL_ORDER_PLANNING = 1

@dataclass
class Problem():

    init   : List[Expression]
    goal   : List[Expression]
    domain : Dict[str, I_Action]

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
