%%%%%%%%%%%%%%%%%%% Premier Exo %%%%%%%%%%%%%%%%%%%
element(X, [X|_]).
element(X, [H|R]) :- 
    dif(X, H), 
    element(X, R).

liste_nombre(0, [0]).
liste_nombre(X, [X|R]) :-
    X > 0,
    X2 is X - 1,
    liste_nombre(X2, R).

chiffre(X) :- 
    liste_nombre(100, Y),
    element(X, Y).

generate1(X1, X2) :- 
    chiffre(X1), 
    chiffre(X2),
    X1<X2.

test1(X1, X2, X) :-
    X =:= X1+X2.

solve1(X1, X2, X) :-
    generate1(X1, X2),
    test1(X1, X2, X).


%%%%%%%%%%%%%%%%%%% Deuxième Exo %%%%%%%%%%%%%%%%%%%
couleur(bleu).
couleur(rouge).
couleur(verte).

habitant(italien).
habitant(norvegien).
habitant(espagnol).

generate_maison(maison(X, Y, Z)) :-
    between(1, 3, X),
    couleur(Y),
    habitant(Z).

generate_aux(0, []).
generate_aux(X, [M|R]) :-
    X > 0,
    generate_maison(M),
    M = maison(X, _, _),  % on génère les maisons à partir des numéro
    X2 is X-1,
    generate_aux(X2, R).    

generate(L) :-
    generate_aux(3, LTmp),
    reverse(LTmp, L).

couleur_dif(C, L) :-
    \+member(maison(_, C, _), L).   % La couleur est pas déjà dans une maison de la liste

couleurs_unique([]).
couleurs_unique([maison(_, C, _)|R]) :-  % On véirife pour chaque maison que sa couleur est unique
    couleur_dif(C, R).

natio_dif(Nat, L) :-
    \+member(maison(_, _, Nat), L).

natios_unique([]).
natios_unique([maison(_, _, Nat)|R]) :-
    natio_dif(Nat, R).

indice1(L) :-
    member(maison(N1, rouge, _), L),
    member(maison(N2, _, espagnol), L),
    N2 is N1 + 1.

indice2(L) :- 
	member(maison(_, bleu, norvegien), L).

indice3(L) :-
    member(maison(2, _, italien), L).

test(L) :-
    couleurs_unique(L), 
    natios_unique(L),
    indice1(L), 
    indice2(L), 
    indice3(L).

solve(L) :-
    generate(L),
    test(L).









% solve([maison(1, _, norvegien)]) .....



