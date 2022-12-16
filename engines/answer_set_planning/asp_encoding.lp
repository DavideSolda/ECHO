%Answer set planning.

%Answer set planning: A Survey. E. Pontelli et al. For a survey.
%Epistemic Multiagent Reasoning with Collaborative Robots: D. Solda' el al. For a practical use-case.



%%%%%%%%%% [[	PROBLEM DEPENDENT RULES	]] %%%%%%%%%%



%%%%%%%%%% TYPES %%%%%%%%%%

agent(alice;bob).
stack(1..3).
color(red;orange;yellow;black).


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
fluent(in_front_of(A, B)):-agent(A),stack(B).


%%%%%%%%%% INITIALLY %%%%%%%%%%

holds(on_stack(red,1), 1).
holds(on_block(black,red), 1).
holds(top_block(black), 1).
holds(on_stack(orange,2), 1).
holds(top_block(orange), 1).
holds(free_gripper(bob), 1).
holds(free_gripper(alice), 1).
holds(free_stack(3), 1).
holds(owner(bob,red), 1).
holds(owner(bob,black), 1).
holds(owner(bob,orange), 1).
holds(in_front_of(bob,1), 1).
holds(in_front_of(bob,2), 1).
holds(in_front_of(alice,3), 1).
holds(free_table, 1).


%%%%%%%%%% ACTIONS %%%%%%%%%%

action(pick(R,C1,C2,C3)):-agent(R),color(C1),color(C2),color(C3).
action(pick_from_ground(R,C1,S)):-agent(R),color(C1),stack(S).
action(place(R,C1,C2,S)):-agent(R),color(C1),color(C2),stack(S).
action(place_on_ground(R,C1,S)):-agent(R),color(C1),stack(S).
action(pick_from_table(R,C1)):-agent(R),color(C1).
action(place_on_table(R,C1)):-agent(R),color(C1).


%%%%%%%%%% EXECUTABLE %%%%%%%%%%

exec(pick(R,C1,C2,C3),top_block(C1)):-color(C1),agent(R),color(C3),color(C2).
exec(pick(R,C1,C2,C3),on_block(C1,C2)):-color(C1),agent(R),color(C3),color(C2).
exec(pick(R,C1,C2,C3),free_gripper(R)):-color(C1),agent(R),color(C3),color(C2).
exec(pick(R,C1,C2,C3),owner(R,C1)):-color(C1),agent(R),color(C3),color(C2).
exec(pick_from_ground(R,C1,S),in_front_of(R,S)):-stack(S),color(C1),agent(R).
exec(pick_from_ground(R,C1,S),top_block(C1)):-stack(S),color(C1),agent(R).
exec(pick_from_ground(R,C1,S),on_stack(C1,S)):-stack(S),color(C1),agent(R).
exec(pick_from_ground(R,C1,S),free_gripper(R)):-stack(S),color(C1),agent(R).
exec(pick_from_ground(R,C1,S),owner(R,C1)):-stack(S),color(C1),agent(R).
exec(place(R,C1,C2,S),top_block(C2)):-stack(S),color(C1),agent(R),color(C2).
exec(place(R,C1,C2,S),neg(free_gripper(R))):-stack(S),color(C1),agent(R),color(C2).
exec(place(R,C1,C2,S),gripped(R,C1)):-stack(S),color(C1),agent(R),color(C2).
exec(place(R,C1,C2,S),owner(R,C1)):-stack(S),color(C1),agent(R),color(C2).
exec(place(R,C1,C2,S),owner(R,C2)):-stack(S),color(C1),agent(R),color(C2).
exec(place_on_ground(R,C1,S),free_stack(S)):-stack(S),color(C1),agent(R).
exec(place_on_ground(R,C1,S),neg(free_gripper(R))):-stack(S),color(C1),agent(R).
exec(place_on_ground(R,C1,S),gripped(R,C1)):-stack(S),color(C1),agent(R).
exec(place_on_ground(R,C1,S),owner(R,C1)):-stack(S),color(C1),agent(R).
exec(place_on_ground(R,C1,S),in_front_of(R,S)):-stack(S),color(C1),agent(R).
exec(pick_from_table(R,C1),table(C1)):-color(C1),agent(R).
exec(pick_from_table(R,C1),neg(free_table)):-color(C1),agent(R).
exec(pick_from_table(R,C1),free_gripper(R)):-color(C1),agent(R).
exec(place_on_table(R,C1),free_table):-color(C1),agent(R).
exec(place_on_table(R,C1),neg(free_gripper(R))):-color(C1),agent(R).
exec(place_on_table(R,C1),gripped(R,C1)):-color(C1),agent(R).
exec(place_on_table(R,C1),owner(R,C1)):-color(C1),agent(R).


