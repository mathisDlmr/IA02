from typing import List, Tuple, Callable
import ast
import random

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
    
# Etant donné un état de jeu renvoie sous forme de tuple l'action amenant au score optimal de la partie et ce score
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
    return minmax_action(grid, player)[1]   # On joue l'action donnée par le minmax

# Ecrire la fonction minmax qui étant donné un état de jeu renvoie dans un tuple les actions amenant au score optimal de la partie et ce score
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

# Minmax indeterministe
def strategy_minmax_random(grid: State, player: Player) -> Action:
    _, actions = minmax_actions(grid, player)
    return random.choice(actions)

def memoize(func: Callable) -> Callable:
    cache = {}

    def memoized_func(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]

    return memoized_func

@memoize
def minmax_cached(grid: State, player: Player) -> Score:
    if final(grid):
        return score(grid)
    scores = []
    for action in legals(grid):
        next_grid = play(grid, player, action)
        next_score = minmax_cached(next_grid, 3 - player)
        scores.append(next_score)
    if player == X:
        return max(scores)
    else:
        return min(scores)

@memoize
def minmax_action_cached(grid: State, player: Player, depth: int = 0) -> tuple[Score, Action]:
    if final(grid):
        return (score(grid), (-1, -1)) 
    best_score = float('-inf') if player == X else float('inf')
    best_action = None
    for action in legals(grid):
        next_grid = play(grid, player, action)
        next_score, _ = minmax_action_cached(next_grid, 3 - player, depth + 1)
        if (player == X and next_score > best_score) or (player == O and next_score < best_score):
            best_score = next_score
            best_action = action
    return (best_score, best_action)

def strategy_minmax_cached(grid: State, player: Player) -> Action:
    return minmax_action_cached(grid, player)[1]

@memoize
def minmax_actions_cached(grid: State, player: Player, depth: int = 0) -> tuple[Score, list[Action]]:
    if final(grid):
        return (score(grid), [])
    best_score = float('-inf') if player == X else float('inf')
    best_actions = []
    for action in legals(grid):
        next_grid = play(grid, player, action)
        next_score, _ = minmax_actions_cached(next_grid, 3 - player, depth + 1)
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

def strategy_minmax_random_cached(grid: State, player: Player) -> Action:
    _, actions = minmax_actions_cached(grid, player)
    return random.choice(actions)

