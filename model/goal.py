from dataclasses import dataclass
from typing import Set, List, Iterator, Tuple, Union
from predicate import Literal
from variable import Variable


@dataclass
class Goal():
    """A goal is a named element, labeled by a set of literals"""
    
    name: str
    arguments: List[Union[Variable, str, int]]
    literals: Set[Literal]

    def __post_init__(self):
        for literal_1 in self.literals:
            for literal_2 in self.literals:
                if literal_1 == (- literal_2):
                    raise Exception(f'Incosistent goal {literal_1} and {literal_2}')

    def __hash__(self):
        return hash(self.name)


class Poset():
    #Poset for now it is only total order

    representation: List[Goal]

    def __init__(self, representation):
        self.representation = representation

    def add_ordered_elements(ordered_elements: List[Goal]) -> None:
        #only one call handled
        self.representation.append(ordered_elements)

    def get_goals(self) -> Set[Goal]:
        return set(self.representation)
        
    def get_maximal_goals(self) -> Iterator[Goal]:
        yield(self.representation[-1])

    def get_precedence_relations(self) -> Iterator[Tuple[Goal, Goal]]:
        for i in range(0, len(self.representation)-1):
            yield(self.representation[i], self.representation[i+1])