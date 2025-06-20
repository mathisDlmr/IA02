tete([H|_], H).   % Correspond à : tete([T|_], H) :- H = T.

reste([_|R], R).

vide([]).

element(X, [X|_]).  % X est la tete ?
element(X, [H|R]) :- dif(X, H), element(X, R).  % Sinon on appel recursivement

dernier([X], X).   % On unifie X quand c'est le dernier élément
dernier([_|R], X) :- dernier(R, X).  % On parcourt jusqu'à la fin

longueur([], 0).   % Condition d'arrêt
longueur([_|R], N) :- longueur(R, N2), N is N2+1.  % A droite du is tout doit etre instancié (raison de l'existence de N2)

nombre([], _, 0).
nombre([X|R], X, N) :- nombre(R, X, N2), N is N2+1.
nombre([_|R], X, N) :- dif(X, H), nombre(R, X, N).

concat([], L2, L2).
concat([H1|R1], L2, [H1|R3]) :- concat[R1, L2, R3]).  % Ce qui est stylé c'est qu'en vrai il peut deviner une liste si on lui donne la dernière liste

inverse([], []).
inverse([H|R], L) :- inverse(R, L2), concat(L2, [H], L).  % Attention H c'est juste le premier élément, il faut mettre [H]

sous_liste([], _).
sous_liste([H, R1], [H, R2]) :- sous_liste(R1, R2).
sous_liste([H1|R1], [H2, R2]) :- dif(H1, H2), sous_liste([H1|R1], R2).

retire_element([], _, []).
retire_element([X|_], X, H).
retire_element([H|R], X, [H|Res]) :- dif(H, X), retire_element(R, X, Res).






partition(_, [], [], []).
partition(X, [H|T], [H|L1], L2) :- 
    H =< X,
    partition(X, T, L1, L2).
partition(X, [H|T], L1, [H|L2]) :- 
    H > X,
    partition(X, T, L1, L2).

tri([], []).
tri([X|R], LSorted) :-
    partition(X, R, L1, L2),
    tri(L1, L1Sorted),
    tri(L2, L2Sorted),
    append(L1Sorted, [X|L2Sorted], LSorted).






retire_element(_, [], []).
retire_element(X, [H|R], [H|L]) :- dif(X, H), retire_element(X, R, L).
retire_element(X, [X|R], Res) :- retire_element(X, R, Res).

retire_doublons([], []).
retire_doublons([H|R], L) :- member(H, R), retire_doublons(R, L).
retire_doublons([H|R1], [H|R2]) :- \+ member(H, R1),retire_doublons(R1, R2).

union(E1, E2, E) :- concat(E1, E2, Etmp), retire_doublons(Etmp, E).

intersection([], _, []).
intersection([H|R1], L, [H|R2]) :- member(H, EL), intersection(R1, L, R2).
intersection([H|R1], L, R2) :- \+ member(H, L), intersection(R1, L, R2).