%%%%%%%%%% CAUSES %%%%%%%%%%

causes(pick(R,C1,C2,C3),neg(top_block(C1))):-color(C1),agent(R),color(C3),color(C2).
causes(pick(R,C1,C2,C3),neg(on_block(C1,C2))):-color(C1),agent(R),color(C3),color(C2).
causes(pick(R,C1,C2,C3),top_block(C2)):-color(C1),agent(R),color(C3),color(C2).
causes(pick(R,C1,C2,C3),neg(free_gripper(R))):-color(C1),agent(R),color(C3),color(C2).
causes(pick(R,C1,C2,C3),gripped(R,C1)):-color(C1),agent(R),color(C3),color(C2).
causes(pick_from_ground(R,C1,S),free_stack(S)):-stack(S),color(C1),agent(R).
causes(pick_from_ground(R,C1,S),neg(top_block(C1))):-stack(S),color(C1),agent(R).
causes(pick_from_ground(R,C1,S),neg(on_stack(C1,S))):-stack(S),color(C1),agent(R).
causes(pick_from_ground(R,C1,S),neg(free_gripper(R))):-stack(S),color(C1),agent(R).
causes(pick_from_ground(R,C1,S),gripped(R,C1)):-stack(S),color(C1),agent(R).
causes(place(R,C1,C2,S),top_block(C1)):-stack(S),color(C1),agent(R),color(C2).
causes(place(R,C1,C2,S),on_block(C1,C2)):-stack(S),color(C1),agent(R),color(C2).
causes(place(R,C1,C2,S),neg(top_block(C2))):-stack(S),color(C1),agent(R),color(C2).
causes(place(R,C1,C2,S),free_gripper(R)):-stack(S),color(C1),agent(R),color(C2).
causes(place(R,C1,C2,S),neg(gripped(R,C1))):-stack(S),color(C1),agent(R),color(C2).
causes(place_on_ground(R,C1,S),neg(free_stack(S))):-stack(S),color(C1),agent(R).
causes(place_on_ground(R,C1,S),top_block(C1)):-stack(S),color(C1),agent(R).
causes(place_on_ground(R,C1,S),free_gripper(R)):-stack(S),color(C1),agent(R).
causes(place_on_ground(R,C1,S),neg(gripped(R,C1))):-stack(S),color(C1),agent(R).
causes(pick_from_table(R,C1),neg(table(C1))):-color(C1),agent(R).
causes(pick_from_table(R,C1),free_table):-color(C1),agent(R).
causes(pick_from_table(R,C1),neg(free_gripper(R))):-color(C1),agent(R).
causes(pick_from_table(R,C1),gripped(R,C1)):-color(C1),agent(R).
causes(pick_from_table(R,C1),owner(R,C1)):-color(C1),agent(R).
causes(place_on_table(R,C1),neg(free_table)):-color(C1),agent(R).
causes(place_on_table(R,C1),neg(owner(R,C1))):-color(C1),agent(R).
causes(place_on_table(R,C1),table(C1)):-color(C1),agent(R).
causes(place_on_table(R,C1),free_gripper(R)):-color(C1),agent(R).
causes(place_on_table(R,C1),neg(gripped(R,C1))):-color(C1),agent(R).


%%%%%%%%%% METHODS %%%%%%%%%%

method(move_to_top(R,C1,C2,C3)):-agent(R),color(C1),color(C2),color(C3), C3!=C2.
method(move_to_ground(R,C1,C2,S)):-agent(R),color(C1),color(C2),stack(S).


%%%%%%%%%% EXECUTABLE %%%%%%%%%%

method_exec(move_to_top(R,C1,C2,C3),on_block(C1,C2)):-color(C1),agent(R),color(C3),color(C2).
method_exec(move_to_top(R,C1,C2,C3),top_block(C3)):-color(C1),agent(R),color(C3),color(C2).
method_exec(move_to_ground(R,C1,C2,S),on_block(C1,C2)):-stack(S),color(C1),agent(R),color(C2).
method_exec(move_to_ground(R,C1,C2,S),free_stack(S)):-stack(S),color(C1),agent(R),color(C2).


%%%%%%%%%% METHOD_GOAL_REFINEMENT %%%%%%%%%%

method_req(move_to_top(R,C1,C2,C3), picked_g(R,C1), on_g(C1,C3)):-agent(R),color(C1),color(C2),color(C3).
method_req(move_to_top(R,C1,C2,C3), on_g(C1,C3), picked_g(R,C2)):-agent(R),color(C1),color(C2),color(C3).
method_req_end(move_to_top(R,C1,C2,C3), picked_g(R,C2)):-agent(R),color(C1),color(C2),color(C3).
method_req(move_to_ground(R,C1,C2,S), picked_g(R,C1), on_table_g(C1)):-agent(R),color(C1),color(C2),stack(S).
method_req(move_to_ground(R,C1,C2,S), on_table_g(C1), picked_g(R,C2)):-agent(R),color(C1),color(C2),stack(S).
method_req_end(move_to_ground(R,C1,C2,S), picked_g(R,C2)):-agent(R),color(C1),color(C2),stack(S).


