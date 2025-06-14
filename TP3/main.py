from typing import List, Tuple
import subprocess
import itertools as it

Grid = List[List[int]] 
PropositionnalVariable = int
Literal = int
Clause = List[Literal]
ClauseBase = List[Clause]
Model = List[Literal]

"""
Attention, les copies en python ne sont que des référencements de pointeurs (sur les objets non mutables).
Il faut utiliser list(variables), copy(variables) ou variables [i] pour vraiment copier
"""

def var(i: int, j: int, v: int) -> int:
    return (i * 81) + (j * 9) + (v + 1)   # A chaque case on attribue la variable de valeur v+1 (car on suppose le sudoko de 0->8) + j*9 (car 9 valeurs par colonne) + i*81 (car 9*9 valeurs par lignes)

def at_least_one() -> ClauseBase:
    res: ClauseBase = []
    for i in range(9):
        for j in range(9):
            res.append([var(i, j, v) for v in range(9)])  # Chaque case aura au moins un nombre : 0 en (0,0) v 1 en (0,0), ... <=> 1 v 2 v ... v 8
    return res

def at_most_one() -> ClauseBase:
    res: ClauseBase = []
    for i in range(9):
        for j in range(9):
            for v1, v2 in it.combinations(range(9), 2):
                res.append([-var(i, j, v1), -var(i, j, v2)])  # Chaque case a un seul chiffre -> On fait une 2 Combi parmis 9 car on a ¬(V1 ^ V2) <=> ¬V1 v ¬V2
    return res

def create_line_constraints() -> ClauseBase:
    res: ClauseBase = []
    for i in range(9):
        for v in range(9):
            res.append([var(i, j, v) for j in range(9)])   # Pour chaque ligne, pour chaque valeur, on a (0 en (0,0) v 0 en (1,0) v ... 0 en (8,0)) ^ (1 en (0,0) v ... v 1 en (8,0)) ...
    return res

def create_column_constraints() -> ClauseBase:
    res: ClauseBase = []
    for j in range(9): 
        for v in range(9):
            res.append([var(i, j, v) for i in range(9)])
    return res

def create_box_constraints() -> ClauseBase:
    res: ClauseBase = []
    for box_i in range(3):
        for box_j in range(3):
            for v in range(9): 
                clause = []
                for i in range(3):
                    for j in range(3):
                        row = box_i * 3 + i
                        col = box_j * 3 + j
                        clause.append(var(row, col, v))   # On a 0 en (0,0) v 0 en (0,1) v ... v 0 en (2,2)
                res.append(clause)
    return res

# Prend une grille comme paramètre et enregistre ses valeurs comme des faits dans le DIMAC
def create_value_constraints(grid: Grid) -> ClauseBase:
    clauses: ClauseBase = []
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                clauses.append([var(i, j, grid[i][j] - 1)])
    return clauses

def write_dimacs_file(clauses: ClauseBase, filename: str):
    nb_clauses = len(clauses)
    with open(filename, "w") as f:
        f.write(f"p cnf {729} {nb_clauses}\n")
        for clause in clauses:
            f.write(" ".join(map(str, clause)) + " 0\n")

def exec_gophersat(filename: str, cmd: str = "./gophersat", encoding: str = "utf8") -> Tuple[bool, List[int]]:
    result = subprocess.run([cmd, filename], capture_output=True, check=True, encoding=encoding)
    string = str(result.stdout)
    lines = string.splitlines()
    if lines[1] != "s SATISFIABLE":
        return False, []
    model = lines[2][2:-2].split(" ")
    return True, [int(x) for x in model]

# Met en forme la réponse en une Grid qu'on pourra afficher plus tard
def model_to_grid(model: Model) -> Grid:
    grid: Grid = [[0 for _ in range(9)] for _ in range(9)]
    for literal in model:
        if literal > 0:
            l = literal - 1
            i, j, v = l // 81, (l % 81) // 9, l % 9
            grid[i][j] = v + 1
    return grid

# Affichage de la Grid mise en forme
def pprint_grid(grid: Grid):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            print(grid[i][j] if grid[i][j] != 0 else ".", end=" ")
        print()

example: Grid = [
    [0, 0, 0, 0, 0, 7, 0, 5, 2],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 0, 8, 0, 6],
    [9, 0, 0, 0, 0, 4, 6, 0, 0],
    [0, 4, 0, 0, 8, 0, 0, 0, 7],
    [0, 1, 0, 3, 0, 0, 0, 9, 0],
    [3, 0, 0, 8, 0, 0, 4, 1, 0],
    [1, 0, 0, 0, 0, 9, 2, 3, 0],
    [0, 0, 5, 4, 0, 0, 0, 0, 0],
]

def main():
    grid = example 
    clauses = (
        at_least_one()
        + at_most_one()
        + create_line_constraints()
        + create_column_constraints()
        + create_box_constraints()
        + create_value_constraints(grid)
    )
    print(len(clauses))
    write_dimacs_file(clauses, "./TP3/sudoku.cnf")
    ok, model = exec_gophersat("./TP3/sudoku.cnf")
    if ok:
        solved = model_to_grid(model)
        print("Grille résolue :")
        pprint_grid(solved)
    else:
        print("Pas de solution trouvée.")

if __name__ == "__main__":
    main()
