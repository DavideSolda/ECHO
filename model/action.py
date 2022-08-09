from typing import List
from dataclasses import dataclass
from boolean import Expression, Symbol, NOT

#TODO: introduction of templates
#      needs of a fluent definition wich can be or boolean or of a particular type
#      you should also be able to define new types
#TODO: definition of a fixed set of actions that have a direct encoding into moveit

@dataclass
class I_Action():
    name : str
    precondition : List[Expression]
    effects : List[Expression]

@dataclass
class inst_I_Action():
    action : I_Action
    ID : int

def main():
    p = Symbol("p")
    q = Symbol("q")
    a = I_Action(name = "a_1",\
                 precondition = [p,q],\
                 effects = [NOT(p)])
    print(a)
    i_a = inst_I_Action(a, 2)
    print(i_a)

if __name__ == "__main__":
    main()
