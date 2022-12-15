%Answer set planning.

%Answer set planning: A Survey. E. Pontelli et al. For a survey.
%Epistemic Multiagent Reasoning with Collaborative Robots: D. Solda' el al. For a practical use-case.



%%%%%%%%%% [[	PROBLEM DEPENDENT RULES	]] %%%%%%%%%%



%%%%%%%%%% TYPES %%%%%%%%%%

agent(alice;bob).
stack(1..3).
color(red;orange;yellow;black).
colorxcolor(red;orange;yellow;black,red;orange;yellow;black).
colorxstack(red;orange;yellow;black,1..3).
agentxcolor(alice;bob,red;orange;yellow;black).


%%%%%%%%%% FLUENTS %%%%%%%%%%

fluent(on_block(A, B)):-color(A),color(B).
fluent(on_stack(A, B)):-color(A),stack(B).
fluent(top_block(X)):-color(X).
fluent(gripped(A, B)):-agent(A),color(B).
fluent(free_gripper(X)):-agent(X).
fluent(free_stack(X)):-stack(X).
fluent(owner(A, B)):-agent(A),color(B).
fluent(free_table).
fluent(table(X)):-color(X).


%%%%%%%%%% INITIALLY %%%%%%%%%%

holds(free_gripper(alice), 1).
holds(table(black), 1).
holds(free_gripper(bob), 1).
holds(owner(bob,red), 1).
holds(owner(bob,orange), 1).
holds(top_block(red), 1).
holds(top_block(orange), 1).
holds(free_stack(3), 1).
holds(on_stack(orange,2), 1).
holds(on_stack(red,1), 1).


%%%%%%%%%% ACTIONS %%%%%%%%%%

action(pick(R,C1,C2)):-agent(R),color(C1),color(C2).
action(pick_from_ground(R,C1,S)):-agent(R),color(C1),stack(S).
action(place(R,C1,C2)):-agent(R),color(C1),color(C2).
action(place_on_ground(R,C1,S)):-agent(R),color(C1),stack(S).
action(pick_from_table(R,C1)):-agent(R),color(C1).
action(place_on_table(R,C1)):-agent(R),color(C1).


%%%%%%%%%% EXECUTABLE %%%%%%%%%%

exec(pick(R,C1,C2),top_block(C1)):-agent(R),color(C2),color(C1).
exec(pick(R,C1,C2),on_block(C1,C2)):-agent(R),color(C2),color(C1).
exec(pick(R,C1,C2),free_gripper(R)):-agent(R),color(C2),color(C1).
exec(pick(R,C1,C2),owner(R,C1)):-agent(R),color(C2),color(C1).
exec(pick_from_ground(R,C1,S),top_block(C1)):-agent(R),stack(S),color(C1).
exec(pick_from_ground(R,C1,S),on_stack(C1,S)):-agent(R),stack(S),color(C1).
exec(pick_from_ground(R,C1,S),free_gripper(R)):-agent(R),stack(S),color(C1).
exec(pick_from_ground(R,C1,S),owner(R,C1)):-agent(R),stack(S),color(C1).
exec(place(R,C1,C2),top_block(C2)):-agent(R),color(C2),color(C1).
exec(place(R,C1,C2),neg(free_gripper(R))):-agent(R),color(C2),color(C1).
exec(place(R,C1,C2),gripped(R,C1)):-agent(R),color(C2),color(C1).
exec(place(R,C1,C2),owner(R,C1)):-agent(R),color(C2),color(C1).
exec(place_on_ground(R,C1,S),free_stack(S)):-agent(R),stack(S),color(C1).
exec(place_on_ground(R,C1,S),neg(free_gripper(R))):-agent(R),stack(S),color(C1).
exec(place_on_ground(R,C1,S),gripped(R,C1)):-agent(R),stack(S),color(C1).
exec(place_on_ground(R,C1,S),owner(R,C1)):-agent(R),stack(S),color(C1).
exec(pick_from_table(R,C1),table(C1)):-agent(R),color(C1).
exec(pick_from_table(R,C1),neg(free_table)):-agent(R),color(C1).
exec(pick_from_table(R,C1),free_gripper(R)):-agent(R),color(C1).
exec(place_on_table(R,C1),free_table):-agent(R),color(C1).
exec(place_on_table(R,C1),neg(free_gripper(R))):-agent(R),color(C1).
exec(place_on_table(R,C1),gripped(R,C1)):-agent(R),color(C1).
exec(place_on_table(R,C1),owner(R,C1)):-agent(R),color(C1).


%%%%%%%%%% CAUSES %%%%%%%%%%

causes(pick(R,C1,C2),neg(top_block(C1))):-agent(R),color(C2),color(C1).
causes(pick(R,C1,C2),neg(on_block(C1,C2))):-agent(R),color(C2),color(C1).
causes(pick(R,C1,C2),top_block(C2)):-agent(R),color(C2),color(C1).
causes(pick(R,C1,C2),neg(free_gripper(R))):-agent(R),color(C2),color(C1).
causes(pick(R,C1,C2),gripped(R,C1)):-agent(R),color(C2),color(C1).
causes(pick_from_ground(R,C1,S),free_stack(S)):-agent(R),stack(S),color(C1).
causes(pick_from_ground(R,C1,S),neg(top_block(C1))):-agent(R),stack(S),color(C1).
causes(pick_from_ground(R,C1,S),neg(on_stack(C1,S))):-agent(R),stack(S),color(C1).
causes(pick_from_ground(R,C1,S),neg(free_gripper(R))):-agent(R),stack(S),color(C1).
causes(pick_from_ground(R,C1,S),gripped(R,C1)):-agent(R),stack(S),color(C1).
causes(place(R,C1,C2),top_block(C1)):-agent(R),color(C2),color(C1).
causes(place(R,C1,C2),on_block(C1,C2)):-agent(R),color(C2),color(C1).
causes(place(R,C1,C2),neg(top_block(C2))):-agent(R),color(C2),color(C1).
causes(place(R,C1,C2),free_gripper(R)):-agent(R),color(C2),color(C1).
causes(place(R,C1,C2),neg(gripped(R,C1))):-agent(R),color(C2),color(C1).
causes(place_on_ground(R,C1,S),neg(free_stack(S))):-agent(R),stack(S),color(C1).
causes(place_on_ground(R,C1,S),top_block(C1)):-agent(R),stack(S),color(C1).
causes(place_on_ground(R,C1,S),free_gripper(R)):-agent(R),stack(S),color(C1).
causes(place_on_ground(R,C1,S),neg(gripped(R,C1))):-agent(R),stack(S),color(C1).
causes(pick_from_table(R,C1),neg(table(C1))):-agent(R),color(C1).
causes(pick_from_table(R,C1),free_table):-agent(R),color(C1).
causes(pick_from_table(R,C1),neg(free_gripper(R))):-agent(R),color(C1).
causes(pick_from_table(R,C1),gripped(R,C1)):-agent(R),color(C1).
causes(pick_from_table(R,C1),owner(R,C1)):-agent(R),color(C1).
causes(place_on_table(R,C1),neg(free_table)):-agent(R),color(C1).
causes(place_on_table(R,C1),neg(owner(R,C1))):-agent(R),color(C1).
causes(place_on_table(R,C1),table(C1)):-agent(R),color(C1).
causes(place_on_table(R,C1),free_gripper(R)):-agent(R),color(C1).
causes(place_on_table(R,C1),neg(gripped(R,C1))):-agent(R),color(C1).


%%%%%%%%%% GOALS %%%%%%%%%%

goal(owner(alice,black)).


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
