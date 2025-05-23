nBienPlace([], [], 0).
nBienPlace([X|R1], [X|R2], BP) :- nBienPlace(R1, R2, BP2), BP is BP2+1.
nBienPlace([H1|R1], [H2|R2], N) :- dif(H1, H2), nBienPlace(R1, R2, N).

longueur([], 0).
longueur([_|R], N) :- longueur(R, N2), N is N2+1.

gagne(Code1, Code2) :- nBienPlace(Code1, Code2, X), longueur(Code1, Y), X = Y.

element(X, [X|_]).
element(X, [H|R]) :- dif(X, H), element(X, R).

enleve(_, [], []).
enleve(X, [X|R], R).
enleve(X, [H|R], [H|Res]) :- dif(H, X), enleve(X, R, Res).

enleveBP([], [], [], []).
enleveBP([X|R1], [X|R2], L1, L2) :- enleveBP(R1, R2, L1, L2).
enleveBP([H1|R1], [H2|R2], [H1|L1], [H2|L2]) :- dif(H1, H2), enleveBP(R1, R2, L1, L2).

nMalPlacesAux([], _, 0).
nMalPlacesAux([X|R1], L2, MP) :- element(X, L2), enleve(X, L2, L2bis), nMalPlacesAux(R1, L2bis, MP2), MP is MP2 + 1.
nMalPlacesAux([X|R1], L2, MP) :- \+ element(X, L2), nMalPlacesAux(R1, L2, MP).

nMalPlaces(Code1, Code2, MP) :- enleveBP(Code1, Code2, C1bis, C2bis), nMalPlacesAux(C1bis, C2bis, MP).

codeur(_, 0, []).
codeur(M, N, [X|R]) :- N > 0, random_between(1, M, X), N1 is N - 1, codeur(M, N1, R).

jouons(M, N, Max) :- codeur(M, N, Code), boucle(Code, Max).

boucle(Code, 0) :- writeln('Perdu !').
boucle(Code, Max) :-
    Max > 0,
    format('Il reste ~w coup(s).~nDonner un code : ', [Max]),
    read(Guess),
    nBienPlace(Code, Guess, BP),
    nMalPlaces(Code, Guess, MP),
    format('BP: ~w/MP: ~w~n', [BP, MP]),
    (gagne(Code, Guess) -> writeln('Gagné !!!') ; M2 is Max - 1, boucle(Code, M2)).