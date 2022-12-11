"""This modul contains Methods classes"""

from dataclasses import dataclass
from typing import List

from goal import Goal, Poset
from variable import Variable
from predicate import Literal

@dataclass
class Method():
    """A method consist of an ordered set of goals
    This class provide also two methods for
    1) give the set of maximal goals
    2) give the set of goal pair (g1, g2) s.t. g1 < g2"""

    name: str
    params: List[Variable]
    precondition: List[Literal]
    goal_poset: Poset
