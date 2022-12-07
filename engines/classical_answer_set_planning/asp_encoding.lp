%Answer set planning.

%Answer set planning: A Survey. E. Pontelli et al. For a survey.
%Epistemic Multiagent Reasoning with Collaborative Robots: D. Solda' el al. For a practical use-case.



%%%%%%%%%% [[	PROBLEM DEPENDENT RULES	]] %%%%%%%%%%



%%%%%%%%%% TYPES %%%%%%%%%%

integer(1..3).
color(red;orange;yellow).
s(red;orange;yellow,1..3).


%%%%%%%%%% FLUENTS %%%%%%%%%%

fluent(f1(A, B)):-color(A),integer(B).
fluent(f3(X)):-color(X).
fluent(f_b).


%%%%%%%%%% INITIALLY %%%%%%%%%%

holds(f1(red,1), 1).
holds(f3(orange), 1).
holds(f1(orange,2), 1).


%%%%%%%%%% ACTIONS %%%%%%%%%%

action(action_1(X)):-integer(X).
action(action_2).


%%%%%%%%%% EXECUTABLE %%%%%%%%%%

exec(action_1(X),f1(red,X)):-integer(X),integer(X).
exec(action_1(X),f3(orange)):-integer(X).


%%%%%%%%%% CAUSES %%%%%%%%%%

causes(action_1(X),f1(yellow,X)):-integer(X),integer(X).
causes(action_1(X),neg(f1(red,X))):-integer(X),integer(X).
causes(action_2,neg(f3(orange))).
causes(action_2,boolean_fluent).


%%%%%%%%%% GOALS %%%%%%%%%%

goal(f1(yellow,1)).
goal(neg(f3(orange))).


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
:- goal(F), not holds(F,t), query(t).
:- goal(neg(F)), holds(F,t), query(t).
#program base.
