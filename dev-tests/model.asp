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
holds(f3(orange), 0).
holds(f1(orange,2), 0).


%%%%%%%%%% ACTIONS %%%%%%%%%%

action(from_red_to_yellow(X)):-integer(X).


%%%%%%%%%% EXECUTABLE %%%%%%%%%%

exec(from_red_to_yellow(X),f1(red,X)):-integer(X).
exec(from_red_to_yellow(X),f3(orange)):-integer(X).


%%%%%%%%%% CAUSES %%%%%%%%%%

causes(from_red_to_yellow(X),f1(yellow,X)):-integer(X).
causes(from_red_to_yellow(X),neg(f1(red,X))):-integer(X).


%%%%%%%%%% GOALS %%%%%%%%%%

goal(f1(yellow,1)).


%%%%%%%%%% [[	PROBLEM INDEPENDENT RULES	]] %%%%%%%%%%

time(0..l).
opposite(F, neg(F)) :- fluent(F).
opposite(neg(f), F) :- fluent(F).
holds(F,T+1) :- opposite(F,G), T < l, holds(F,T), not holds(G, T+1).
not_goal_at(T) :- time(T), not holds(F, T), goal(F), fluent(F).
:- not_goal_at(l).
not_executable(A,T) :- exec(A,F), not holds(F,T), time(T).
executable(A,T) :- T < l, not not_executable(A,T), time(T), action(A).
holds(F, T+1) :- T < l, executable(A,T), occurs(A,T), causes(A,F).
{occurs(A,T) : action(A)}1 :- time(T).
:- action(A), time(T), occurs(A,T), not executable(A,T).
#show holds/2.
#show occurs/2.
