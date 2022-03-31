"""
This "selector" is just a placeholder used to demonstrate the available attributes of the resolver instance.
"""
import resolution as rl
import numpy as np

def selector(resolver):

    print("pair history:")
    res = resolver
    while res.parent != None:
        print(" ",res.parent.pairs[res.idx])
        res = res.parent

    print("last index:")
    print(resolver.idx)

    print("inferences:")
    print(resolver.inferences)

    print("clauses:")
    print(resolver.clauses)

    print("pairs:")
    print(resolver.pairs)

    input("..")

    return np.random.randint(len(resolver.pairs))

if __name__ == "__main__":

    premises = rl.parse("¬p ∨ q ∧ p ∧ ¬q")
    result, resolver = rl.run(premises, selector, timeout=np.inf)
    selector(resolver)

