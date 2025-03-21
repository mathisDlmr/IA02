"""
Écrire un programme python permettant de générer le fichier .cnf permettant de
résoudre le problème de coloration de graphe (https://fr.wikipedia.org/wiki/Coloration_de_graphe)
à 3 couleurs suivant (schéma issu de wikipedia (https://fr.wikipedia.org
/wiki/Fichier:Petersen1_tiny.svg))
"""

import subprocess

def lecture_graphe()->(list[int],list[(int,int)]):
    nb_sommets = int(input("Nombre de sommets du graphe : "))
    sommets:list[int] = [i for i in range(1 ,nb_sommets+1)]
    print("Sommets : ", sommets)

    graphe:list[(int,int)] = []
    nb_arretes = int(input("Nombre d'arrêtes du graphe : "))
    for i in range(0, nb_arretes):
        print("Origine de la ",i+1,"e arrête : ", end="")
        a = int(input())
        print("Destination de la ",i+1,"e arrête : ", end="")
        b = int(input())
        graphe.append((a,b))
    return(sommets, graphe)

def encodage_cnf(sommets:list[int], graphe:list[(int,int)])->None:
    variables:dict[str,int] = {}
    colors:(str, str, str) = ("R","V","B")
    clauses:list[str] = []
    
    # Création des variables
    for i, sommet in enumerate(sommets):
        for j, color in enumerate(colors):
            variables[f"S{sommet}{color}"] = str(i * 3 + j + 1)

    # At Least One (chaque sommet doit avoir au moins une couleur)
    for sommet in sommets:
        at_least_one = [variables[f"S{sommet}{color}"] for color in colors]
        clauses.append(" ".join(at_least_one) + " 0")

    # At Most One (chaque sommet ne peut pas avoir plus d'une couleur)
    for sommet in sommets:
        for j in range(len(colors)):
            for k in range(j + 1, len(colors)):
                clauses.append(f"-{variables[f'S{sommet}{colors[j]}']} -{variables[f'S{sommet}{colors[k]}']} 0")

    # Contraintes sur les arêtes (pas deux sommets adjacents de la même couleur)
    for (a, b) in graphe:
        for color in colors:
            clauses.append(f"-{variables[f'S{a}{color}']} -{variables[f'S{b}{color}']} 0")

    # Écriture dans le fichier CNF
    nb_variables = len(variables)
    nb_clauses = len(clauses)

    with open('./TP2/ex3.cnf', 'w', encoding="utf-8") as f:
        f.write(f"p cnf {nb_variables} {nb_clauses}\n")
        f.write("\n".join(clauses) + "\n")

    # Exécution de Gophersat
    r = subprocess.run("./gophersat ./TP2/ex3.cnf".split(), capture_output=True, text=True)
    print(r.stdout)

def main()->None:
    (sommets, graphe) = lecture_graphe()
    encodage_cnf(sommets, graphe)

if __name__ == "__main__":
    main()