from urm.engine import run

def mem_required(prgm): 
	'''
	Function that takes a program and calculates how much memory it will use.
	At least 1 is always returned.
	Args:
		prgm: the program which memory usage is to be calculated
	Returns:
		a number of how many cells of memory is needed for prgm
	'''
	tmp_mem_size = 0
	for stmnt in prgm:
		## for Z and S commands
		if stmnt[0] == 0 or stmnt[0] == 1: 
			tmp_mem_size = max(tmp_mem_size, stmnt[1]) 
		## for T and J commands, third argument of J is not related to memory
		else: 
			tmp_mem_size = max(tmp_mem_size, stmnt[1], stmnt[2]) 
	return tmp_mem_size + 1


def superposition(f_num_args, g_num_args, f_prgm, *g_prgms):
	'''
	Function that takes an outer program, a number of inner programs and produces their superposition.
	Args:
        f_num_args: number of arguments in outer function
		g_num_args: number of arguments in inner functions
		f_prgm: the program for outer function
		g_prgms: the programs for inner functions
    Returns:
        a program that represents a superposition of outer function with inner functions provided as programs
	Raises:
		ValueError if f_num_args doesn't match the number of given g_prgms
	'''
	if f_num_args != len(g_prgms):
		raise ValueError("Number of arguments for \"f\" program doesn't meet the number of \"g\" programs")
		
	composed_program = []
	translate_g_results = []
	
	f_mem_occupation = mem_required(f_prgm)
	if f_mem_occupation < f_num_args + 1:
		f_mem_occupation = f_num_args + 1
		
	mem_offset = f_mem_occupation
	statement_offset = 0
	
	
	for i in range(f_num_args):
		g_mem_occupation = mem_required(g_prgms[i])
		if g_mem_occupation < g_num_args + 1:
			g_mem_occupation = g_num_args + 1
		
		for j in range(1, g_num_args + 1):
			composed_program.append((2, j, j + mem_offset)) # T(j, j + mem_offset)
		statement_offset += g_num_args
		for stmnt in g_prgms[i]:
			if stmnt[0] == 0 or stmnt[0] == 1:
				composed_program.append((stmnt[0], stmnt[1] + mem_offset))
			elif stmnt[0] == 2:
				composed_program.append((stmnt[0], stmnt[1] + mem_offset, stmnt[2] + mem_offset))
			else:
				if (stmnt[3] != 0):
					composed_program.append((stmnt[0], stmnt[1] + mem_offset, stmnt[2] + mem_offset, stmnt[3] + statement_offset))
				else:
					composed_program.append((stmnt[0], stmnt[1] + mem_offset, stmnt[2] + mem_offset, len(g_prgms[i]) + statement_offset))
				
		translate_g_results.append((2, mem_offset,  i + 1)) # T(mem_offset, i+1)
				
		mem_offset += g_mem_occupation
		statement_offset += len(g_prgms[i])
		
	composed_program.extend(translate_g_results)
	statement_offset += len(translate_g_results)
	for stmnt in f_prgm: 
		if stmnt[0] != 3:
			composed_program.append(stmnt)
		else:
			if (stmnt[3] != 0):
				composed_program.append((stmnt[0], stmnt[1], stmnt[2], stmnt[3] + statement_offset))
			else:
				composed_program.append((stmnt[0], stmnt[1], stmnt[2], 0))
	return composed_program
	
