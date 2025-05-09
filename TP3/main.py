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
    return (i * 81) + (j * 9) + (v + 1)

def at_least_one() -> ClauseBase:
    res: ClauseBase = []
    for i in range(9):
        for j in range(9):
            res.append([var(i, j, v) for v in range(9)])
    return res

def at_most_one() -> ClauseBase:
    res: ClauseBase = []
    for i in range(9):
        for j in range(9):
            for v1, v2 in it.combinations(range(9), 2):
                res.append([-var(i, j, v1), -var(i, j, v2)])
    return res

def all_diff_unit(get_indices) -> ClauseBase:
    res: ClauseBase = []
    for v in range(9):
        for unit in range(9):
            cells = get_indices(unit)
            for i1, i2 in it.combinations(cells, 2):
                res.append([-var(*i1, v), -var(*i2, v)])
    return res

def ligne() -> ClauseBase:
    return all_diff_unit(lambda i: [(i, j) for j in range(9)])

def colonne() -> ClauseBase:
    return all_diff_unit(lambda j: [(i, j) for i in range(9)])

def carre() -> ClauseBase:
    def block_indices(b):
        bi, bj = divmod(b, 3)
        return [(i, j) for i in range(bi * 3, bi * 3 + 3) for j in range(bj * 3, bj * 3 + 3)]
    return all_diff_unit(block_indices)

def insert_values(grid: Grid) -> ClauseBase:
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

def model_to_grid(model: Model) -> Grid:
    grid: Grid = [[0 for _ in range(9)] for _ in range(9)]
    for literal in model:
        if literal > 0:
            l = literal - 1
            i, j, v = l // 81, (l % 81) // 9, l % 9
            grid[i][j] = v + 1
    return grid

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
        + ligne()
        + colonne()
        + carre()
        + insert_values(grid)
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
