import sys
import time
import numpy as np
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor, as_completed

STEP = .001

def gaussian2D(x, y, sigma):
    return (1/(2*np.pi*sigma**2))*np.exp(-1*(x**2+y**2)/(2*sigma**2))

def plot(z):
    plt.imshow(z.T)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(f"{len(z)} points")
    plt.gca().invert_yaxis()
    plt.gca().set_aspect("equal")

def main(limit, sigma=1):
    xmin, xmax, ymin, ymax = limit
    X = np.arange(float(xmin), float(xmax), STEP)
    Y = np.arange(float(ymin), float(ymax), STEP)
    Z = []  # 1D array
    for x in X:
        for y in Y:
            Z.append(gaussian2D(x, y, sigma))
    return np.array(Z)


if __name__ == "__main__":
    start = time.time()

    max_workers = 4
    serial = False
    race_condition = True

    xmin = float(sys.argv[1])
    xmax = float(sys.argv[2])
    ymin = float(sys.argv[3])
    ymax = float(sys.argv[4])

    X = np.arange(float(xmin), float(xmax), STEP)
    Y = np.arange(float(ymin), float(ymax), STEP)

    # Break the problem into chunks that we can easily feed into `main`
    limits = []  # [xmin, xmax, ymin, ymax]
    x0 = xmin
    for x1 in np.linspace(xmin, xmax, max_workers + 1)[1:]:
        limits.append([int(x0), int(x1), ymin, ymax])
        x0 = x1
    
    z = np.array([])
    # Submit does not retain order so it will create a race condition
    if race_condition:
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(main, limit) for limit in limits]
        for future in as_completed(futures):
            z = np.append(z, future.result())
    # Map retains order but we will have a different call structure
    else:
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            results = executor.map(main, limits)
        for result in results:
            z = np.append(z, result)

    plot(z.reshape(len(X), len(Y)))

    elapsed = time.time() - start
    print(f"Total Elapsed: {elapsed:.2f}s")
    plt.show()

