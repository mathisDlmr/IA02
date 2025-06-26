from typing import List, Tuple, Callable
import random
from math import sqrt, log
import time

Grid = tuple[tuple[int, ...], ...]
State = Grid
Action = tuple[int, int]
Player = int
Score = float
Strategy = Callable[[State, Player], Action]
ScoreFunction = Callable[[State, Player], Score]

# Quelques constantes
DRAW = 0
EMPTY = 0
X = 1
O = 2

# Constantes de l'examen de TP
N_SIMULATIONS = 100
MAX_DEPTH = 3
N_PLAYOUTS = 1000
CONSTANTE = 0.3

def grid_tuple_to_grid_list(grid: Grid) -> list[list[int]]:
    return [list(row) for row in grid]

def grid_list_to_grid_tuple(grid: list[list[int]]) -> Grid:
    return tuple(tuple(row) for row in grid)

def legals(grid: State) -> list[Action]:
    legs : list[Action] = []
    for line in range(len(grid)):       # On utilisera len(grid) pour retrouver la taille n du Ti-Tac-Toe sachant que la grille est carré
        for col in range(len(grid)):
            if(grid[line][col] == 0):
                legs.append((line, col))
    return legs

def check_lines(grid: State, player: Player) -> bool:
    count: int = 0
    for line in range(len(grid)):
        count = 0
        for col in range(len(grid)):
            if(grid[line][col] == player):
                count+=1
            if count == len(grid):
                return True
    return False

def check_cols(grid: State, player: Player) -> bool:
    count: int = 0
    for line in range(len(grid)):
        count = 0
        for col in range(len(grid)):
            if(grid[col][line] == player):
                count+=1
            if count == len(grid):
                return True
    return False

def check_diags(grid: State, player: Player) -> bool:
    if all(grid[i][i] == player for i in range(len(grid))):
        return True
    if all(grid[i][len(grid)-1-i] == player for i in range(len(grid))):
        return True
    return False

def line(grid: State, player: Player) -> bool:
    return check_lines(grid, player) or check_cols(grid, player) or check_diags(grid, player)

def final(grid: State) -> bool:
    full = all(grid[i][j] != 0 for i in range(len(grid)) for j in range(len(grid)))
    return full or line(grid, X) or line(grid, O)

def score(grid: State) -> Score:
    if line(grid, X):
        return 1
    elif line(grid, O):
        return -1
    else:
        return 0

def pprint(grid: State):
    for line in range(len(grid)):
        for col in range(len(grid)):
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

def tictactoe_n(strategy_X: Strategy, strategy_O: Strategy, n:int, debug: bool = False) -> Score:
    templateGrid: list[list[int]] = [[0 for _ in range(n)] for _ in range(n)]
    grid: State = grid_list_to_grid_tuple(templateGrid)
    #pprint(grid)
    player: Player = X
    while not final(grid):
        if player == X:
            action = strategy_X(grid, X)
            if action == (-1, -1):
                break
            grid = play(grid, X, action)
            player = O
        else: 
            action = strategy_O(grid, O)
            if action == (-1, -1):
                break
            grid = play(grid, O, action)
            player = X
        pprint(grid)
    return score(grid)

def strategy_first_legal(grid: State, player: Player) -> Action:
    return(legals(grid)[0])

def strategy_random(grid: State, player: Player) -> Action:
    legs: list[Action] = legals(grid)
    return (legs[random.randint(0, len(legs)-1)])

def rotate_90(grid: Grid) -> Grid:
    return tuple(zip(*grid[::-1]))

def flip_horizontal(grid: Grid) -> Grid:
    return tuple(row[::-1] for row in grid)

def flip_vertical(grid: Grid) -> Grid:
    return grid[::-1]

def all_symmetries(grid: Grid) -> list[Grid]:   # Génère les 8 symétries (4 rotations et 2 flips)
    symmetries = []
    g = grid
    for _ in range(4):
        symmetries.append(g)
        symmetries.append(flip_horizontal(g))
        g = rotate_90(g)
    return symmetries

def minimal_symetries(grid: Grid) -> Grid:     # Renvoie la symétrie minimale parmis les flips et rotations
    return min(all_symmetries(grid))

def memoize(func: Callable) -> Callable:
    cache = {}

    def memoized_func(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]

    return memoized_func

@memoize
def simulate(grid: State, player: Player) -> Score:
    while not final(grid):
        if player == X:
            action = strategy_random(grid, X)
            grid = play(grid, X, action)
            player = O
        else: 
            action = strategy_random(grid, O)
            grid = play(grid, O, action)
            player = X
    return score(grid)

