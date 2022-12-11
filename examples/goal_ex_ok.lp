time(0..horizon).

table(a;b;c).

fluent(loaded(TABLE)):-table(TABLE).
fluent(moved(TABLE)):-table(TABLE).
fluent(ready(TABLE)):-table(TABLE).

%a method to ligthen up the weigth on a table for a while
method(lighten_up(TABLE)):-table(TABLE).

%subgoals:
method_req(lighten_up(TABLE), picked_g(TABLE), moved_g(TABLE)):-table(TABLE).
method_req(lighten_up(TABLE), moved_g(TABLE), placed_g(TABLE)):-table(TABLE).
method_req_end(lighten_up(TABLE), placed_g(TABLE)):-table(TABLE).

%executability for method:
method_exec(lighten_up(TABLE), loaded(TABLE)):-table(TABLE).

%express what goals stand for:
goal_DNF(picked_g(TABLE), neg(loaded(TABLE))):-table(TABLE).
goal_DNF(placed_g(TABLE), loaded(TABLE)):-table(TABLE).
goal_DNF(moved_g(TABLE), moved(TABLE)):-table(TABLE).
goal_DNF(placed_g(TABLE), ready(TABLE)):-table(TABLE).
goal_DNF(ready_g(TABLE), ready(TABLE)):-table(TABLE).

goal(picked_g(TABLE)):-table(TABLE).
goal(placed_g(TABLE)):-table(TABLE).
goal(moved_g(TABLE)):-table(TABLE).
goal(ready_g(TABLE)):-table(TABLE).

%actions:
action(pick(TABLE)):-table(TABLE).
action(place(TABLE)):-table(TABLE).
action(move(TABLE)):-table(TABLE).

%effect of actions:
causes(pick(TABLE), neg(loaded(TABLE))):-table(TABLE).
causes(place(TABLE), loaded(TABLE)):-table(TABLE).
causes(place(TABLE), ready(TABLE)):-table(TABLE).
causes(move(TABLE), moved(TABLE)):-table(TABLE).

%executability for action:
action_exec(pick(TABLE), loaded(TABLE)):-table(TABLE).
action_exec(place(TABLE), neg(loaded(TABLE))):-table(TABLE).
action_exec(move(TABLE), neg(loaded(TABLE))):-table(TABLE).

%initially fluents:
holds(loaded(a), 0).
holds(loaded(b), 0).
holds(neg(loaded(c)), 0).
holds(neg(ready(TABLE)), 0):-table(TABLE).
holds(neg(moved(TABLE)), 0):-table(TABLE).

%initially goals:
goal_to_sat(ready_g(a), 0, 0).
goal_to_sat(ready_g(b), 0, 0).
%goal_to_sat(picked(a), 0, 0).


%%DOMAIN INDEPENDENT RULES:

%creation of new subgoals
goal_to_sat(G, T+1, T+1):-occurs(M, T), method_req(M, G, G2), time(T), goal(G).
goal_to_sat(G, T+1, T+1):-occurs(M, T), method_req_end(M, G), time(T), goal(G).
prec_to_sat(G1, T+1, G2, T+1):-occurs(M, T), method_req(M, G1, G2), time(T).
prec_to_sat(G1, T1, G2, T2):-T2<T1, goal_to_sat(G1, T1, T), goal_to_sat(G2, T2, T).

%definition of minimal goal
not_minimal(G2, T2, T):-prec_to_sat(G1, T1, G2, T2), goal_to_sat(G1,T1,T), goal_to_sat(G2, T2, T).

%selected_sub_goal(goal_to_sat(G, T1, T), T):-not not_selected_sub_goal(goal_to_sat(G, T1, T), T), goal_to_sat(G, T1, T).
minimal(G, T1, T):-goal_to_sat(G, T1, T), not not_minimal(G, T1, T).

1{selected_sub_goal(G, T1, T):minimal(G, T1, T)}1:-time(T), goal_to_sat(G2, T2, T).

%executability for methods:
not_executable(M,T):-method_exec(M,F), holds(F2,T), opposite(F, F2), time(T).
not_relevant(M,T):-method(M), time(T), T<horizon, goal_DNF(MG,F), method_req_end(M, MG), selected_sub_goal(SG, ST, T), goal_DNF(SG, NOTF), opposite(F,NOTF).
relevant(M,T):-method(M), time(T), T<horizon, selected_sub_goal(SG, ST, T), goal_DNF(SG, F), method_req_end(M, MG), goal_DNF(MG, F), not not_relevant(M,T).
executable(M,T):-method(M), not not_executable(M,T), T<horizon, time(T), relevant(M,T).
:- not executable(M,T), occurs(M,T), method(M).

%executability for actions:
not_executable(A,T):-action_exec(A,F), not holds(F,T), time(T).
not_relevant(A,T):-action(A), time(T), T<horizon, selected_sub_goal(SG, ST, T), goal_DNF(SG, NOTF), causes(A,F), opposite(F, NOTF).
relevant(A,T):-action(A), time(T), T<horizon, selected_sub_goal(SG, ST, T), goal_DNF(SG, F), causes(A,F), not not_relevant(A,T).
executable(A,T):-action(A), not not_executable(A,T), T<horizon, time(T), relevant(A, T).
:- not executable(A,T), occurs(A,T), action(A).


%inertia for fluents:
holds(F, T+1):-holds(F, T), T<horizon, opposite(F, G), not holds(G, T+1).

%opposite definition
opposite(F, neg(F)):-fluent(F).
opposite(neg(F), F):-fluent(F).

%at most one action/method at a time:
{occurs(A,T):action(A)}:-time(T).
{occurs(M,T):method(M)}:-time(T).
:-occurs(A,T), occurs(M,T), A!=M.

%action effects:
holds(F, T+1):-action(A), occurs(A,T), causes(A,F).

%inertia for subgoals
action_occurs(T):-occurs(A,T), action(A).
not_sat(G, T):-goal_DNF(G, F), holds(F2, T), opposite(F2 ,F), goal(G).
goal_to_sat(G, T1, T+1):-T<horizon,  goal_to_sat(G, T1, T), not action_occurs(T).
goal_to_sat(G, T1, T+1):- not_sat(G, T+1), goal_to_sat(G, T1, T), action_occurs(T).

:- goal_to_sat(G, T, horizon).
g(G) :- goal_to_sat(G, T, horizon).