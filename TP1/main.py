from typing import Generator

def decomp(n: int, nb_bits: int) -> list[bool]:
    res:list[bool] = []
    for i in range (nb_bits):
        res.append(False) if n%2==0 else res.append(True)
        n=int(n/2)
    return res

def interpretation(voc: list[str], vals: list[bool]) -> dict[str, bool]:
    if(len(voc)!=len(vals)):
        return BaseException
    
    res:dict[str, bool]={}
    for i in range(len(voc)):
        res[voc[i]]=vals[i]
    return res

def gen_interpretations(voc: list[str]) -> Generator[dict[str, bool], None, None]:    #Un générateur ne prend que très peu de place en mémoire, ce n'est pas uen collection stockée
    for i in range(2**len(voc)):
        yield interpretation(voc, decomp(i, len(voc)))      #yield return la valeur puis mets en pause la fonction

def valuate(formula: str, interpretation: dict[str, bool]) -> bool:
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

def is_valid(formula: str, voc:list[str]) -> bool:
    interpretation:Generator=gen_interpretations(voc)
    for i in range(2**len(voc)):
        if not(valuate(formula, next(interpretation))):
            return False 
    return True

def is_contradictory(formula: str, voc:list[str]) -> bool:
    interpretation:Generator=gen_interpretations(voc)
    for i in range(2**len(voc)):
        if valuate(formula, next(interpretation)):
            return False 
    return True

def is_contagent(formula: str, voc:list[str]) -> bool:
    if not(is_valid(formula, voc)) and not(is_contradictory(formula, voc)):
        return True

def is_cons(f1: str, f2: str, voc: List[str]) -> bool:
    interpretation:Generator=gen_interpretations(voc)
    for i in range(2**len(voc)):
        if not(valuate(f1, next(interpretation))) and valuate(f2, next(interpretation)):
            return False 
    return True

def main() -> None:
    gen_truth_table("(A or B) and not(C)", ["A", "B", "C"])

if __name__ == "__main__":
    main()