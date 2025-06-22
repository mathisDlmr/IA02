size([], 0).
size([_|R], N) :- size(R, N2), N is N2+1.

sum([], 0).
sum([H|R], N) :- sum(R, N2), N is N2+H.

split([], [], []).
split([H|T], [H|T1], T2) :- split(T, T1, T2).  % On met dans T1
split([H|T], T1, [H|T2]) :- split(T, T1, T2).  % Ou T2

deux_partition(L, L1, L2) :-
    split(L, L1, L2),
    sum(L1, X),
    sum(L2, X).

check_sum([H|R], S) :-
    sum(H, S),
    check_sum(R, S).
