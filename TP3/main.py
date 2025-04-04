from typing import List, Tuple
import subprocess
import itertools as it

Grid = List[List[int]] 
PropositionnalVariable = int
Literal = int
Clause = List[Literal]
ClauseBase = List[Clause]
Model = List[Literal]

example: Grid = [
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

example2: Grid = [
    [0, 0, 0, 0, 2, 7, 5, 8, 0],
    [1, 0, 0, 0, 0, 0, 0, 4, 6],
    [0, 0, 0, 0, 0, 9, 0, 0, 0],
    [0, 0, 3, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 5, 0, 2, 0],
    [0, 0, 0, 8, 1, 0, 0, 0, 0],
    [4, 0, 6, 3, 0, 1, 0, 0, 9],
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [7, 2, 0, 0, 0, 0, 3, 1, 0],
]

empty_grid: Grid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
]

"""
Attention, les copies en python ne sont que des référencements de pointeurs (sur les objets non mutables).
Il faut utiliser list(variables), copy(variables) ou variables [i] pour vraiment copier
"""

def at_least_one():
    res:ClauseBase = []
    for i in range(0 ,9):
        for j in range(0, 9):
            case : Clause = []
            for v in range(0, 9):
                case.append((i*9+j)*9+v+1)
            res.append(case)
    return res

def at_most_one():
    res:ClauseBase = []
    values:list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in range(0 ,9):
        for j in range(0, 9):
            for l1, l2 in it.combinations(values, 2):
                res.append([-((i*9+j)*9+l1+1),-((i*9+j)*9+l2+1)])
    return res

def colonne():
    res:ClauseBase = []
    for j in range(0, 9):
        case : Clause = []
        for v in range(0, 9):
            case.append((9+j)*9+v+1)
        res.append(case)
    return res

def ligne():
    res:ClauseBase = []
    for i in range(0 ,9):
        case : Clause = []
        for v in range(0, 9):
            case.append((i*9)*9+v+1)
        res.append(case)
    return res

def carre():
    res:ClauseBase = []
    for i in range(0 ,3):
        for j in range(0, 3):
            case : Clause = []
            for v in range(0, 9):
                case.append((i*9+j)*9+v+1)
            res.append(case)
    return res

def write_dimacs_file(dimacs: str, filename: str):
    with open(filename, "w", newline="") as cnf:
        cnf.write(dimacs)

def exec_gophersat(filename: str, cmd: str = "gophersat", encoding: str = "utf8") -> Tuple[bool, List[int]]:
    result = subprocess.run([cmd, filename], capture_output=True, check=True, encoding=encoding)
    string = str(result.stdout)
    lines = string.splitlines()
    if lines[1] != "s SATISFIABLE":
        return False, []
    model = lines[2][2:-2].split(" ")
    return True, [int(x) for x in model]

def model_to_grid():
    pass

def main():
    pass
    #write_dimacs_file(None, "./TP3/my_file.cnf")
    #exec_gophersat("./TP3/my_file.cnf")
    #pprint(model_to_grid())

if __name__ == "__main__":
    main()
