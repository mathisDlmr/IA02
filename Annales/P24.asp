enfants(alfred; betty; charles).
accessoire(chapeau; manteau; echarpe).
couleur_pref(rouge; vert; bleu).
couleur_accessoire(rouge; vert; bleu).

{ generate(X, Y, Z, W) : accessoire(Y), couleur_pref(Z), couleur_accessoire(W) } = 1 :- enfants(X).

:- generate(X, chapeau, _, rouge), X!=alfred.   % Attention on ne peut donner que des contraintes, pas des faits
:- generate(X, manteau, _, vert), X!=betty.
:- generate(X, echarpe, _, bleu), X!=charles.
:- generate(X, _, Z, _), generate(Y, _, Z, _), X!=Y.
:- generate(_, _, X, X).
:- generate(X, _, rouge, _), X!=betty.
