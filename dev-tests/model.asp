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

holds(f1(red,1), 0).
holds(f1(orange,2), 0).


%%%%%%%%%% ACTIONS %%%%%%%%%%

action(from_red_to_yellow(X)):-integer(X).


%%%%%%%%%% EXECUTABLE %%%%%%%%%%

exec(from_red_to_yellow(X),f1(red,X)).
exec(from_red_to_yellow(X),f3(orange)).


%%%%%%%%%% CAUSES %%%%%%%%%%

causes(from_red_to_yellow(X),f1(yellow,X)).


%%%%%%%%%% GOALS %%%%%%%%%%

goal(f1(orange,2)).


%%%%%%%%%% [[	PROBLEM INDEPENDENT RULES	]] %%%%%%%%%%

time(1..l).
not_goal(T) :- time(T), goal(F), holds(F,T).
goal(T) :- time(T), not holds(F, T).
:- not goal(l).
opposite(F, neg(F)).
opposite(neg(f), F).
not_executable(A,T) :- exec(A,F), not holds(F,T).
executable(A,T) :- T < l, not not_executable(A,T).
holds(F, T+1) :- T < l, executalbe(A,T), occurs(A,T), causes(A,F).
holds(F,T+1) :- opposite(F,G), T < l, holds(F,T), not holds(G, T+1).
occurs(A,T) :- action(A), time(T), not goal(T), not not_occurs(A,T).
not_occurs(A,T) :- action(A), action(B), time(T), occurs(B,T), A!=B.
:- action(A), time(T), occurs(A,T), not executable(A,T).
