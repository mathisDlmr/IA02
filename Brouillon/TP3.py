from pprint import pprint
import itertools as it
import subprocess
from typing import List, Tuple

# aliases de type
Grid = list[list[int]] 
PropositionnalVariable = int
Literal = int
Clause = list[Literal]
ClauseBase = list[Clause]
Model = list[Literal]

# Exemple de grille de Sudoku 
grid_example = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]

def cell_to_variable(i: int, j: int, val: int) -> PropositionnalVariable:
    return 81*i + 9*j + val + 1

def model_to_grid(model: Model, nb_vals: int = 9) -> Grid:
    grid: Grid = [[0 for _ in range(9)] for _ in range(9)] # Penser à init les dimensions du tableau
    for literal in model:
        if literal > 0:   # Attention sinon ça rentre tout, mêmme les mauvaises valeurs
            l = literal - 1
            i= l // 81
            j = (l % 81) // 9
            v = l % 9
            grid[i][j] = v + 1
    return grid

def at_least_one() -> ClauseBase:
    res: ClauseBase = []
    for i in range(9):
        for j in range(9):
            cell: Clause = []
            for v in range(9):
                cell.append(cell_to_variable(i, j, v))
            res.append(cell)
    return res

def at_most_one() -> ClauseBase:
    res: ClauseBase = []
    for i in range(9):
        for j in range(9):
            for v1, v2 in it.combinations(range(9), 2):
                res.append([-cell_to_variable(i, j, v1), -cell_to_variable(i, j, v2)])
    return res

def create_cell_constraints() -> ClauseBase:
    return at_least_one() + at_most_one()

def create_line_constraints() -> ClauseBase:
    res: ClauseBase = []
    for i in range(9):
        for v in range(9):
            res.append([cell_to_variable(i, j, v) for j in range(9)])   # Pour chaque ligne, pour chaque valeur, on a (0 en (0,0) v 0 en (1,0) v ... 0 en (8,0)) ^ (1 en (0,0) v ... v 1 en (8,0)) ...
    return res

def create_column_constraints() -> ClauseBase:
    res: ClauseBase = []
    for j in range(9): 
        for v in range(9):
            res.append([cell_to_variable(i, j, v) for i in range(9)])
    return res

def create_box_constraints() -> ClauseBase:
    res: ClauseBase = []
    for box_i in range(3):
        for box_j in range(3):
            for v in range(9): 
                clause: Clause = []
                for i in range(3):
                    for j in range(3):
                        row = box_i * 3 + i
                        col = box_j * 3 + j
                        clause.append(cell_to_variable(row, col, v))   # On a 0 en (0,0) v 0 en (0,1) v ... v 0 en (2,2)
                res.append(clause)
    return res

def create_value_constraints(grid: Grid) -> ClauseBase:
    res: ClauseBase = []
    for line in range(9):
        for col in range(9):
            if grid[line][col] != 0:
                res.append([cell_to_variable(line, col, grid[line][col] -1)])
    return res

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

def pprint_grid(grid: Grid):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            print(grid[i][j] if grid[i][j] != 0 else ".", end=" ")
        print()

def main():
    grid = grid_example
    clauses = (
        create_cell_constraints()
        + create_line_constraints()
        + create_column_constraints()
        + create_box_constraints()
        + create_value_constraints(grid)
    )
    print(len(clauses))
    write_dimacs_file(clauses, "./Brouillon/sudoku.cnf")
    ok, model = exec_gophersat("./Brouillon/sudoku.cnf")
    if ok:
        solved = model_to_grid(model)
        print("Grille résolue :")
        pprint_grid(solved)
    else:
        print("Pas de solution trouvée.")


main()