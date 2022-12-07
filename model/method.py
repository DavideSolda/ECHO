"""This modul contains Methods classes"""

from dataclasses import dataclass

from goal import Goal, Poset

@dataclass
class Method():
    """A method consist of an ordered set of goals
    This class provide also two methods for
    1) give the set of maximal goals
    2) give the set of goal pair (g1, g2) s.t. g1 < g2"""

    name: str
    goal_poset: Poset
