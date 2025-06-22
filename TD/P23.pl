hamburger([], []).
hamburger([H|R], [hamb(pain, H, pain)|L]) :- 
    hamburger(R, L).

begaie([], []).
begaie([H|R], [H,H|L]) :- begaie(R, L).

repete(_, 0, []).
repete(X, N, [X|R]) :- N>0, N2 is N-1, repete(X, N2, R).

concat([], L2, L2).
concat([H|R], L2, [H|Ltmp]) :- concat(R, L2, Ltmp).

begaie_n([], _, []).A
begaie_n([H|R], N, L) :-
    repete(H, N, Ltmp),
    begaie_n(R, N, L2),
    concat(Ltmp, L2, L).
