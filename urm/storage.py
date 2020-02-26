"""Module contains model of URM-storage"""

from urm.util import nat


def storage(x):
    """Smart constructor for storage"""
    try: 
        return list(map(nat, x))
    except:
        raise ValueError("invalid literal for storage()")


# Assumptions:
#   mem is a correctly created storage
#   addr and val is naturals

def read(mem, addr):
    """Function reads the value located at address 'addr' of storage 'mem'"""
    addr = nat(addr)
    return 0 if addr >= len(mem) else mem[addr]


def write(mem, addr, val):  
    """Function writes value 'val' into storage 'mem' at addres 'addr'"""
    addr = nat(addr)
    need = addr - len(mem) + 1  # lack of memory
    if need > 0:
        mem.extend(need * [0])
    mem[addr] = val
