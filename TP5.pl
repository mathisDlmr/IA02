% Les predicats sont sous entendus p(+In, -Out, ?InOut)

% nBienPlace(+Code1, +Code2, -BP) où Code1 représente la reponse
nBienPlace([], [], 0).   % Condition d'arrêt
nBienPlace([X|R1], [X|R2], BP) :- nBienPlace(R1, R2, BP2), BP is BP2+1.  % Si meme tete on inc
nBienPlace([H1|R1], [H2|R2], N) :- dif(H1, H2), nBienPlace(R1, R2, N).   % Sinn on continue

% longueur(+L, -N)
longueur([], 0).
longueur([_|R], N) :- longueur(R, N2), N is N2+1.

% gagne(+Code1, +Code2)
gagne(Code1, Code2) :- nBienPlace(Code1, Code2, Y), longueur(Code1,Y).


% element(+E, +L)
element(X, [X|_]).
element(X, [H|R]) :- dif(X, H), element(X, R).

% enleve(+E, +L1, -L2)
enleve(_, [], []).
enleve(X, [X|R], R).   % Pour ne retirer que la premiere occurence il suffit de ne pas continuer l'appel
enleve(X, [H|R], [H|Res]) :- dif(H, X), enleve(X, R, Res).

% enleveBP(+Code1, +Code2, -Code1Bis, -Code2Bis)
enleveBP([], [], [], []).
enleveBP([X|R1], [X|R2], L1, L2) :- enleveBP(R1, R2, L1, L2).
enleveBP([H1|R1], [H2|R2], [H1|L1], [H2|L2]) :- dif(H1, H2), enleveBP(R1, R2, L1, L2).

% nMalPlacesAux([1,2,3,4], [4,3,2,1], MP).
nMalPlacesAux([], _, 0).
nMalPlacesAux([X|R1], L2, MP) :- element(X, L2), enleve(X, L2, L2bis), nMalPlacesAux(R1, L2bis, MP2), MP is MP2 + 1.   % Si on trouve la tete de L1 ds L2 on le retire, inc le compteur et continue
nMalPlacesAux([X|R1], L2, MP) :- \+ element(X, L2), nMalPlacesAux(R1, L2, MP).  % Si on ne trouve pas la tete de L1 ds L2, on continue

% nMalPlaces(+Code1, +Code2, -MP)
nMalPlaces(L1, L2, MP) :- enleveBP(L1, L2, C1, C2), nMalPlacesAux(C1, C2, MP).

% codeur(+M, +N, -Code)
codeur(_, 0, []).
codeur(M, N, [X|R]) :- N > 0, random_between(1, M, X), N2 is N - 1, codeur(M, N2, R).


% jouons(+M, +N, +Max)
jouons(M, N, Max) :- codeur(M, N, Code), boucle(Code, Max).

boucle(_, 0) :- print('Perdu !').
boucle(Code, Max) :-
    Max > 0,
    format('Il reste ~w coup(s).~nDonner un code : ', [Max]),
    read(Rep),
    nBienPlace(Code, Rep, BP),
    nMalPlaces(Code, Rep, MP),
    format('BP: ~w/MP: ~w~n', [BP, MP]),
    (gagne(Code, Rep) -> print('Gagné !!!') ; M2 is Max - 1, boucle(Code, M2)).
