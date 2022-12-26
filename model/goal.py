import sys, os
from dataclasses import dataclass
from typing import Set, List, Iterator, Tuple, Union, Dict
from copy import deepcopy

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, current_dir)

from .predicate import Literal
from .variable import Variable


def convert_elw(el: Union[Variable, str, int],
               var_val: Dict[Variable, Union[str, int]]) -> Union[str, int]:

    if isinstance(el, int):
        return el
    if isinstance(el, str):
        return el
    if isinstance(el, Variable):
        return var_val[el]

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

    def instatiate(self, var_val: Dict[Variable, Union[str, int]]) -> 'Goal':

        goal = Goal(name=self.name,
                    arguments=list(map(lambda arg : var_val[arg] if isinstance(arg, Variable)
                                                                 else arg,
                                       self.arguments)),
                    literals=list(map(lambda x : x.instatiate(var_val), self.literals)))
        return goal

    def __hash__(self):
        return hash(self.name)        

    def __call__(self, *args) -> 'Goal':
        var_val = dict(zip(self.arguments, list(*args)))
        return self.instatiate(var_val)

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

    def instatiate(self, var_val: Dict[Variable, Union[str, int]]) -> 'Poset':

        return Poset(list(map(lambda x : x.instatiate(var_val), self.representation)))
