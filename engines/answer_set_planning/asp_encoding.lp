%Answer set planning.

%Answer set planning: A Survey. E. Pontelli et al. For a survey.
%Epistemic Multiagent Reasoning with Collaborative Robots: D. Solda' el al. For a practical use-case.



%%%%%%%%%% [[	PROBLEM DEPENDENT RULES	]] %%%%%%%%%%



%%%%%%%%%% TYPES %%%%%%%%%%

stack(1..3).
color(red;orange;yellow;black;violet;brown;white;green;blue;gray).


%%%%%%%%%% FLUENTS %%%%%%%%%%

fluent(on_block(A, B)):-color(A),color(B).
fluent(on_stack(A, B)):-color(A),stack(B).
fluent(top_block(X)):-color(X).
fluent(gripped(X)):-color(X).
fluent(free_gripper).
fluent(free_stack(X)):-stack(X).


%%%%%%%%%% INITIALLY %%%%%%%%%%

holds(on_stack(red,1), 1).
holds(on_block(orange,red), 1).
holds(on_block(yellow,orange), 1).
holds(on_block(black,yellow), 1).
holds(top_block(black), 1).
holds(on_stack(violet,2), 1).
holds(on_block(brown,violet), 1).
holds(on_block(white,brown), 1).
holds(on_block(green,white), 1).
holds(top_block(green), 1).
holds(free_gripper, 1).
holds(on_stack(blue,3), 1).
holds(on_block(gray,blue), 1).
holds(top_block(gray), 1).


%%%%%%%%%% ACTIONS %%%%%%%%%%

action(pick(C1,C2)):-color(C1),color(C2).
action(place(C1,C2)):-color(C1),color(C2).
action(place_on_ground(C1,S)):-color(C1),stack(S).
action(pick_from_ground(C1,S)):-color(C1),stack(S).


%%%%%%%%%% EXECUTABLE %%%%%%%%%%

exec(pick(C1,C2),top_block(C1)):-color(C2),color(C1).
exec(pick(C1,C2),on_block(C1,C2)):-color(C2),color(C1).
exec(pick(C1,C2),free_gripper):-color(C2),color(C1).
exec(place(C1,C2),top_block(C2)):-color(C2),color(C1).
exec(place(C1,C2),neg(free_gripper)):-color(C2),color(C1).
exec(place(C1,C2),gripped(C1)):-color(C2),color(C1).
exec(place_on_ground(C1,S),free_stack(S)):-stack(S),color(C1).
exec(place_on_ground(C1,S),neg(free_gripper)):-stack(S),color(C1).
exec(place_on_ground(C1,S),gripped(C1)):-stack(S),color(C1).
exec(pick_from_ground(C1,S),top_block(C1)):-stack(S),color(C1).
exec(pick_from_ground(C1,S),on_stack(C1,S)):-stack(S),color(C1).
exec(pick_from_ground(C1,S),free_gripper):-stack(S),color(C1).


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
causes(place_on_ground(C1,S),neg(free_stack(S))):-stack(S),color(C1).
causes(place_on_ground(C1,S),top_block(C1)):-stack(S),color(C1).
causes(place_on_ground(C1,S),free_gripper):-stack(S),color(C1).
causes(place_on_ground(C1,S),neg(gripped(C1))):-stack(S),color(C1).
causes(place_on_ground(C1,S),on_stack(C1,S)):-stack(S),color(C1).
causes(pick_from_ground(C1,S),free_stack(S)):-stack(S),color(C1).
causes(pick_from_ground(C1,S),neg(top_block(C1))):-stack(S),color(C1).
causes(pick_from_ground(C1,S),neg(on_stack(C1,S))):-stack(S),color(C1).
causes(pick_from_ground(C1,S),neg(free_gripper)):-stack(S),color(C1).
causes(pick_from_ground(C1,S),gripped(C1)):-stack(S),color(C1).


%%%%%%%%%% GOALS %%%%%%%%%%

goal(on_block(blue,red)).


%%%%%%%%%% [[	PROBLEM INDEPENDENT RULES	]] %%%%%%%%%%

opposite(F, neg(F)) :- fluent(F).
opposite(neg(F), F) :- fluent(F).
#program step(t).
holds(F,t+1) :- opposite(F,G), holds(F,t), not holds(G, t+1).
not_executable(A,t) :- fluent(F), exec(A,F), not holds(F,t).
not_executable(A,t) :- exec(A,G), opposite(F,G), holds(F,t).
executable(A,t) :- not not_executable(A,t), action(A).
holds(F, t+1) :- executable(A,t), occurs(A,t), causes(A,F).
1{occurs(A,t) : action(A)}1.
:- action(A), occurs(A,t), not executable(A,t).
#program check(t).
:- goal(F), not holds(F,t+1), query(t).
:- goal(neg(F)), holds(F,t+1), query(t).
#program base.