%%%%%%%%%% GOAL DNF %%%%%%%%%%

goal_DNF(top_g(C1), top_block(C1)):-color(C1).
goal_DNF(picked_g(R,C1), gripped(R,C1)):-agent(R),color(C1).
goal_DNF(on_g(C1,C2), on_block(C1,C2)):-color(C1),color(C2).
goal_DNF(on_table_g(C1), table(C1)):-color(C1).


%%%%%%%%%% GOAL %%%%%%%%%%

goal(top_g(C1)):-color(C1).
goal(picked_g(R,C1)):-agent(R),color(C1).
goal(on_g(C1,C2)):-color(C1),color(C2).
goal(on_table_g(C1)):-color(C1).


%%%%%%%%%% GOAL TO SAT %%%%%%%%%%

goal_to_sat(picked_g(bob,red), 1, 1).
#program step(t).
%creation of new subgoals.
goal_to_sat(G, t+1, t+1):-occurs(M, t), method_req(M, G, G2), goal(G).
goal_to_sat(G, t+1, t+1):-occurs(M, t), method_req_end(M, G), goal(G).
prec_to_sat(G1, t+1, G2, t+1):-occurs(M, t), method_req(M, G1, G2).
%definition of minimal goal.
not_minimal(G2, T2, t):-prec_to_sat(G1, T1, G2, T2), goal_to_sat(G1,T1,t), goal_to_sat(G2, T2, t).
not_minimal(G2, T2, t):-goal_to_sat(G1,T1,t), goal_to_sat(G2, T2, t), T2<T1.
minimal(G, T1, t):-goal_to_sat(G, T1, t), not not_minimal(G, T1, t).
0{selected_sub_goal(G, T1, t):minimal(G, T1, t)}1.
%executability for methods:.
not_executable(M, t):-method_exec(M,F), fluent(F), not holds(F,t).
not_executable(M, t):-method_exec(M,F), opposite(F, NOTF), holds(NOTF,t).
not_relevant(M,t):-method(M), goal_DNF(MG,F), method_req_end(M, MG), selected_sub_goal(SG, ST, t), goal_DNF(SG, NOTF), opposite(F,NOTF).
relevant(M,t):-method(M), selected_sub_goal(SG, ST, t), goal_DNF(SG, F), method_req_end(M, MG), goal_DNF(MG, F), not not_relevant(M,t).
executable(M,t):-method(M), not not_executable(M,t), relevant(M,t).
:- not executable(M,t), occurs(M,t), method(M).
%executability for actions:.
not_executable(A,t):-exec(A,F), fluent(F), not holds(F,t).
not_executable(A,t):-exec(A,NOTF), opposite(F, NOTF), holds(F,t).
not_relevant(A,t):-action(A), selected_sub_goal(SG, ST, t), goal_DNF(SG, NOTF), causes(A,F), opposite(F, NOTF).
relevant(A,t):-action(A), selected_sub_goal(SG, ST, t), goal_DNF(SG, F), causes(A,F), not not_relevant(A,t).
executable(A, t):-action(A), not not_executable(A, t), relevant(A, t).
:- not executable(A, t), occurs(A, t), action(A).
%inertia for fluents:.
holds(F, t+1):-holds(F, t), opposite(F, G), not holds(G, t+1).
%opposite definition.
opposite(F, neg(F)):-fluent(F).
opposite(neg(F), F):-fluent(F).
%at most one action/method at a time:.
{occurs(A,t):action(A)}.
{occurs(M,t):method(M)}.
:-occurs(A,t), occurs(M,t), A!=M.
%action effects:.
holds(F, t+1):-action(A), occurs(A,t), causes(A,F).
%inertia for subgoals.
action_occurs(t):-occurs(A,t), action(A).
not_sat(G, t+1):-goal_DNF(G, F), holds(NOTF, t+1), opposite(NOTF ,F), goal(G).
not_sat(G, t+1):-goal_DNF(G, F), fluent(F), not holds(F, t+1), goal(G).
goal_to_sat(G, T1, t+1):- goal_to_sat(G, T1, t), not action_occurs(t).
goal_to_sat(G, T1, t+1):- not_sat(G, t+1), goal_to_sat(G, T1, t), action_occurs(t).
#program check(t).
:- goal_to_sat(G, T, t), query(t).
