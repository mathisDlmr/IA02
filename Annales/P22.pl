yeux(grands;petits).
bouche(rieuse;fermee).
bras(rouge;blanc).
chaussures(mocassins_noirs;sandales;baskets).

couvre_chef(chapeau_melon;casquette).
lunettes(bleues;soleil).
parapluie(noir).

monsieur_patate(sylvain).

{ poss(M, E) : yeux(E) } = 1 :- monsieur_patate(M).
{ poss(M, B) : bouche(B) } = 1 :- monsieur_patate(M).
{ poss(M, C) : bras(C) } = 1 :- monsieur_patate(M).
{ poss(M, S) : chaussures(S) } = 1 :- monsieur_patate(M).

0 { poss(M, C) : couvre_chef(C) } 1 :- monsieur_patate(M).
0 { poss(M, L) : lunettes(L) } 1 :- monsieur_patate(M).
0 { poss(M, parapluie(noir)) } 1 :- monsieur_patate(M).
0 { poss(M, oreilles) } 1 :- monsieur_patate(M).

:- poss(M, L), monsieur_patate(M), lunettes(L), not poss(M, oreilles).

:- poss(M, chapeau_melon), monsieur_patate(M), not poss(M, parapluie(noir)).

:- poss(M, lunettes(soleil)), poss(M, parapluie(noir)).

#show poss/2.
