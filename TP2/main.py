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
    for i in range(0, len(sommets)):
        for j in range(0, len(colors)):
            variables["S"+str(i)+colors[j]] = str(i*3+j+1)

# At Least One
    atLeastOne:list[str] = []
    for value in variables.values():
        atLeastOne.append(value)

# At Most One
    atMostOne:list[str] = []
    for value in variables.values(): 

# Pour chaque arrete, on a [non(SiC),non(SjC)] avec C la couleur



#    with open('./TP2/ex3.cnf', 'w',encoding="utf-8") as f:
#        f.write("bla")
#    r = subprocess.run("./gophersat ./TP2/ex3.cnf".split(), capture_output=True)
#    r.stdout

def main()->None:
    sommets:list[int] = []
    graphe:list[(int,int)] = []
    (sommets,graphe) = lecture_graphe()
    encodage_cnf(sommets, graphe)

if __name__ == "__main__":
    main()