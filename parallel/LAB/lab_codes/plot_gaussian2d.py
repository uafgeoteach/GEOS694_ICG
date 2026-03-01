from glob import glob
import matplotlib.pyplot as plt
import numpy as np


def read(fid="./gaussian2d.npy"):
    return np.load(fid)

def plot(z):
    plt.imshow(z)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(f"{len(z)} points")
    plt.gca().invert_yaxis()

if __name__ == "__main__":
    z = np.array([])
    for fid in sorted(glob("*.npy")):
        z = np.append(z, read(fid))

    plot(z)

