% 4 primitives : homme/1, femme/1, parent/2, couple/2

homme(créon).
homme(hémon).
homme(œdipe).
homme(étéocle).
homme(ménécée).
homme(polynice).
homme(laïos).
homme(penthée).

femme(ismène).
femme(antigone).
femme(jocaste).
femme(eurydice). 

parent(penthée, ménécée).
parent(créon, hémon).
parent(eurydice, hémon).
parent(ménécée, jocaste).
parent(ménécée, créon).
parent(laïos, œdipe).
parent(jocaste, œdipe).
parent(œdipe, étéocle).
parent(œdipe, polynice).
parent(œdipe, antigone).
parent(œdipe, ismène).
parent(jocaste, étéocle).
parent(jocaste, polynice).
parent(jocaste, antigone).
parent(jocaste, ismène).

pere(X, Y) :- homme(X), parent(X, Y).
mere(X, Y) :- femme(X), parent(X, Y).
epoux(X, Y) :- homme(X), couple(X, Y).
% on Rajoute homme(X), couple(Y, X)
epouse(X, Y) :- femme(X), couple(X, Y).
% couple(X, Y) :- couple(Y, X). % Pas possible car créé des boucles infinies
fils(X, Y) :- homme(X), parent(Y, X).
fille(X, Y) :- femme(X), parent(Y, X).
enfant(X, Y) :- parent(Y, X).
parent(X, Y) :- pere(X, Y); mere(X, Y).
grandPere(X, Y) :- homme(X), parent(X, Z), parent(Z, Y).
grandMere(X, Y) :- femme(X), parent(X, Z), parent(Z, Y).
grandParent(X, Y) :- parent(X, Z), parent(Z, Y).
petitFils(X, Y) :- homme(X), parent(Z, X), parent(Y, Z).
petiteFille(X, Y) :- femme(X), parent(Z, X), parent(Y, Z).
memePere(X, Y) :- pere(P, X), pere(P, Y), X \= Y.
memeMere(X, Y) :- mere(M, X), mere(M, Y), X \= Y.
memeParent(X, Y) :- parent(P, X), parent(P, Y), X \= Y.
memeParents(X, Y) :- pere(P, X), pere(P, Y), mere(M, X), mere(M, Y), X \= Y.
frere(X, Y) :- homme(X), memeParents(X, Y).
soeur(X, Y) :- femme(X), memeParents(X, Y).
demiFrere(X, Y) :- homme(X), memeParent(X, Y), \+ memeParents(X, Y).   % Ici il faut bien mettre à la fin le \+ meme Parents. Si on le met au début, on essaye de prouver la non-existence de tout l'univers
demiSoeur(X, Y) :- femme(X), memeParent(X, Y), \+ memeParents(X, Y).

% Oncles et tantes
oncle(X, Y) :-
    homme(X),
    parent(P, Y),
    frere(X, P).

oncle(X, Y) :-
    homme(X),
    parent(P, Y),
    soeur(S, P),
    couple(X, S).

tante(X, Y) :-
    femme(X),
    parent(P, Y),
    soeur(X, P).

tante(X, Y) :-
    femme(X),
    parent(P, Y),
    frere(F, P),
    couple(X, F).

% Neveux et nièces
neveu(X, Y) :- homme(X), parent(P, X), frere(P, Y).
neveu(X, Y) :- homme(X), parent(P, X), soeur(P, Y).

niece(X, Y) :- femme(X), parent(P, X), frere(P, Y).
niece(X, Y) :- femme(X), parent(P, X), soeur(P, Y).

% Cousins et cousines
cousin(X, Y) :-
    homme(X),
    parent(P1, X),
    parent(P2, Y),
    memeParent(P1, P2),
    P1 \= P2.

cousine(X, Y) :-
    femme(X),
    parent(P1, X),
    parent(P2, Y),
    memeParent(P1, P2),
    P1 \= P2.

% Gendre et bru
gendre(X, Y) :-
    homme(X),
    couple(X, E),
    parent(Y, E).

bru(X, Y) :-
    femme(X),
    couple(X, E),
    parent(Y, E).

% Marâtre et beaux-parents
maratre(X, Y) :-
    femme(X),
    couple(X, P),
    pere(P, Y),
    \+ mere(X, Y).

belleMere(X, Y) :-
    femme(X),
    (gendre(Y, X); bru(Y, X));
    maratre(X, Y).

beauPere(X, Y) :-
    homme(X),
    couple(X, M),
    mere(M, Y),
    \+ pere(X, Y).

% Ascendants et descendants
ascendant(X, Y) :- parent(X, Y).
ascendant(X, Y) :- parent(X, Z), ascendant(Z, Y).

descendant(X, Y) :- enfant(X, Y).
descendant(X, Y) :- enfant(X, Z), descendant(Z, Y).

% Lignée et parenté
lignee(X, Y) :- ascendant(X, Y); descendant(X, Y).

parente(X, Y) :- X \= Y, lignee(X, Y).
