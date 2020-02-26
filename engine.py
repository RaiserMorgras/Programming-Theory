"""Module contains model of URM-engine"""

from urm.util import *
from urm.storage import * 


def apply(stm, mem):
    """Function applies URM-statement to memeory

    Args:
        stm: statement
        mem: URM-storage
    Returns:
        None if control is passed to the next statement
        addres of the next statement otherwise
    """
  # None for transition to the next statement
#     adrress of the statement
    if stm[0] == 0:  # Z(n)-statement
        write(mem, stm[1], 0)
        return None
    elif stm[0] == 1:  # S(n)-statement
        write(mem, stm[1], read(mem, stm[1]) + 1)
        return None
    elif stm[0] == 2:  # T(n,m)-statement
        write(mem, stm[2], read(mem, stm[1]))
        return None
    else:  # stm[0] == 3  # J(n,m,k)-statement
        if read(mem, stm[1]) == read(mem, stm[2]):
            return stm[3]
        return None


def run(prgm, *args):  
    """Function executes computing

    Args:
        prgm: list of statements
        args: input data
    Returns
        result of running if the program 'prgm' halts
    """
    mem = [0]
    mem.extend(list(args))
    ic, lprgm = 1, len(prgm)
    while 1 <= ic <= lprgm:
        stm = prgm[ic - 1]
        ii = apply(stm, mem)
        ic = ic + 1 if ii is None else ii 
    return read(mem, 0)

