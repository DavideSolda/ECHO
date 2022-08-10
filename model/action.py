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
    precondition : List[Literal]
    effects : List[FLiteral]

@dataclass
class inst_I_Action():
    action : I_Action
    ID : int

def main():
    pass

if __name__ == "__main__":
    main()
