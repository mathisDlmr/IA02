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
    return [[i for i in j] for j in grid]

def grid_list_to_grid_tuple(grid: list[list[int]]) -> Grid:
    return (tuple(tuple(row) for row in grid))

def legals(grid: State) -> list[Action]:
    res : list[Action] = []
    for i in range(3):
        for j in range(3):
            if grid[i][j] == 0:
                res.append((i, j))
    return res

def rows(grid: State, player: Player) -> bool:
    for i in range(3):
        count: int = 0
        for j in range(3):
            if grid[i][j]==player:
                count+=1
        if count == 3:
            return True
    return False

def cols(grid: State, player: Player) -> bool:
    for i in range(3):
        count: int = 0
        for j in range(3):
            if grid[j][i]==player:
                count+=1
        if count == 3:
            return True
    return False

def diags(grid: State, player: Player) -> bool:
    if all(grid[i][i] == player for i in range(3)):
        return True
    if all(grid[i][2-i] == player for i in range(3)):
        return True
    return False

def line(grid: State, player: Player) -> bool:
    return rows(grid, player) or cols(grid, player) or diags(grid, player)

def final(grid: State) -> bool:
    return line(grid, X) or line(grid, O) or (legals(grid) == [])

def score(grid: State) -> Score:
    if line(grid, X):
        return 1
    if line(grid, O):
        return -1
    return 0

def pprint(grid: State):
    for i in range(3):
        for j in range(3):
            if grid[i][j] == 0:
                print(".", end=" ")
            elif grid[i][j] == 1:
                print("X", end=" ")
            else:
                print("O", end=" ")
        print()
    print()

def play(grid: State, player: Player, action: Action) -> State:
    new_state:[[int]] = grid_tuple_to_grid_list(grid)
    new_state[action[0]][action[1]] = player
    return grid_list_to_grid_tuple(new_state)

def tictactoe(strategy_X: Strategy, strategy_O: Strategy, debug: bool = False) -> Score:
    grid: Grid = GRID_0
    pprint(grid)
    player: int = X
    while(not(final(grid))):
        if player == X:
            grid = play(grid, player, strategy_X(grid, X))
        if player == O:
            grid = play(grid, player, strategy_O(grid, O))
        player = 3 - player
        pprint(grid)
    return score(grid)

def strategy_first_legal(grid: State, player: Player) -> Action:
    return legals(grid)[0]

def strategy_random(grid: State, player: Player) -> Action:
    legs = legals(grid)
    return legs[random.randint(0, len(legs)-1)]

def minmax(grid: State, player: Player) -> Score:
    if final(grid):
        return score(grid)
    if player == X:
        bestValue: int = float('-inf')
        for action in legals(grid):
            child: Grid = play(grid, 3-player, action)
            v = minmax(child, 3-player)
            bestValue = max(bestValue, v)
    else:
        bestValue: int = float('+inf')
        for action in legals(grid):
            child: Grid = play(grid, 3-player, action)
            v = minmax(child, 3-player)
            bestValue = min(bestValue, v)
    return bestValue

def minmax_action(grid: State, player: Player, depth: int = 0) -> tuple[Score, Action]:
    if final(grid):
        return score(grid)
    if player == X:
        bestValue: int = float('-inf')
        for action in legals(grid):
            child: Grid = play(grid, 3-player, action)
            v = minmax(child, 3-player)
            if v > bestValue:
                bestValue = v
                bestAction: Action = action
    else:
        bestValue: int = float('+inf')
        for action in legals(grid):
            child: Grid = play(grid, 3-player, action)
            v = minmax(child, 3-player)
            if v < bestValue:
                bestValue = v
                bestAction: Action = action
    return (bestValue, bestAction)

def strategy_minmax(grid: State, player: Player) -> Action:
    return minmax_action(grid, player)[1]

def minmax_actions(grid: State, player: Player, depth: int = 0) -> tuple[Score, list[Action]]:
    if final(grid):
        return score(grid)
    bestAction: list[Action] = []
    if player == X:
        bestValue: int = float('-inf')
        for action in legals(grid):
            child: Grid = play(grid, 3-player, action)
            v = minmax(child, 3-player)
            if v > bestValue:
                bestValue = v
                bestAction = [action]
            elif v == bestValue:
                bestAction.append(action)
    else:
        bestValue: int = float('+inf')
        for action in legals(grid):
            child: Grid = play(grid, 3-player, action)
            v = minmax(child, 3-player)
            if v < bestValue:
                bestValue = v
                bestAction = [action]
            elif v == bestValue:
                bestAction.append(action)
    return (bestValue, bestAction)

def strategy_minmax_random(grid: State, player: Player) -> Action:
    actions: list[Action] = minmax_actions(grid, player)
    return actions[random.randint(0, len(actions)-1)]

def memoize(f: Callable[[State, Player], tuple[Score, Action]]) -> Callable[[State, Player], tuple[Score, Action]]:
    cache = {} # closure
    def g(grid: State, player: Player):
        if grid in cache:
            return cache[grid]
        val = f(grid, player)
        cache[grid] = val
        return val
    return g

@memoize
def minmax_action_cached(grid: State, player: Player, depth: int = 0) -> tuple[Score, Action]:
    if final(grid):
        return score(grid)
    if player == X:
        bestValue: int = float('-inf')
        for action in legals(grid):
            child: Grid = play(grid, 3-player, action)
            v = minmax(child, 3-player)
            if v > bestValue:
                bestValue = v
                bestAction: Action = action
    else:
        bestValue: int = float('+inf')
        for action in legals(grid):
            child: Grid = play(grid, 3-player, action)
            v = minmax(child, 3-player)
            if v < bestValue:
                bestValue = v
                bestAction: Action = action
    return (bestValue, bestAction)

