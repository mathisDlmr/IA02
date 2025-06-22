suite_domino([], []).
suite_domino([D], [D2]) :- retourner_ou_pas(D, D2).     % Si il reste un seul domino, on peut le tourner comme on veut. On met D et D2 en crochet pour passer un domino en param, et non la liste de domino
suite_domino(Bag, [[X, Y] , [Y, T] | R]) :-    % On colle le domino X,Y à Y,T sans prendre en compte le R
    select(D, Bag, Bag2),    % On prend un D dans Bag, Bag2 correspond à Bag sans D
    retourner_ou_pas(D, [X, Y]),   % On offre la possibilité de le retourner
    suite_domino(Bag2, [[Y, T] | R]).   % On récurse sur la liste sans D

retourner_ou_pas(D, D).   % Renvoyer le domino tel quel
retourner_ou_pas([X, Y], [Y, X]) :- dif(X, Y).   % Renvoyer le domino inversé

domino([X,Y]) :-
    between(0, 6, X),
    between(0, 6, Y),
	X =< Y.     % On bloque les symétries	
