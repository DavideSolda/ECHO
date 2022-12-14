%Answer set planning.

%Answer set planning: A Survey. E. Pontelli et al. For a survey.
%Epistemic Multiagent Reasoning with Collaborative Robots: D. Solda' el al. For a practical use-case.



%%%%%%%%%% [[	PROBLEM DEPENDENT RULES	]] %%%%%%%%%%



%%%%%%%%%% TYPES %%%%%%%%%%

stak(1..3).
color(red;orange;yellow;black).
colorxcolor(red;orange;yellow;black,red;orange;yellow;black).
colorxstack(red;orange;yellow;black,1..3).


%%%%%%%%%% FLUENTS %%%%%%%%%%

fluent(on_block(A, B)):-color(A),color(B).
fluent(on_stack(A, B)):-color(A),stak(B).
fluent(top_block(X)):-color(X).
fluent(gripped(X)):-color(X).
fluent(free_gripper).
fluent(free_stack(X)):-stak(X).


%%%%%%%%%% INITIALLY %%%%%%%%%%

holds(on_stack(red,1), 1).
holds(on_block(black,red), 1).
holds(top_block(black), 1).
holds(on_stack(orange,2), 1).
holds(top_block(orange), 1).
holds(free_gripper, 1).
holds(free_stack(3), 1).


%%%%%%%%%% ACTIONS %%%%%%%%%%

action(pick(C1,C2)):-color(C1),color(C2).
action(place(C1,C2)):-color(C1),color(C2).
action(place_on_ground(C1,S)):-color(C1),stak(S).


%%%%%%%%%% EXECUTABLE %%%%%%%%%%

exec(pick(C1,C2),top_block(C1)):-color(C2),color(C1).
exec(pick(C1,C2),on_block(C1,C2)):-color(C2),color(C1).
exec(pick(C1,C2),free_gripper):-color(C2),color(C1).
exec(place(C1,C2),top_block(C2)):-color(C2),color(C1).
exec(place(C1,C2),neg(free_gripper)):-color(C2),color(C1).
exec(place(C1,C2),gripped(C1)):-color(C2),color(C1).
exec(place_on_ground(C1,S),free_stack(S)):-color(C1),stak(S).
exec(place_on_ground(C1,S),neg(free_gripper)):-color(C1),stak(S).
exec(place_on_ground(C1,S),gripped(C1)):-color(C1),stak(S).


%%%%%%%%%% CAUSES %%%%%%%%%%

causes(pick(C1,C2),neg(top_block(C1))):-color(C2),color(C1).
causes(pick(C1,C2),neg(on_block(C1,C2))):-color(C2),color(C1).
causes(pick(C1,C2),top_block(C2)):-color(C2),color(C1).
causes(pick(C1,C2),neg(free_gripper)):-color(C2),color(C1).
causes(pick(C1,C2),gripped(C1)):-color(C2),color(C1).
causes(place(C1,C2),top_block(C1)):-color(C2),color(C1).
causes(place(C1,C2),on_block(C1,C2)):-color(C2),color(C1).
causes(place(C1,C2),neg(top_block(C2))):-color(C2),color(C1).
causes(place(C1,C2),free_gripper):-color(C2),color(C1).
causes(place(C1,C2),neg(gripped(C1))):-color(C2),color(C1).
causes(place_on_ground(C1,S),neg(free_stack(S))):-color(C1),stak(S).
causes(place_on_ground(C1,S),top_block(C1)):-color(C1),stak(S).
causes(place_on_ground(C1,S),free_gripper):-color(C1),stak(S).
causes(place_on_ground(C1,S),neg(gripped(C1))):-color(C1),stak(S).


%%%%%%%%%% GOALS %%%%%%%%%%

goal(on_block(black,orange)).
goal(free_gripper).


%%%%%%%%%% [[	PROBLEM INDEPENDENT RULES	]] %%%%%%%%%%

opposite(F, neg(F)) :- fluent(F).
opposite(neg(F), F) :- fluent(F).
#program step(t).
holds(F,t+1) :- opposite(F,G), holds(F,t), not holds(G, t+1).
not_executable(A,t) :- exec(A,F), not holds(F,t).
executable(A,t) :- not not_executable(A,t), action(A).
holds(F, t+1) :- executable(A,t), occurs(A,t), causes(A,F).
{occurs(A,t) : action(A)}1.
:- action(A), occurs(A,t), not executable(A,t).
#program check(t).
:- goal(F), not holds(F,t+1), query(t).
:- goal(neg(F)), holds(F,t+1), query(t).
#program base.