def strategy_minmax_cached(grid: State, player: Player) -> Action:
    return minmax_action_cached(grid, player)[1]

@memoize
def minmax_actions_cached(grid: State, player: Player, depth: int = 0) -> tuple[Score, list[Action]]:
    if final(grid):
        return score(grid)
    bestAction: list[Action] = []
    if player == X:
        bestValue: int = float('-inf')
        for action in legals(grid):
            child: Grid = play(grid, 3-player, action)
            v = minmax(child, 3-player)
            if v > bestValue:
                bestValue = v
                bestAction = [action]
            elif v == bestValue:
                bestAction.append(action)
    else:
        bestValue: int = float('+inf')
        for action in legals(grid):
            child: Grid = play(grid, 3-player, action)
            v = minmax(child, 3-player)
            if v < bestValue:
                bestValue = v
                bestAction = [action]
            elif v == bestValue:
                bestAction.append(action)
    return (bestValue, bestAction)

def strategy_minmax_random_cached(grid: State, player: Player) -> Action:
    actions: list[Action] = minmax_actions_cached(grid, player)
    return actions[random.randint(0, len(actions)-1)]

def alphabeta_action(grid: State, player: Player, a:float, b:float, depth: int = 0) -> tuple[Score, Action]:
    if final(grid):
        return score(grid)
    if player == X:
        bestValue: int = float('-inf')
        for action in legals(grid):
            child: Grid = play(grid, 3-player, action)
            v = alphabeta_action(child, 3-player, a, b)
            if v > bestValue:
                bestValue = v
                bestAction: Action = action
            a = max(a, v)
            if a >= b:
                break
    else:
        bestValue: int = float('+inf')
        for action in legals(grid):
            child: Grid = play(grid, 3-player, action)
            v = alphabeta_action(child, 3-player, a, b)
            if v < bestValue:
                bestValue = v
                bestAction: Action = action
            b = min(b, v)
            if a >= b:
                break
    return (bestValue, bestAction)

def strategy_alphabeta(grid: State, player: Player) -> Action:
    return alphabeta_action(grid, player, float('-inf'), float('inf'))

def alphabeta_actions(grid: State, player: Player, a:float, b:float, depth: int = 0) -> tuple[Score, list[Action]]:
    if final(grid):
        return score(grid)
    bestAction: list[Action] = []
    if player == X:
        bestValue: int = float('-inf')
        for action in legals(grid):
            child: Grid = play(grid, 3-player, action)
            v = alphabeta_action(child, 3-player, a, b)
            if v > bestValue:
                bestValue = v
                bestAction = [action]
            if v == bestValue:
                bestAction.append(action)
            a = max(a, v)
            if a >= b:
                break
    else:
        bestValue: int = float('+inf')
        for action in legals(grid):
            child: Grid = play(grid, 3-player, action)
            v = alphabeta_action(child, 3-player, a, b)
            if v < bestValue:
                bestValue = v
                bestAction = [action]
            if v == bestValue:
                bestAction.append(action)
            b = min(b, v)
            if a >= b:
                break
    return (bestValue, bestAction)

def strategy_alphabeta_random(grid: State, player: Player) -> Action:
    actions: list[Action] = alphabeta_actions(grid, player, float('-inf'), float('inf'))
    return actions[random.randint(0, len(actions)-1)]

@memoize
def alphabeta_action_cached(grid: State, player: Player, a:float, b:float, depth: int = 0) -> tuple[Score, Action]:
    if final(grid):
        return score(grid)
    if player == X:
        bestValue: int = float('-inf')
        for action in legals(grid):
            child: Grid = play(grid, 3-player, action)
            v = alphabeta_action(child, 3-player, a, b)
            if v > bestValue:
                bestValue = v
                bestAction: Action = action
            a = max(a, v)
            if a >= b:
                break
    else:
        bestValue: int = float('+inf')
        for action in legals(grid):
            child: Grid = play(grid, 3-player, action)
            v = alphabeta_action(child, 3-player, a, b)
            if v < bestValue:
                bestValue = v
                bestAction: Action = action
            b = min(b, v)
            if a >= b:
                break
    return (bestValue, bestAction)

def strategy_alphabeta_cached(grid: State, player: Player) -> Action:
    return alphabeta_action_cached(grid, player, float('-inf'), float('inf'))

@memoize
def alphabeta_actions_cached(grid: State, player: Player, a:float, b:float, depth: int = 0) -> tuple[Score, list[Action]]:
    if final(grid):
        return score(grid)
    bestAction: list[Action] = []
    if player == X:
        bestValue: int = float('-inf')
        for action in legals(grid):
            child: Grid = play(grid, 3-player, action)
            v = alphabeta_action(child, 3-player, a, b)
            if v > bestValue:
                bestValue = v
                bestAction = [action]
            if v == bestValue:
                bestAction.append(action)
            a = max(a, v)
            if a >= b:
                break
    else:
        bestValue: int = float('+inf')
        for action in legals(grid):
            child: Grid = play(grid, 3-player, action)
            v = alphabeta_action(child, 3-player, a, b)
            if v < bestValue:
                bestValue = v
                bestAction = [action]
            if v == bestValue:
                bestAction.append(action)
            b = min(b, v)
            if a >= b:
                break
    return (bestValue, bestAction)

def strategy_alphabeta_random_cached(grid: State, player: Player) -> Action:
    actions: list[Action] = alphabeta_actions_cached(grid, player, float('-inf'), float('inf'))
    return actions[random.randint(0, len(actions)-1)]

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
    tictactoe(strategy_alphabeta_cached, strategy_random)
    print(f"Temps avec cache : {time.time() - start:.4f} secondes")

if __name__ == "__main__":
    main()





