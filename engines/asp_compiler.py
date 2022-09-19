from model.shortcuts import *

#holds(F,T)
#occ(A,T)
#possible(A,T)

def compile_into_asp(problem : Problem):

    s = ""
    
    for t in problem.types:
        s += f"{t}"
    for 
    for f in problem.init_value:
        s += f"holds({f.name}, 0).\n"

    
        
