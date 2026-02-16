import time
import numpy as np
import matplotlib.pyplot as plt

STEP = .001

def gaussian2D(x, y, sigma):
    return (1/(2*np.pi*sigma**2))*np.exp(-1*(x**2+y**2)/(2*sigma**2))
def plot(z):
    plt.imshow(z); plt.xlabel("X"); plt.ylabel("Y")
    plt.title(f"{len(z)} points")
    plt.gca().invert_yaxis()
def main(xmin, xmax, ymin, ymax, sigma=1):
    X = np.arange(xmin, xmax, STEP)
    Y = np.arange(ymin, ymax, STEP)
    Z = []
    for x in X:
        for y in Y:
            Z.append(gaussian2D(x, y, sigma))

    Z = np.array(Z)
    Z = Z.reshape(len(X), len(Y))
    plot(Z)
if __name__ == "__main__":
    start = time.time()
    main(-2, 2, -2, 2, 0.5)
    elapsed = time.time() - start
    print(f"Elapsed Time: {elapsed}s")
    plt.show() # plot after time calc so we're not waiting for plot