def alphabeta(grid: State, player: Player, alpha: float = float('-inf'), beta: float = float('inf')) -> Score:
    if final(grid):
        return score(grid)
    if player == X:
        max_eval = float('-inf')
        for action in legals(grid):
            next_grid = play(grid, player, action)
            eval = alphabeta(next_grid, 3 - player, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for action in legals(grid):
            next_grid = play(grid, player, action)
            eval = alphabeta(next_grid, 3 - player, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval
    
def alphabeta_action(grid: State, player: Player, alpha: float = float('-inf'), beta: float = float('inf')) -> tuple[Score, Action]:
    if final(grid):
        return (score(grid), (-1, -1)) 
    best_score = float('-inf') if player == X else float('inf')
    best_action = None
    for action in legals(grid):
        next_grid = play(grid, player, action)
        eval_score, _ = alphabeta_action(next_grid, 3 - player, alpha, beta)
        if player == X:
            if eval_score > best_score:
                best_score = eval_score
                best_action = action
            alpha = max(alpha, eval_score)
        else:
            if eval_score < best_score:
                best_score = eval_score
                best_action = action
            beta = min(beta, eval_score)
        if beta <= alpha:
            break
    return (best_score, best_action)

def strategy_alphabeta(grid: State, player: Player) -> Action:
    return alphabeta_action(grid, player)[1]
    
def rotate(grid: Grid) -> Grid:
    return tuple(zip(*grid[::-1]))

def reflect(grid: Grid) -> Grid:
    return tuple(tuple(row[::-1]) for row in grid)

def symmetries(grid: Grid) -> list[Grid]:
    grids = []
    g = grid
    for _ in range(4):  # rotations
        grids.append(g)
        grids.append(reflect(g))
        g = rotate(g)
    return grids

def canonical(grid: Grid) -> Grid:
    return min(symmetries(grid))

def memoize_with_symmetry(func: Callable) -> Callable:
    cache = {}
    def memoized_func(grid: State, player: Player, *args):
        key = (canonical(grid), player, *args)
        if key not in cache:
            cache[key] = func(grid, player, *args)
        return cache[key]
    return memoized_func

@memoize_with_symmetry
def minmax_cached_with_symmetry(grid: State, player: Player) -> Score:
    if final(grid):
        return score(grid)
    scores = []
    for action in legals(grid):
        next_grid = play(grid, player, action)
        next_score = minmax_cached_with_symmetry(next_grid, 3 - player)
        scores.append(next_score)
    if player == X:
        return max(scores)
    else:
        return min(scores)

@memoize_with_symmetry
def minmax_action_cached_with_symmetry(grid: State, player: Player, depth: int = 0) -> tuple[Score, Action]:
    if final(grid):
        return (score(grid), (-1, -1)) 
    best_score = float('-inf') if player == X else float('inf')
    best_action = None
    for action in legals(grid):
        next_grid = play(grid, player, action)
        next_score, _ = minmax_action_cached_with_symmetry(next_grid, 3 - player, depth + 1)
        if (player == X and next_score > best_score) or (player == O and next_score < best_score):
            best_score = next_score
            best_action = action
    return (best_score, best_action)

def strategy_minmax_cached_with_symmetry(grid: State, player: Player) -> Action:
    return minmax_action_cached(grid, player)[1]

@memoize_with_symmetry
def minmax_actions_cached_with_symmetry(grid: State, player: Player, depth: int = 0) -> tuple[Score, list[Action]]:
    if final(grid):
        return (score(grid), [])
    best_score = float('-inf') if player == X else float('inf')
    best_actions = []
    for action in legals(grid):
        next_grid = play(grid, player, action)
        next_score, _ = minmax_actions_cached_with_symmetry(next_grid, 3 - player, depth + 1)
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

def strategy_minmax_random_cached_with_symmetry(grid: State, player: Player) -> Action:
    _, actions = minmax_actions_cached_with_symmetry(grid, player)
    return random.choice(actions)

def test_performance(strategy: Strategy):
    start = time.time()
    result = tictactoe(strategy, strategy, debug=False)
    end = time.time()
    print(f"Score: {result}, Temps de calcul : {end - start:.4f} secondes")

def main():
    print("Test sans cache (first legal vs random):")
    tictactoe(strategy_first_legal, strategy_random)

    print("Test minmax SANS cache :")
    start = time.time()
    tictactoe(strategy_minmax, strategy_random)
    print(f"Temps sans cache : {time.time() - start:.4f} secondes")

    print("\nTest minmax AVEC cache :")
    start = time.time()
    tictactoe(strategy_minmax_cached, strategy_random)
    print(f"Temps avec cache : {time.time() - start:.4f} secondes")

    print("\nTest minmax_random SANS cache :")
    start = time.time()
    tictactoe(strategy_minmax_random, strategy_random)
    print(f"Temps sans cache : {time.time() - start:.4f} secondes")

    print("\nTest minmax_random AVEC cache :")
    start = time.time()
    tictactoe(strategy_minmax_random_cached, strategy_random)
    print(f"Temps avec cache : {time.time() - start:.4f} secondes")

    print("\nTest alpha-beta :")
    start = time.time()
    tictactoe(strategy_alphabeta, strategy_random)
    print(f"Temps avec cache : {time.time() - start:.4f} secondes")

    print("\nTest minmax_random AVEC cache ET symétrie :")
    start = time.time()
    tictactoe(strategy_minmax_random_cached_with_symmetry, strategy_random)
    print(f"Temps avec cache : {time.time() - start:.4f} secondes")

if __name__ == "__main__":
    main()