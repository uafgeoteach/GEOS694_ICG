import matplotlib.pyplot as plt
import numpy as np
import time

STEP = .001

def gaussian2D(x, y, sigma):
    """
    for given x, y, sigma, returns equations for a two-dimensional 
    gaussian distribution
    """
    return (1 / (2 * np.pi * sigma**2)) * np.exp(-1 * (x**2 + y**2)/(2 * sigma**2))

    
def plot(z):
    """plots a two-dimensional array as a heatmap"""
    plt.imshow(z.T)
    plt.gca().invert_yaxis()  # flip axes to get imshow to plot representatively
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(f"{z.shape} points")
    plt.gca().set_aspect(1)

    
def main(xmin, xmax, ymin, ymax, sigma=1):
    """
    for given min and max x-, y-values and a sigma value, creates and plots 
    a two-dimensional gaussian distribution.
    """
    X = np.arange(float(xmin), float(xmax), STEP)
    Y = np.arange(float(ymin), float(ymax), STEP)
    Z = []  # 1D array
    for x in X:
        for y in Y:
            Z.append(gaussian2D(x, y, sigma))
    
    ZZ = np.array(Z).reshape(len(X), len(Y))  # 2D array
    plot(ZZ)

    
if __name__ == "__main__":
    start = time.time()
    main(-2, 2, -2, 2)
    elapsed = time.time() - start
    print(f"Elapsed Time: {elapsed}s")
    plt.show()