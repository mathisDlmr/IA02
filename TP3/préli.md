## 1. Combien de variables propositionnelles sont nécessaires ?
> On a 9 lignes, 9 colonnes, 9 valeurs donc **729 variables**

## 2. Étant donné un ensemble de variables propositionnelles, que signifient les contraintes at_least_one et unique sur cet ensemble ? 
> Le at_least_ont correspond à la présence d'un chiffre dans chaque case.

> L'unicité représente qu'on a un seul nombre dans chaque case

### Quel rapport avec un XOR ? 
> Le xor pourrait presque représenter l'unicité, mais il est vrai s'il y a un nombre impair de variables négatives. 

> On va donc utiliser un at_most_one avec le at_least_one pour représenter l'unicité

### Comment les écrit-on avec des clauses ?
> - at_least_one : Disjonction de tous nos littéraux
> - at_most_one : Disjonction de toutes les 2-combinaisons réalisables sur les littéraux négatifs

## 3. Comment modélise-t-on les règles génériques du Sudoku en logique propositionnelle à l’aide de ces contraintes ?
> - Une et une seule valeur dans chaque case
>   - cf. questions précédentes
>   - |alo| + |amo| : (9 * 9 * ( 1 + ( 2C9 ))) = **2997 clauses**
> - Toutes les valeurs sur une colonne sont différentes
>   - Pas besoin de préciser l'unicité car on sait que chaque case aura une valeur, et que les 9 chiffres sont différents
> - 9 valeurs sur 9 colonnes : **81 clauses**
>   - Il suffit donc d'avoir un at_lest_one de chaque valeur sur la colonne j
> - Toutes les valeurs sur une ligne sont différentes
>   - Pas besoin de préciser l'unicité car on sait que chaque case aura une valeur, et que les 9 chiffres sont différents
>   - Il suffit donc d'avoir un at_lest_one de chaque valeur sur la ligne i
> - 9 valeurs sur 9 lignes : **81 clauses**
> - Toutes les valeurs dans un carré sont différentes
>   - Pas besoin de préciser l'unicité car on sait que chaque case aura une valeur, et que les 9 chiffres sont différents
>   - Il suffit d'avoir un at_lest_one de chaque valeur sur "chaque carré"
> - 9 valeurs sur 9 cases du carré : **81 clauses**

> **Total de 3240 clauses + Le nombre de faits que l'on a déjà**

## Comment représenter la grille
> On représente la grille en 2 couches
> - Un premier niveau qui représente les 9 carrés
> - Le deuxième niveau qui représente les 9 valeurs de notre carré
Dans cette représentation, la position est donnée par (i * 3 + i', j * 3 + j') = 3(i,j) + (i', j') avec (i,j) les cords absolue et (i', j') les cords relatives
> 
> Cela nous permettra d'analyser la règle sur les carrés selon les (i, j) fixés et (i', j') variables

> En termes de littéraux, on va commencer à partir de 1 (pour avoir un négatif).
> - 0 en (0 ,0) = 1
> - 1 en (0, 0) = 2
> - ...
> - 0 en (0, 1) = 10
> - ...
> - 8 en (0, 8) = 81
>
> Les variables sont donc données selon (i * 81 + j * 9 + v + 1) = **(i * 9 + j) * 9 + v + 1** avec v la valeur, i la ligne et j la colonne

## 4. Comment peut-on intégrer les valeurs d’une grille donnée à la précédente modélisation ?
> Pour intégrer nos faits (valeurs données) à la grille, il suffit d'ajouter (conjonction) la présence du numéro v sur la colonne j et ligne i

## Comment inverser l'encodage de notre grille
> Soit n un littéral. On pose n' = n-1
> - v = n' % 9
> - j = (n' // 9) % 9
> - i = (n' // 9) // 9