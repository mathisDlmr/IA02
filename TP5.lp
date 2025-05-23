% Les predicats sont sous entendus p(+In, -Out, ?InOut)

% nBienPlace(+Code1, +Code2, -BP) où Code1 représente la reponse
nBienPlace([], [], 0).   % Condition d'arrêt
nBienPlace([X|R1], [X|R2], BP) :- nBienPlace(R1, R2, BP2), BP is BP2+1.  % Si meme tete on inc
nBienPlace([H1|R1], [H2|R2], N) :- dif(H1, H2), nBienPlace(R1, R2, N).   % Sinn on continue

% longueur(+L, -N)
longueur([], 0).
longueur([_|R], N) :- longueur(R, N2), N is N2+1.

% gagne(+Code1, +Code2)
gagne(Code1, Code2) :- nBienPlace(Code1, Code2, X), longueur(Code1,Y), X=Y.


% element(+E, +L)
element(X, [X|_]).
element(X, [H|R]) :- dif(X, H), element(X, R).

% enleve(+E, +L1, -L2)
enleve(_, [], []).
enleve(X, [X|R], R).
enleve(X, [H|R], [H|Res]) :- dif(H, X), enleve(X, R, Res).

% enleveBP(+Code1, +Code2, -Code1Bis, -Code2Bis)
enleveBP([], [], [], []).
enleveBP([X|R1], [X|R2], L1, L2) :- enleveBP(R1, R2, L1, L2).
enleveBP([H1|R1], [H2|R2], L1, L2) :- dif(H1, H2), enleveBP(R1, R2, [H1|L1], [H2|L2]).

% nMalPlacesAux([1,2,3,4], [4,3,2,1], MP).
nMalPlacesAux(L1, _, X) :- longueur(L1, Y), X = Y.

% nMalPlaces(+Code1, +Code2, -MP)
nMalPlaces(L1, L2, X) :- Diff=[], enleveBP(L1, L2, Diff, []), longueur(Diff, Y), X=Y.


% codeur(+M, +N, -Code)
codeur(_, 0, []).
codeur(M, N, L) :- codeur(M, N2, [Rand|L]), Rand = random_between(1, M), N is N2+1.


% jouons(+M, +N, +Max)







