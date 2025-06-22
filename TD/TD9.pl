% 1.1 Écrire un programme ASP qui renvoie un seul modèle contenant toutes les paires de nombre dont la somme des carrés fait n.
#const n=25.
nombre(0..n).

somme_carre(X,Y) :-
    nombre(X),
    nombre(Y),
    X*X + Y*Y == n.


% 1.2 Faire en sorte qu’il n’y ait qu’une seule solution par modèle.
#const n=25.
nombre(0..n).

{ somme_carre(X,Y) : nombre(X), nombre(Y), X*X + Y*Y == n } = 1.


% 1.3 Réécrire sous la forme d’un generate and test.
#const n=25.
nombre(0..n).

{ somme_carre(X,Y) : nombre(X), nombre(Y) } = 1.

:- somme(X, Y), X**X + Y**Y != n.


% 1.4 Comment casser les symétries de solution ?
% On ajoute la contrainte 

:- somme(X, Y), X<Y.   % Attention tout ce qui est avant la virgule ne vérifie pas la contrainte après la virugle. Logique de ASP




% 2. Soit le polynome p(x)=x2+2x−3. On veut définir ses valeurs comprises dans les images des entiers dans [−n,n].
% 2.1 Écrire un programme ASP dont le seul modèle stable est l’ensemble des valeurs recherchées.

#const n=25.
intervalle(-n..n).

polynome(X, Px) :-
    intervalle(X),
    Px = X**2 + 2*X - 3.
    
    
% 2.2 Le modifier pour n’avoir qu’une seule valeur par solution.

#const n=25.
intervalle(-n..n).

{ polynome(X, Px) : intervalle(X), Px = X**2 + 2*X - 3 } = 1.


% 2.3 En utilisant un generate and test, trouver ses racines entières (toujours dans le même intervalle).

#const n=25.
intervalle(-n..n).

{ polynome(X, Px) : intervalle(X), Px = X**2 + 2*X - 3 } = 1.

:- polynome(_, Px), Px != 0.


% 2.4 Que se passe-t-il si l’on considère p2(x)=x2−1 ? Et p3(x)=x2+1 ?
////////////////




% 3. On souhaite trouver une solution via Prolog au problème suivant. Dans une rue sont alignées 3 maisons, numérotées de gauche à droite de 1 à 3. Dans chaque maison habite une unique personne. On veut 
% connaître la couleur de chaque maison et la nationalité de chacun des habitants.

%    Règle 1 : Chaque maison possède une couleur différente (bleu, vert ou rouge).
%    Règle 2 : Chaque habitant possède une nationalité différente (Italien, Norvégien ou Espagnol).

%On considère également les indices suivants.

%    Indice 1 : L’Espagnol habite la maison directement à droite de la maison rouge.
%    Indice 2 : Le Norvégien vit dans la maison bleue.
%    Indice 3 : L’Italien habite dans la maison n°2.

numero(1..3).
couleur(vert; bleu; rouge).
nation(italien; norvegien; espagnol).

{ maison(X, Y, Z) : couleur(Y), nation(Z) }= 1 :- numero(X). % On génère une seule maison par numéro

:- maison(X, Y, _), maison(Z, Y, _), X!=Z.

:- maison(X, _, Z), maison(Y, _, Z), X!=Y.

:- maison(X, _, espagnol), maison(Y, rouge, _), Y!=X+1.

:- maison(_, X, norvegien), X!=bleu.

:- maison(X, _, italien), X!=2.













#const n = 10.

sommet(1..n).
couleur(rouge; vert; bleu).

{ coloration(X, Y) : couleur(Y) } = 1 :- sommet(X).  % On génère une vouleur pour chaque sommet et non un seul couple (sommet, couleur)

arc(1,2). arc(2,3). arc(3,4). arc(4,5). arc(5,1).
arc(1,6). arc(2,7). arc(3,8). arc(4,9). arc(5,10).
arc(6,8). arc(8,10). arc(10,7). arc(7,9). arc(9,6).

:- coloration(X, Z), coloration(Y, Z), arc(X, Y).  % Pas de tableau en ASP, on déclare des faits


















domino(X, Y) :-
    X = 0..6,
    Y = 0..6,
    X <= Y.
    
step(1..28).

inverser_ou_pas(X, Y) :- domino(X, Y).
inverser_ou_pas(Y, X) :- 
    domino(X, Y),
    X != Y.
    
{seq(d(X,Y), S) : inverser_ou_pas(X,Y)} = 1 :- step(S).   % on associe chaque domino à un step pour utiliser les 28 domino et les ordonner
:- seq(d(X,Y), S), seq(d(X,Y),S'), S != S'.       % Chaque domino a un et un seul id
:- seq(d(X,Y), _), seq(d(Y,X), _), X != Y.        % On a pas de doublon, mais on a des dominos doublons 
:- seq(d(X,Y),S), seq(d(Y',Z), S+1), Y!=Y'.       % Deux domnios côtes à côtes respectent les contraints de proximité

#show seq/2.
