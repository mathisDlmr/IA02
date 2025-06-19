from typing import Generator, List, Dict

def decomp(n: int, nb_bits: int) -> list[bool]:
    res: list[bool] = []
    for _ in range(nb_bits):
        res.append(False if n%2==0 else True)
        n=n//2
    res.reverse()
    return res

def interpretation(voc: list[str], vals: list[bool]) -> dict[str, bool]:
    res: dict[str, bool] = {}
    for i in range(len(voc)):
        res[voc[i]] = vals[i]
    return res

def gen_interpretations(voc: List[str]) -> Generator[Dict[str, bool], None, None]:
    for i in range(len(voc)**2):
        yield interpretation(voc, decomp(i, len(voc)))

def valuate(formula: str, interpretation: Dict[str, bool]) -> bool:
    return eval(formula, None, interpretation)

def gen_truth_table(formula: str, voc: list[str]) -> None:
    for i in range(len(voc)): print("+---", end='')
    print("+-------+")
    for i in range(len(voc)): print("|", voc[i], "", end='')
    print("| eval. |")
    for i in range(len(voc)): print("+---", end='')
    print("+-------+")
    
    line_generator:Generator=gen_interpretations(voc)
    for i in range(2**len(voc)):
        line:dict[str, bool]=next(line_generator)
        for var in voc:
            print("|", str(line[var])[0], "", end='')
        print("|", valuate(formula, line),"|")


    for i in range(len(voc)): print("+---", end='')
    print("+-------+")

def isValid(formula: str, voc: List[str]) -> bool:
    for interpt in gen_interpretations(voc):
        if(valuate(formula, interpt)) != True:
            return False
    return True

def isContradictory(formula: str, voc: List[str]) -> bool:
    for interpt in gen_interpretations(voc):
        if(valuate(formula, interpt)) != False:
            return False
    return True

def isContagent(formula: str, voc: List[str]) -> bool:
    return ( not(isValid(formula, voc)) and not(isContradictory(formula, voc)))