def primitive_recursion(f_num_args, f_prgm, g_prgm):
	'''
	Function that builds a primitive recursion of two given functions.
	Args:
        f_num_args: number of arguments in zero iteration function
		f_prgm: the program for zero iteration function, that takes as much as (f_num_args) arguments
		g_prgms: the programs for non-zero iteration function, that takes as much as (f_num_args+2) arguments
    Returns:
        a program that represents a primitive recursion of two given functions provided as programs
	'''
	composed_program = []
	mem_offset = f_num_args + 3
	composed_program.append((0, f_num_args + 2)) # Z(f_num_args + 2), that's where we will calc iterations
	for i in range (1, f_num_args + 1):
		composed_program.append((2, i, mem_offset + i)) # T(i, mem_offset + i), copying args to iteration memory
	
	statement_offset = 1 + f_num_args
	for stmnt in f_prgm: 
		if stmnt[0] == 0 or stmnt[0] == 1:
			composed_program.append((stmnt[0], stmnt[1] + mem_offset))
		elif stmnt[0] == 2:
			composed_program.append((stmnt[0], stmnt[1] + mem_offset, stmnt[2] + mem_offset))
		else:
			if (stmnt[3] != 0):
				composed_program.append((stmnt[0], stmnt[1] + mem_offset, stmnt[2] + mem_offset, stmnt[3] + statement_offset))
			else:
				composed_program.append((stmnt[0], stmnt[1] + mem_offset, stmnt[2] + mem_offset, len(f_prgm) + statement_offset + 1))
			
	statement_offset += len(f_prgm)
	cycle_begin_statement_num = statement_offset + 1
	composed_program.append((2, f_num_args + 3, 0)) # T(f_num_args + 3, 0) Save the iteration result as output
	composed_program.append((3, f_num_args + 1, f_num_args + 2, 0)) 
	for i in range (1, f_num_args + 1):
		composed_program.append((2, i, mem_offset + i)) # T(i, mem_offset + i), copying args to iteration memory
	composed_program.append((2, f_num_args + 2, mem_offset + f_num_args + 1)) # T(i, f_num_args + 2, mem_offset + f_num_args + 1), copying the number of iteration
	composed_program.append((2, f_num_args + 3, mem_offset + f_num_args + 2)) # T(i, f_num_args + 3, mem_offset + f_num_args + 2), copying the result of prev iteration into argument of next
	composed_program.append((0, f_num_args + 3)) # Z(f_num_args + 3), zeroing the cell used for iteration result
	statement_offset += 5 + f_num_args
	
	for stmnt in g_prgm:
		if stmnt[0] == 0 or stmnt[0] == 1:
			composed_program.append((stmnt[0], stmnt[1] + mem_offset))
		elif stmnt[0] == 2:
			composed_program.append((stmnt[0], stmnt[1] + mem_offset, stmnt[2] + mem_offset))
		else:
			if (stmnt[3] != 0):
				composed_program.append((stmnt[0], stmnt[1] + mem_offset, stmnt[2] + mem_offset, stmnt[3] + statement_offset))
			else:
				composed_program.append((stmnt[0], stmnt[1] + mem_offset, stmnt[2] + mem_offset, len(g_prgm) + statement_offset))
	composed_program.append((1, f_num_args + 2))
	composed_program.append((3, 0, 0, cycle_begin_statement_num))
	return composed_program
	
def minimization(f_num_args, f_prgm):
	'''
	Function that builds a minimization of the given function.
	Args:
        f_num_args: number of arguments in zero iteration function
		f_prgm: the program representing a function to be minimized, that takes as much as (f_num_args) arguments
    Returns:
        a program that represents a function that is a minimization of provided function, and takes (f_num_args - 1)
	Raises:
		ValueError if f_num_args equals zero
	'''
	if (f_num_args == 0)
		raise ValueError("Function with zero arguments cannot be minimized")
	composed_program = []
	mem_offset = f_num_args + 1 # reserve for result of iteration
	composed_program.append((0, f_num_args)) # Z(f_num_args), that cell will be used for iteration
	for i in range (1, f_num_args + 1):
		composed_program.append((2, i, mem_offset + i)) # T(i, mem_offset + i), copying args to iteration memory
	statement_offset = 1 + f_num_args
	for stmnt in f_prgm: 
		if stmnt[0] == 0 or stmnt[0] == 1:
			composed_program.append((stmnt[0], stmnt[1] + mem_offset))
		elif stmnt[0] == 2:
			composed_program.append((stmnt[0], stmnt[1] + mem_offset, stmnt[2] + mem_offset))
		else:
			if (stmnt[3] != 0):
				composed_program.append((stmnt[0], stmnt[1] + mem_offset, stmnt[2] + mem_offset, stmnt[3] + statement_offset))
			else:
				composed_program.append((stmnt[0], stmnt[1] + mem_offset, stmnt[2] + mem_offset, len(f_prgm) + statement_offset +1))
	composed_program.append((3, 0, f_num_args + 1, statement_offset + len(f_prgm) + 4))
	composed_program.append((1, f_num_args))
	composed_program.append((3, 0, 0, 2))
	composed_program.append((2, f_num_args, 0))
	return composed_program