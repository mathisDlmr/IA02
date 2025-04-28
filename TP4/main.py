from typing import List, Tuple, Callable
import ast
import random
from functools import lru_cache # Cache pour l'optimisation

# Optionnel
import itertools as it
import time

# Quelques structures de données
Grid = tuple[tuple[int, ...], ...]   # tuple de tuple pour pouvoir le mettre en cache dans un dictionnaire (car pas mutable) + garde l'idée qu'on peut créer un nouvel état mais pas modifier l'état actuel
State = Grid   # Grille actuelle
Action = tuple[int, int]  # Les coords (qui sont suffisantes avec l'info Player)
Player = int   # 1 pour x et 2 pour o
Score = float  # Pour faire une fonctione d'évaluation à profondeur limitée
Strategy = Callable[[State, Player], Action]

# Quelques constantes
DRAW = 0
EMPTY = 0
X = 1
O = 2

EMPTY_GRID: Grid = ((0, 0, 0), (0, 0, 0), (0, 0, 0))
GRID_0: Grid = EMPTY_GRID
GRID_1: Grid = ((0, 0, 0), (0, X, O), (0, 0, 0))
# (0, 0, 0),
# (0, X, O),
# (0, 0, 0))

GRID_2: Grid = ((O, 0, X), (X, X, O), (O, X, 0))
#((O, 0, X),
# (X, X, O),
# (O, X, 0)

GRID_3: Grid = ((O, 0, X), (0, X, O), (O, X, 0))
#((O, 0, X),
# (0, X, O),
# (O, X, 0))

GRID_4: Grid = ((0, 0, 0), (X, X, O), (0, 0, 0))
#((0, 0, 0),
# (X, X, O),
# (0, 0, 0))

GRID_5: Grid = ((0, O, O), (X, O, X), (O, 0, 0))

def grid_tuple_to_grid_list(grid: Grid) -> list[list[int]]:
    return [list(row) for row in grid]

def grid_list_to_grid_tuple(grid: list[list[int]]) -> Grid:
    return tuple(tuple(row) for row in grid)

def legals(grid: State) -> list[Action]:
    legs : list[Action] = []
    for line in range(3):
        for col in range(3):
            if(grid[line][col] == 0):
                legs.append((line, col))
    return legs

def check_lines(grid: State, player: Player) -> bool:
    count: int = 0
    for line in range(3):
        count = 0
        for col in range(3):
            if(grid[line][col] == player):
                count+=1
            if count == 3:
                return True
    return False

def check_cols(grid: State, player: Player) -> bool:
    count: int = 0
    for line in range(3):
        count = 0
        for col in range(3):
            if(grid[col][line] == player):
                count+=1
            if count == 3:
                return True
    return False

def check_diags(grid: State, player: Player) -> bool:
    if all(grid[i][i] == player for i in range(3)):
        return True
    if all(grid[i][2-i] == player for i in range(3)):
        return True
    return False

def line(grid: State, player: Player) -> bool:
    return check_lines(grid, player) or check_cols(grid, player) or check_diags(grid, player)

def final(grid: State) -> bool:
    full = all(grid[i][j] != 0 for i in range(3) for j in range(3))
    return full or line(grid, X) or line(grid, O)

def score(grid: State) -> Score:
    if line(grid, X):
        return 1
    elif line(grid, O):
        return -1
    else:
        return 0

def pprint(grid: State):
   for line in range(3):
        for col in range(3):
            if(grid[line][col]==0):
                print('.', end=' ') 
            elif(grid[line][col]==1):
                print('X', end=' ') 
            else:
                print('O', end=' ') 
        print()

def play(grid: State, player: Player, action: Action) -> State:
    new_state:[[int]] = grid_tuple_to_grid_list(grid)
    new_state[action[0]][action[1]] = player
    return grid_list_to_grid_tuple(new_state)

def tictactoe(strategy_X: Strategy, strategy_O: Strategy, debug: bool = False) -> Score:
    grid: State = EMPTY_GRID
    pprint(grid)
    player: Player = X
    while not final(grid):
        if player == X:
            action = strategy_X(grid, X)
            grid = play(grid, X, action)
            player = O
        else: 
            action = strategy_O(grid, O)
            grid = play(grid, O, action)
            player = X
        pprint(grid)
    return score(grid)

def strategy_first_legal(grid: State, player: Player) -> Action:
    return(legals(grid)[0])

def strategy_random(grid: State, player: Player) -> Action:
    legs: list[Action] = legals(grid)
    return (legs[random.randint(0, len(legs)-1)])

@lru_cache(maxsize=None)
def minmax(grid: State, player: Player) -> Score:
    if final(grid):
        return score(grid)
    scores = []
    for action in legals(grid):
        next_grid = play(grid, player, action)
        next_score = minmax(next_grid, 3 - player)  # 3-player inverse 1->2 ou 2->1
        scores.append(next_score)
    if player == X:
        return max(scores)
    else:
        return min(scores)

@lru_cache(maxsize=None)
def minmax_action(grid: State, player: Player, depth: int = 0) -> tuple[Score, Action]:
    if final(grid):
        return (score(grid), (-1, -1)) 
    best_score = float('-inf') if player == X else float('inf')
    best_action = None
    for action in legals(grid):
        next_grid = play(grid, player, action)
        next_score, _ = minmax_action(next_grid, 3 - player, depth + 1)
        if (player == X and next_score > best_score) or (player == O and next_score < best_score):
            best_score = next_score
            best_action = action
    return (best_score, best_action)

def strategy_minmax(grid: State, player: Player) -> Action:
    return minmax_action(grid, player)[1]

@lru_cache(maxsize=None)
def minmax_actions(grid: State, player: Player, depth: int = 0) -> tuple[Score, list[Action]]:
    if final(grid):
        return (score(grid), [])
    best_score = float('-inf') if player == X else float('inf')
    best_actions = []
    for action in legals(grid):
        next_grid = play(grid, player, action)
        next_score, _ = minmax_actions(next_grid, 3 - player, depth + 1)
        if player == X:
            if next_score > best_score:
                best_score = next_score
                best_actions = [action]
            elif next_score == best_score:
                best_actions.append(action)
        else:
            if next_score < best_score:
                best_score = next_score
                best_actions = [action]
            elif next_score == best_score:
                best_actions.append(action)
    return (best_score, best_actions)

def strategy_minmax_random(grid: State, player: Player) -> Action:
    _, actions = minmax_actions(grid, player)
    return random.choice(actions)

def test_performance(strategy: Strategy):
    start = time.time()
    result = tictactoe(strategy, strategy, debug=False)
    end = time.time()
    print(f"Score: {result}, Temps de calcul : {end - start:.4f} secondes")

def main():
    print("Test sans cache (first legal vs random):")
    tictactoe(strategy_first_legal, strategy_random)
    print("\nTest minmax avec cache (minmax vs minmax):")
    test_performance(strategy_minmax)
    print("\nTest minmax_random avec cache (minmax_random vs minmax_random):")
    test_performance(strategy_minmax_random)


if __name__ == "__main__":
    main()
