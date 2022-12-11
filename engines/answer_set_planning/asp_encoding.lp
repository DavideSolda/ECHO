%Answer set planning.

%Answer set planning: A Survey. E. Pontelli et al. For a survey.
%Epistemic Multiagent Reasoning with Collaborative Robots: D. Solda' el al. For a practical use-case.



%%%%%%%%%% [[	PROBLEM DEPENDENT RULES	]] %%%%%%%%%%



%%%%%%%%%% TYPES %%%%%%%%%%

table(table1;table2;table3).


%%%%%%%%%% FLUENTS %%%%%%%%%%

fluent(loaded(X)):-table(X).
fluent(moved(X)):-table(X).
fluent(ready(X)):-table(X).


%%%%%%%%%% INITIALLY %%%%%%%%%%

holds(loaded(table1), 0).
holds(loaded(table2), 0).


%%%%%%%%%% ACTIONS %%%%%%%%%%

action(pick(TABLE)):-table(TABLE).
action(move(TABLE)):-table(TABLE).
action(place(TABLE)):-table(TABLE).


%%%%%%%%%% EXECUTABLE %%%%%%%%%%

action_exec(pick(TABLE),loaded(TABLE)):-table(TABLE).
action_exec(move(TABLE),neg(loaded(TABLE))):-table(TABLE).
action_exec(place(TABLE),neg(loaded(TABLE))):-table(TABLE).


%%%%%%%%%% CAUSES %%%%%%%%%%

causes(pick(TABLE),neg(loaded(TABLE))):-table(TABLE).
causes(move(TABLE),moved(TABLE)):-table(TABLE).
causes(place(TABLE),loaded(TABLE)):-table(TABLE).
causes(place(TABLE),ready(TABLE)):-table(TABLE).


%%%%%%%%%% METHODS %%%%%%%%%%

method(lighten_up(TABLE)):-table(TABLE).


%%%%%%%%%% EXECUTABLE %%%%%%%%%%

method_exec(lighten_up(TABLE),loaded(TABLE)):-table(TABLE).


%%%%%%%%%% METHOD_GOAL_REFINEMENT %%%%%%%%%%

method_req(lighten_up(TABLE), picked_g(TABLE), moved_g(TABLE)):-table(TABLE).
method_req(lighten_up(TABLE), moved_g(TABLE), placed_g(TABLE)):-table(TABLE).
method_req_end(lighten_up(TABLE), placed_g(TABLE)):-table(TABLE).


%%%%%%%%%% GOAL DNF %%%%%%%%%%

goal_DNF(moved_g(TABLE), moved(TABLE)):-table(TABLE).
goal_DNF(placed_g(TABLE), loaded(TABLE)):-table(TABLE).
goal_DNF(placed_g(TABLE), ready(TABLE)):-table(TABLE).
goal_DNF(ready_g(TABLE), ready(TABLE)):-table(TABLE).
goal_DNF(picked_g(TABLE), neg(loaded(TABLE))):-table(TABLE).


%%%%%%%%%% GOAL %%%%%%%%%%

goal(moved_g(TABLE)):-table(TABLE).
goal(placed_g(TABLE)):-table(TABLE).
goal(ready_g(TABLE)):-table(TABLE).
goal(picked_g(TABLE)):-table(TABLE).


%%%%%%%%%% GOAL TO SAT %%%%%%%%%%

prec_to_sat(ready_g(table1), 0,ready_g(table2), 0).
goal_to_sat(ready_g(table1), 0, 0).
goal_to_sat(ready_g(table2), 0, 0).
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
not_executable(A,t):-action_exec(A,F), fluent(F), not holds(F,t).
not_executable(A,t):-action_exec(A,NOTF), opposite(F, NOTF), holds(F,t).
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
