"""
Implement your own premise selector below.
The input is a resolver class instance with two attributes:
- clauses: the set of all clauses proven so far
- pairs: the list of pairs of clauses that can be selected for the next resolution step
The output is an integer, which is an index in the pairs list indicating which pair to select.
"""
import numpy as np

def selector(resolver):

    #get the smallest
    k = np.argmin([len(P) + len(Q) for P,Q in resolver.pairs])
    #get the length of the smallest
    y = len(resolver.pairs[k])
    
    best_pairs = {}
    """
    Find all pairs that are the same length as the smallest, and rank them based on how many inverse atoms are in the pair
    For example, ~p0 in p and p0 in q would +1 to the rank then add it to a dictionary
    """
    for p, q in resolver.pairs:
        if len(p) + len(q) == y:
            similarp = []
            similarq = []
            rank = 0
            for x in p:
                similarp.append(x)
            for i in q:
                similarq.append(i)
            for j in similarp:
                for g in similarq:
                    if ~j == g: #checking for inverse of the atom
                        rank += 1

            best_pairs.update( {(p,q):rank} )  
    
    #sanity check to see if dictionary is populated
    if best_pairs:
        best = max(best_pairs, key=best_pairs.get)
    else:
        return k

    #get the index of the best pair in resolver.pairs
    z = [ (P,Q) for P,Q in resolver.pairs ]
    for i in range(len(z)):
        if z[i] == best:
            return i
    
    #another sanity check. This should never get hit if it does something has gone very wrong
    return k
