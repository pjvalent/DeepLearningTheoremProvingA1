from collections import namedtuple
from time import perf_counter
import itertools as it
import numpy as np

class Literal(namedtuple("Literal", ("negated", "atom"))):
    def __invert__(self):
        return Literal(not self.negated, self.atom)
    def __repr__(self):
        return ("¬" if self.negated else "") + self.atom

class Clause(frozenset):
    def __repr__(self):
        if len(self) == 0: return "⊥"
        else: return " ∨ ".join(sorted(map(str, self)))

contradiction = Clause()

def parse(cnf_string):
    return set([
        Clause([
            Literal(True, literal[1:]) if literal[0] == "¬" else Literal(False, literal)
            for literal in clause.split("∨")])
        for clause in cnf_string.replace(" ","").split("∧")])

def resolve(P, Q):
    if len(P) > len(Q): P, Q = Q, P
    for p in P:
        if ~p in Q:
            yield Clause((P - {p}) | (Q - {~p}))

class Resolver:

    def __init__(self, clauses, pairs, inferences=None, num_steps=0, parent=None, idx=None):
        self.clauses = clauses
        self.pairs = pairs

        # inferences[clause] = (..., (pair that implies clause), ...)
        self.inferences = inferences if inferences != None else dict()

        # Number of resolution steps performed so far
        self.num_steps = num_steps

        # Previous resolver before most recent step
        self.parent = parent

        # Index of pair selected from previous resolver
        self.idx = idx

    def resolve(self, idx):
        # invariant: every pair of clauses has been pushed on pair queue

        # copy clauses, pairs, and inferences attributes of self
        clauses = set(self.clauses)
        pairs = self.pairs[:idx] + self.pairs[idx+1:] # exclude the pair about to be resolved
        inferences = dict(self.inferences)

        # resolve the selected pair
        for resolvent in resolve(*self.pairs[idx]):

            # add this pair to the list of resolvent's inferences
            if resolvent not in inferences: inferences[resolvent] = tuple()
            inferences[resolvent] += (self.pairs[idx],)

            # move on if this resolvent was already proven and paired previously
            if resolvent in clauses: continue

            # add new resolvent and pair with all existing clauses
            clauses.add(resolvent)
            for clause in clauses:
                pairs.append( (resolvent, clause) )

        return Resolver(clauses, pairs, inferences, self.num_steps + 1, self, idx)

def run(premises, selector = lambda r: 0, timeout = 60):

    start = perf_counter()

    # initialize resolver instance with premises and their pairs
    resolver = Resolver(set(premises), list(it.combinations(premises, 2)))

    # iterate until all pairs have been processed
    while len(resolver.pairs) > 0:

        # Abort at timeout
        if perf_counter() - start > timeout: return None, resolver

        # check for successful proof by contradiction
        if contradiction in resolver.clauses: return True, resolver

        # select a pair index
        idx = selector(resolver)

        # resolve the pair
        resolver = resolver.resolve(idx)

    # no successful proof
    return False, resolver

def model_check(clauses):
    atoms = list({literal.atom for clause in clauses for literal in clause})

    for truth in it.product([True, False], repeat = len(atoms)):
        assignment = {atoms[i]: truth[i] for i in range(len(atoms))}
        
        satisfied = all(
            any(assignment[literal.atom] != literal.negated for literal in clause)
            for clause in clauses)

        if satisfied: return True

    return False

if __name__ == "__main__":

    p = Literal(negated=False, atom='p')
    q = Literal(negated=False, atom='q')

    P = Clause({p})
    Q = Clause({q})
    PQ = Clause({p, q})
    A = Clause({~p, q})
    B = Clause({~p, ~q})

    print(p)
    print(q)
    print(~p)
    print(~~p)
    print(PQ)
    print(A)
    print(contradiction)

    print(set(resolve(PQ, A)))
    print(set(resolve(A, B)))
    print(set(resolve(Clause({p, q, ~p}), Clause({p, q, ~q}))))

    assert p == p
    assert p != q
    assert p != ~p
    assert p == ~~p

    premises = {Clause({p}), Clause({~p})}
    result, resolver = run(premises)
    assert result == True
    assert model_check(premises) != result
    print(resolver.clauses)

    premises = {Clause({p}), Clause({q})}
    result, resolver = run(premises)
    assert result == False
    assert model_check(premises) != result
    print(resolver.clauses)

    # premises = {Clause({p, q}), Clause({p, ~q}), Clause({~q})}
    premises = parse("p ∨ q ∧ p ∨ ¬q ∧ ¬q")
    result, resolver = run(premises)
    assert result == False
    assert model_check(premises) != result
    print(premises)
    print(resolver.clauses)

    premises = {Clause({p, q}), Clause({p, ~q}), Clause({~p})}
    result, resolver = run(premises)
    assert result == True
    assert model_check(premises) != result
    print(resolver.clauses)

    premises = parse("p ∨ q ∨ r ∧ ¬p ∧ ¬q ∧ ¬r")
    result, resolver = run(premises)
    assert result == True
    assert model_check(premises) != result
    print(resolver.clauses)

    premises = parse("p ∨ q ∨ r ∧ ¬p ∧ ¬q")
    result, resolver = run(premises)
    assert result == False
    assert model_check(premises) != result
    print(resolver.clauses)

    # Proving Modus Ponens with resolution
    # ((p -> q) ∧ p) -> q # modus ponens
    # ((p -> q) ∧ p) ∧ ¬q # proof by contradiction
    # ((¬p ∨ q) ∧ p) ∧ ¬q # eliminate ->
    # (¬p ∨ q) ∧ p ∧ ¬q # associative
    premises = parse("¬p ∨ q ∧ p ∧ ¬q")
    result, resolver = run(premises)
    assert result == True
    assert model_check(premises) != result
    print(resolver.clauses)

