%Answer set planning.

%Answer set planning: A Survey. E. Pontelli et al. For a survey.
%Epistemic Multiagent Reasoning with Collaborative Robots: D. Solda' el al. For a practical use-case.



%%%%%%%%%% [[	PROBLEM DEPENDENT RULES	]] %%%%%%%%%%



%%%%%%%%%% TYPES %%%%%%%%%%

agent(alice;bob;mario;giangiovanni).
color(red;black;gray;red;violet).


%%%%%%%%%% FLUENTS %%%%%%%%%%

fluent(connected_via_phone(A, B)):-agent(A),agent(B).
fluent(digited(A, B)):-agent(A),agent(B).
fluent(calling(A, B)):-agent(A),agent(B).
fluent(closed(A, B)):-agent(A),agent(B).


%%%%%%%%%% INITIALLY %%%%%%%%%%

holds(connected_via_phone(alice,bob), 1).
holds(connected_via_phone(alice,mario), 1).
holds(connected_via_phone(mario,giangiovanni), 1).


%%%%%%%%%% ACTIONS %%%%%%%%%%

action(digit(R1,R2)):-agent(R1),agent(R2).
action(call(R1,R2)):-agent(R1),agent(R2).
action(close(R1,R2)):-agent(R1),agent(R2).
action(a_1(C1,C2)):-color(C1),color(C2).
action(a_2(C1,C2)):-color(C1),color(C2).
action(a_3(C1,C2)):-color(C1),color(C2).
action(a_4(C1,C2)):-color(C1),color(C2).
action(a_5(C1,C2)):-color(C1),color(C2).
action(a_6(C1,C2)):-color(C1),color(C2).
action(a_7(C1,C2)):-color(C1),color(C2).
action(a_8(C1,C2)):-color(C1),color(C2).
action(a_9(C1,C2)):-color(C1),color(C2).
action(a_10(C1,C2)):-color(C1),color(C2).
action(a_11(C1,C2)):-color(C1),color(C2).
action(a_12(C1,C2)):-color(C1),color(C2).
action(a_13(C1,C2)):-color(C1),color(C2).
action(a_14(C1,C2)):-color(C1),color(C2).
action(a_15(C1,C2)):-color(C1),color(C2).
action(a_16(C1,C2)):-color(C1),color(C2).
action(a_17(C1,C2)):-color(C1),color(C2).
action(a_18(C1,C2)):-color(C1),color(C2).
action(a_19(C1,C2)):-color(C1),color(C2).
action(a_20(C1,C2)):-color(C1),color(C2).
action(a_21(C1,C2)):-color(C1),color(C2).
action(a_22(C1,C2)):-color(C1),color(C2).
action(a_23(C1,C2)):-color(C1),color(C2).
action(a_24(C1,C2)):-color(C1),color(C2).
action(a_25(C1,C2)):-color(C1),color(C2).
action(a_26(C1,C2)):-color(C1),color(C2).
action(a_27(C1,C2)):-color(C1),color(C2).
action(a_28(C1,C2)):-color(C1),color(C2).
action(a_29(C1,C2)):-color(C1),color(C2).
action(a_30(C1,C2)):-color(C1),color(C2).
action(a_31(C1,C2)):-color(C1),color(C2).
action(a_32(C1,C2)):-color(C1),color(C2).
action(a_33(C1,C2)):-color(C1),color(C2).
action(a_34(C1,C2)):-color(C1),color(C2).
action(a_35(C1,C2)):-color(C1),color(C2).
action(a_36(C1,C2)):-color(C1),color(C2).
action(a_37(C1,C2)):-color(C1),color(C2).
action(a_38(C1,C2)):-color(C1),color(C2).
action(a_39(C1,C2)):-color(C1),color(C2).
action(a_40(C1,C2)):-color(C1),color(C2).
action(a_41(C1,C2)):-color(C1),color(C2).
action(a_42(C1,C2)):-color(C1),color(C2).
action(a_43(C1,C2)):-color(C1),color(C2).
action(a_44(C1,C2)):-color(C1),color(C2).
action(a_45(C1,C2)):-color(C1),color(C2).
action(a_46(C1,C2)):-color(C1),color(C2).
action(a_47(C1,C2)):-color(C1),color(C2).
action(a_48(C1,C2)):-color(C1),color(C2).
action(a_49(C1,C2)):-color(C1),color(C2).


%%%%%%%%%% EXECUTABLE %%%%%%%%%%

exec(digit(R1,R2),connected_via_phone(R1,R2)):-agent(R1),agent(R2).
exec(call(R1,R2),connected_via_phone(R1,R2)):-agent(R1),agent(R2).
exec(call(R1,R2),digited(R1,R2)):-agent(R1),agent(R2).
exec(close(R1,R2),connected_via_phone(R1,R2)):-agent(R1),agent(R2).
exec(close(R1,R2),calling(R1,R2)):-agent(R1),agent(R2).


%%%%%%%%%% CAUSES %%%%%%%%%%

causes(digit(R1,R2),digited(R1,R2)):-agent(R1),agent(R2).
causes(call(R1,R2),neg(digited(R1,R2))):-agent(R1),agent(R2).
causes(call(R1,R2),calling(R1,R2)):-agent(R1),agent(R2).
causes(close(R1,R2),neg(calling(R1,R2))):-agent(R1),agent(R2).
causes(close(R1,R2),closed(R1,R2)):-agent(R1),agent(R2).


%%%%%%%%%% GOALS %%%%%%%%%%

goal(closed(alice,bob)).
goal(closed(alice,mario)).


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
