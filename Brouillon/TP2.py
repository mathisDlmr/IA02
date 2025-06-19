from typing import List, Dict, Tuple
import itertools as it
import subprocess

def lecture_graphe()->(list[int],list[(int,int)]):
    a = int(input("Nombre de sommets : "))
    sommets: List[int] = [i+1 for i in range (a)]
    print("Les sommets sont donc ", sommets)

    arretes: List[(int, int)] = []
    nb_arretes = int(input("Combien d'arretes ? "))
    for _ in range(nb_arretes):
        i = int(input("Origine ? "))
        j = int(input("Destination ? "))
        arretes.append((i,j))

    return (sommets, arretes)

def encodage_cnf(sommets:list[int], arretes:list[(int,int)])->None:
    colors: Tuple[str] = ("R","V","B")
    var: Dict[str, int] = {}
    for sommet in sommets:
        for i in range(3):
            var[f"{colors[i]}{sommet}"] = 3*(sommet-1) + i +1

    clauses: List[List[int]] = []

    # At Least One
    for sommet in sommets:
        clauses.append([var[f"{color}{sommet}"] for color in colors])

    # At Most One
    for sommet in sommets:
        for i,j in it.combinations(range(3), 2):
            clauses.append([-var[f"{colors[i]}{sommet}"], -var[f"{colors[j]}{sommet}"]])

    # Contrainte de proxi
    for arrete in arretes:
        for color in colors:
            clauses.append([-var[f"{color}{arrete[0]}"], -var[f"{color}{arrete[1]}"]])

    nb_variables = len(var)
    nb_clauses = len(clauses)

    with open('./Brouillon/TD2.cnf', 'w', encoding="utf-8") as f:
        f.write(f"p cnf {nb_variables} {nb_clauses}\n")
        for clause in clauses:
            f.write(" ".join(str(variable) for variable in clause) + " 0\n")

    r = subprocess.run("./gophersat ./Brouillon/TD2.cnf".split(), capture_output=True, text=True)
    print(r.stdout)

def main()->None:
    #(sommets, graphe) = lecture_graphe()
    #encodage_cnf(sommets, graphe)
    encodage_cnf([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (2, 7), (3, 8), (4, 9), (5, 10), (6, 8), (8, 10), (10, 7), (7, 9), (9, 6), (5, 1)])

main()