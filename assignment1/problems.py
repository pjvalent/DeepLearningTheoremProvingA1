import numpy as np
import itertools as it
from resolution import Literal, Clause, run

def exhaust(num_atoms):
    literals = np.array(tuple(it.product((False, True), range(num_atoms))))
    clauses = np.array(tuple(it.product((False, True), repeat = len(literals))))
    clauses = clauses[1:] # exclude contradiction
    input(f"{len(clauses)} clauses, {2**len(clauses)} cnfs...")

    cnfs = np.array(tuple(it.product((False, True), repeat = len(clauses))))

    return tuple(
        {Clause(Literal(n, "p%d" % a) for (n,a) in literals[clause]) for clause in clauses[cnf]}
        for cnf in cnfs)

def sample(num_atoms):

    literals = np.array(tuple(it.product((False, True), range(num_atoms))))
    clauses = np.array(tuple(it.product((False, True), repeat = len(literals))))
    clauses = clauses[1:] # exclude contradiction
    cnf = np.random.choice((False, True), size = len(clauses))
    return {Clause(Literal(n, "p%d" % a) for (n,a) in literals[clause]) for clause in clauses[cnf]}

if __name__ == "__main__":

    # problems = exhaust(2)

    # for premises in problems:
    #     print(premises)

    # print(len(problems))

    problem = sample(2)

    result, closure = run(problem)
    print(result)
    print(problem)
    print(closure)
    print(f"{len(problem)} -> {len(closure)}")

