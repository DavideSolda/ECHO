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


%%%%%%%%%% INITIALLY %%%%%%%%%%

holds(f1(red,1), 0).


%%%%%%%%%% ACTIONS %%%%%%%%%%



%%%%%%%%%% EXECUTABLE %%%%%%%%%%



%%%%%%%%%% CAUSES %%%%%%%%%%



%%%%%%%%%% GOALS %%%%%%%%%%

goal(f1(yellow,1)).


%%%%%%%%%% [[	PROBLEM INDEPENDENT RULES	]] %%%%%%%%%%

opposite(F, neg(F)) :- fluent(F).
opposite(neg(F), F) :- fluent(F).
#program step(t).
holds(F,t+1) :- opposite(F,G), holds(F,t), not holds(G, t+1).
not_goal_at(t) :- not holds(F, t), goal(F).
:- not_goal_at(t), goal_at(t).
not_executable(A,t) :- exec(A,F), not holds(F,t).
executable(A,t) :- not not_executable(A,t), action(A).
holds(F, t+1) :- executable(A,t), occurs(A,t), causes(A,F).
{occurs(A,t) : action(A)}1.
:- action(A), occurs(A,t), not executable(A,t).
#program check(t).
:- goal_on(D,P), not on(D,P,t), query(t).
finally(F):- holds(F,t), query(t).
#program base.

#program t_program(f).
time(f).
#external goal_at(f).