@memoize
def strategy_monte_carlo(grid: State, player: Player) -> Action:
    bestAction: Action = legals(grid)[0]
    bestMean: int = -1 if player == X else 0   # On initialise avec la pire moyenne possible
    for action in legals(grid):
        nextGrid: Grid = play(grid, player, action)   # Pour chaque action possible, on créé la prochaine grille
        actualMean: int = 0
        for _ in range(N_SIMULATIONS):
            actualMean += simulate(nextGrid, 3 - player)   # On somme les scores des parties simulées à partir de la prochaine grille
        actualMean = actualMean / N_SIMULATIONS   # On calcule la moyenne
        if player == X:
            if actualMean > bestMean:   # Si c'est le jouer max alors on veut la plus grande moyenne
                bestMean = actualMean
                bestAction = action
        elif player == O:
            if actualMean < bestMean:   # Si c'est le joueur min on veut la plus basse
                bestMean = actualMean
                bestAction = action
    return bestAction

@memoize
def minmax_action_depth(grid: State, player: Player, f_score: ScoreFunction, depth: int) -> tuple[Score, Action] :
    if final(grid):
        return (score(grid), (-1, -1)) 
    if depth == 0:
        return (f_score(grid, player), (-1, -1))
    best_score: Score = -1 if player == X else 1  # On init au pire score
    best_action: Action = ()
    for action in legals(grid):
        next_grid: Grid = play(grid, player, action)
        next_score, _ = minmax_action_depth(next_grid, 3 - player, f_score, depth - 1)   # Quand on appelle avec 3 - player on inverse les joueurs
        if (player == X and next_score > best_score) or (player == O and next_score < best_score):
            best_score = next_score
            best_action = action
    return (best_score, best_action)

def MCS(grid: State, player: Player) -> Score:
    scoreSimulation: Score = 0
    for _ in range(N_SIMULATIONS):
        scoreSimulation += simulate(grid, player)                # On simule N_SIMULATIONS de parties 
    scoreSimulation =  scoreSimulation / N_SIMULATIONS           # Et on fait la moyenne 
    return scoreSimulation

def strategy_MCS(grid: State, player: Player) -> Action:
    _, action = minmax_action_depth(grid, player, MCS, MAX_DEPTH)
    return action     # On utilise la meilleure action donnée par le minmax, avec MCS en fonction pour calculer le score et une profondeur MAX_DEPTH

def UCB(grid: State, player: Player) -> tuple[Score, Action]:
    UcbValues: dict[Action, Score] = {}
    for action in legals(grid):
        nextGrid: Grid = play(grid, player, action)
        if player == X:
            UcbValues[action] = score(nextGrid) + CONSTANTE * sqrt(log(N_SIMULATIONS) / N_PLAYOUTS)
        elif player == O:
            UcbValues[action] = score(nextGrid) - CONSTANTE * sqrt(log(N_SIMULATIONS) / N_PLAYOUTS)
    print(UcbValues)
    bestAction: Action = max(UcbValues, key=UcbValues.get)
    return (UcbValues[bestAction], bestAction)

def strategy_UCB(grid: State, player: Player) -> Action:
    return(UCB(grid, player)[1])

@memoize
def minmax_action_ucb(grid: State, player: Player, f_score: ScoreFunction, depth: int) -> tuple[Score, Action] :
    pprint(grid)
    if final(grid):
        return (score(grid), (-1, -1)) 
    if depth == 0:
        return (f_score(grid, player), (-1, -1))
    best_score: Score = -1 if player == X else 1  # On init au pire score
    best_action: Action = ()
    for action in legals(grid):
        next_grid: Grid = play(grid, player, action)
        next_score, _ = minmax_action_ucb(next_grid, 3 - player, f_score, depth - 1)   # Quand on appelle avec 3 - player on inverse les joueurs
        if (player == X and next_score > best_score) or (player == O and next_score < best_score):
            best_score = next_score
            best_action = action
    return (best_score, best_action)

def strategy_minmax_ucb(grid: State, player: Player) -> Action:
    _, action = minmax_action_ucb(grid, player, MCS, MAX_DEPTH)
    return action     # On utilise la meilleure action donnée par le minmax, avec MCS en fonction pour calculer le score et une profondeur MAX_DEPTH

def main():
    print(tictactoe_n(strategy_minmax_ucb, strategy_minmax_ucb, 5))

if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Temps : {time.time() - start:.4f} secondes")