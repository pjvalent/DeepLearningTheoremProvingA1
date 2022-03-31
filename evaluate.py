from time import perf_counter
import numpy as np
import resolution as rl
import problems as pb
import matplotlib.pyplot as pt

def baseline_selector(resolver):
    return np.argmin([len(P) + len(Q) for P,Q in resolver.pairs])

def evaluate(num_atoms, num_samples, selector):

    run_times = {"baseline": [], "submission": []}
    num_steps = {"baseline": [], "submission": []}
    results = {"baseline": [], "submission": []}

    for n in range(num_samples):
        print(f"{num_atoms} atoms: sample {n}...")
        premises = pb.sample(num_atoms)

        for (name, fn) in [("baseline", baseline_selector), ("submission", selector)]:

            start = perf_counter()
            result, resolver = rl.run(premises, fn, timeout=60)
            run_times[name].append(perf_counter() - start)
            num_steps[name].append(resolver.num_steps)
            results[name].append(result)

        if None not in (results["baseline"][n], results["submission"][n]):
            assert results["baseline"][n] == results["submission"][n]

    return run_times, num_steps, results

if __name__ == "__main__":

    from submission import selector
    # from ref_submission import selector

    pt.figure(figsize=(6,9))

    num_samples = 100
    # num_atoms = 4
    atom_range = list(range(2,4))
    for a,num_atoms in enumerate(atom_range):
    
        run_times, num_steps, results = evaluate(num_atoms, num_samples, selector)
    
        color = [(1,0,0) if result == True else (0,0,1) for result in results["baseline"]]
    
        for k,kpi,name in ((1, run_times, "Run time (s)"), (2, num_steps, "Steps")):
            pt.subplot(len(atom_range), 2, len(results)*a + k)
            pt.scatter(kpi["baseline"], kpi["submission"], color=color)
            mx = max(max(kpi["baseline"]), max(kpi["submission"]))
            pt.plot([0, mx], [0, mx], 'k--')
            pt.xlabel("Baseline")
            pt.ylabel("Submission")
            pt.xscale("log")
            pt.yscale("log")
            pt.title(f"{name} ({num_atoms} atoms)")

    pt.tight_layout()
    pt.show()


