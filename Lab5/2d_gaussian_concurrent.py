
######################

import matplotlib.pyplot as plt
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed
import time

STEP = .0002

def gaussian2D(x, y, sigma=1):
    return ((1 / (2 * np.pi * sigma**2)) * np.exp(-1 * (x**2 + y**2)/(2 * sigma**2)))

def main(xmin, xmax, ymin, ymax):
    X = np.arange(float(xmin), float(xmax), STEP)
    Y = np.arange(float(ymin), float(ymax), STEP)
    Z = []
    for x in X:
        for y in Y:
            Z.append(gaussian2D(x, y))
    return np.array(Z).reshape(len(X), len(Y))

if __name__ == "__main__":
    xmin, xmax, ymin, ymax = -2, 2, -2, 2
    core_counts = list(range(1, 61, 2))
    runtimes = []

    for nproc in core_counts:
        start = time.time()
        
        y_bounds = np.linspace(ymin, ymax, nproc + 1)
        futures_map = {}
        results = [None] * nproc 

        with ProcessPoolExecutor(max_workers=nproc) as executor:
            for i in range(nproc):
                f = executor.submit(main, xmin, xmax, y_bounds[i], y_bounds[i+1])
                futures_map[f] = i 

            for f in as_completed(futures_map):
                index = futures_map[f]
                results[index] = f.result()

        final_ZZ = np.concatenate(results, axis=1)
        
        elapsed = time.time() - start
        runtimes.append(elapsed)
        print(f"Tested {nproc} cores: {elapsed:.2f}s")
    
    plt.figure(figsize=(10, 6))
    plt.plot(core_counts, runtimes, 'o-')
    plt.xlabel("Number of Cores")
    plt.ylabel("Execution Time (seconds)")
    plt.title("Scaling Performance")
    plt.grid(True)
    plt.show()