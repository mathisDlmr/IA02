"""
Écrire un programme python permettant de générer le fichier .cnf permettant de
résoudre le problème de coloration de graphe (https://fr.wikipedia.org/wiki/Coloration_de_graphe)
à 3 couleurs suivant (schéma issu de wikipedia (https://fr.wikipedia.org
/wiki/Fichier:Petersen1_tiny.svg))
"""

import subprocess
import matplotlib.pyplot as plt
import networkx as nx

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
    
    for i, sommet in enumerate(sommets):
        for j, color in enumerate(colors):
            variables[f"S{sommet}{color}"] = str(i*3+j+1)

    for sommet in sommets:
        at_least_one = [variables[f"S{sommet}{color}"] for color in colors]  # Pour chaque sommet on donne une couleur (R1 v V1 v B1)
        clauses.append(" ".join(at_least_one) + " 0")

    for sommet in sommets:
        for j in range(len(colors)):
            for k in range(j + 1, len(colors)):
                clauses.append(f"-{variables[f'S{sommet}{colors[j]}']} -{variables[f'S{sommet}{colors[k]}']} 0")   # Pour chaque sommet on a au plus une couleur (¬R1 v ¬B1) ^ (¬B1 v ¬V1) ^ (¬R1 v ¬V1)

    for (a, b) in graphe:
        for color in colors:
            clauses.append(f"-{variables[f'S{a}{color}']} -{variables[f'S{b}{color}']} 0")  # On ne peut avoir 2 sommets côtes à côtes de mm couleur : ¬(R1 ^ R2) <=> (¬R1 v ¬R2)

    nb_variables = len(variables)
    nb_clauses = len(clauses)

    with open('./TP2/ex3.cnf', 'w', encoding="utf-8") as f:
        f.write(f"p cnf {nb_variables} {nb_clauses}\n")
        f.write("\n".join(clauses) + "\n")

    r = subprocess.run("./gophersat ./TP2/ex3.cnf".split(), capture_output=True, text=True)
    print(r.stdout)

    lines = r.stdout.splitlines()
    solution_line = next((line for line in lines if line.startswith('v')), "")
    solution = [int(x) for x in solution_line.split()[1:] if x != '0']
    
    color_map = {}
    for var, idx in variables.items():
        idx = int(idx)
        if idx in solution:
            sommet = int(var[1:-1])
            couleur = var[-1]
            if couleur == 'R':
                color_map[sommet] = 'red'
            elif couleur == 'V':
                color_map[sommet] = 'green'
            elif couleur == 'B':
                color_map[sommet] = 'blue'

    G = nx.Graph()
    G.add_nodes_from(sommets)
    G.add_edges_from(graphe)
    node_colors = [color_map.get(node, 'gray') for node in G.nodes()]
    nx.draw(G, with_labels=True, node_color=node_colors, edge_color='black')
    plt.show()

def main()->None:
    #(sommets, graphe) = lecture_graphe()
    #encodage_cnf(sommets, graphe)
    encodage_cnf([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (2, 7), (3, 8), (4, 9), (5, 10), (6, 8), (8, 10), (10, 7), (7, 9), (9, 6), (5, 1)])

if __name__ == "__main__":
    main()


"""
Nombre de sommets du graphe : 10
Sommets :  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
Nombre d'arrêtes du graphe : 15
Origine de la  1 e arrête : 1
Destination de la  1 e arrête : 2
Origine de la  2 e arrête : 2
Destination de la  2 e arrête : 3
Origine de la  3 e arrête : 3
Destination de la  3 e arrête : 4
Origine de la  4 e arrête : 4
Destination de la  4 e arrête : 5
Origine de la  5 e arrête : 5
Destination de la  5 e arrête : 6
Origine de la  6 e arrête : 2
Destination de la  6 e arrête : 7
Origine de la  7 e arrête : 3
Destination de la  7 e arrête : 8
Origine de la  8 e arrête : 4
Destination de la  8 e arrête : 9
Origine de la  9 e arrête : 5
Destination de la  9 e arrête : 10
Origine de la  10 e arrête : 6
Destination de la  10 e arrête : 8
Origine de la  11 e arrête : 8
Destination de la  11 e arrête : 10
Origine de la  12 e arrête : 10
Destination de la  12 e arrête : 7
Origine de la  13 e arrête : 7
Destination de la  13 e arrête : 9
Origine de la  14 e arrête : 9
Destination de la  14 e arrête : 6
Origine de la  15 e arrête : 5
Destination de la  15 e arrête : 1
c solving ./TP2/ex3.cnf
s SATISFIABLE
v -1 -2 3 -4 5 -6 7 -8 -9 -10 -11 12 -13 14 -15 -16 -17 18 -19 -20 21 -22 23 -24 25 -26 -27 28 -29 -30 0
"""