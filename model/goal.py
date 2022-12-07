from dataclasses import dataclass
from typing import Set, List
from predicate import Literal

@dataclass
class Goal():
    """A goal is a named element, labeled by a set of literals"""
    
    name: str
    literals: Set[Literal]

    def __post_init__(self):
        for literal_1 in literals:
            for literal_2 in literals:
                if literal_1 == (- literal_2):
                    raise Exception(f'Incosistent goal {literal_1} and {literal_2}')


class Poset():
    #Poset for now it is only total order

    representation: List[Goal]

    def __init__():
        self.representation = []

    def add_ordered_elements(ordered_elements: List[Goal]) -> None:
        #only one call handled
        self.representation.append(ordered_elements)

    def get_maximal_goals() -> Set[Goal]:
        return representation[-1]
