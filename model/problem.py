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

    def __init__(self):
        self.inits     : List[FLiteral] = []
        self.goals     : List[FLiteral] = []
        self.types     : List[Type]     = []
        self.variables : List[Variable] = []
        self.fluents   : List[Fluent]   = []
        self.domain    : List[I_Action] = []

    def add_type(self, t : Type) -> None:

        for _t in self.types:
            if t == _t:
                logging.info(f"{t} already inserted")
            elif _t.name == t.name:
                raise Exception(f"{_t} has name {_t.name} as {t}")

        self.types.append(t)

    def add_variable(self, v : Variable) -> None:

        if not v.type in self.types:

            raise Exception(f"{v.type} not added")

        self.variables.append(v)

    def add_fluent(self, fluent : Fluent):

        if not fluent.type in self.types:

            raise Exception(f"{v.type} not added")

        self.fluents.append(fluent)

    def add_action(self, action : I_Action):

        for pre in action.precondition:
            for t in pre.types:
                if not t in self.types:
                    raise Exception(f"{t} not added, from {pre} in preconditions")

        for eff in action.effects:
            for t in eff.types:
                if not t in self.types:
                    raise Exception(f"{t} not added, from {eff} in effects")

        self.domain.append(action)

    def add_initial_values(self, *args):

        for arg in args:
            self.inits.append(arg)

    def add_goals(self, *args):

        for arg in args:
            self.gaols.append(arg)

    def __repr__(self):

        sep = "\n\n-----------------------\n\n"
        s = "Problem domain:"
        s += sep
        s += "Types\n"
        s += "\n".join(map(lambda x: str(x), self.types))
        s += sep
        s += "Variables\n"
        s += "\n".join(self.variables)
        s += sep
        s += "Fluents\n"
        s += "\n".join(self.fluents)
        s += sep
        s += "Actions\n"
        s += "\n".join(self.domain)
        s += sep + sep
        s += "Problem instance:"
        s += sep
        s += "Initial values\n"
        s += "\n".join(self.inits)
        s += sep
        s += "Goals\n"
        s += "\n".join(self.goals)

        return s
    def solve(self, solving_algorithm : Solving_Algorithm = Solving_Algorithm.PARTIAL_ORDER_PLANNING):
        if (solving_algorithm == Solving_Algorithm.PARTIAL_ORDER_PLANNING):
            self._solve_POP()
        return

    def _solve_POP(self):
        return

def main():

    problem = Problem()
    i = IntType("i", 1, 4)
    problem.add_type(i)
    print(problem)
    #problem.solve()

if __name__ == "__main__":
  main()
