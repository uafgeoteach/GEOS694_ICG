# LAB 5: Parallel Python
UAF GEOS694: Introduction to Computational Geosciences  
Bryant Chow

### Description 
In this lab we will play around with Python's `concurrent.futures` package to implement **multiprocessing** in our codes. We will try to understand the "human" cost of implementing true parallelism in our code (i.e., structuring or re-writing), as well as the computational overhead and limitations of implementing concurrency.

### Instructions
- For visual clarity I break the lab into main tasks with sub-tasks below. 
- Each sub-task may build on previous tasks so don't skip around.
- `Reflection` are the reflection questions you will submit on Canvas
- You will upload your final code to GitHub so practice readability through proper code formatting and style (PEP-8)
- Ask for help from your classmates, google/stackoverflow, me, ChatGPT (in that order) if needed.
- You can also use the example notebooks in the course GitHub repository as reference for how to do things

### Context

### Task 1: Serial Code
- Start a new Python script called `2d_gaussian.py`
- Copy the following code block into your new script
```python
import time
import numpy as np
import matplotlib.pyplot as plt

STEP = .001

def gaussian2D(x, y, sigma):
    return (1/(2*np.pi*sigma**2))*np.exp(-1*(x**2+y**2)/(2*sigma**2))
def plot(z):
    plt.imshow(z.T)
    plt.gca().invert_yaxis()  # flip axes to get imshow to plot representatively
    plt.xlabel("X"); plt.ylabel("Y"); plt.title(f"{z.shape} points")
    plt.gca().set_aspect(1)
def main(xmin, xmax, ymin, ymax, sigma=1):
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
```
- Fix up the script by formatting to PEP-8 and adding appropriate docstrings/comments
- Run it in your Python interpreter and make sure you get a plot
- Use the `time` library to determine how long this takes
- This takes about 10s on my laptop, if it takes a lot longer on yours, you can increase the value of `STEP`

#### Reflection
- Is this task embarassingly parallel? Why or why not?
- Is this task IO-bound or CPU-bound? Why? 
- What approach do we need to solve this problem, multithreading or multiprocessing? 
- What can you change about the problem to make it the other type? (i.e., if you chose multithreading, what would be required to make it a multiprocess problem)

---

### Task 2: Easy Parallel
- Copy your script into a new file: 
    ```bash
    cp 2d_gaussian.py 2d_gaussian_embarassing.py
    ```
- Rewrite the script so that is can be embarassingly parallelized with a multiple terminal, Bash script, or subprocess approach (see lecture slides and example scripts in this directory)
- Break the problem into 2 tasks to create 2 individual figures (you do **not** have to combine them)
- Make sure that the final figures actual add up to the figure you got in (1). Save the figures, you will upload them.
- You can write additional scripts, make new files, etc. to make this work, but do not use any concurrency libraries.
- Break this up into 4 tasks to create 4 individual figures


#### Reflection
- Was the total elapsed time to run in parallel shorter or longer than serial, why?
- What would need to change about the problem to get a shorter parallel compute time?
---

### Task 3: Concurrent Futures
- Copy your script into a new file:
    ```bash
    cp 2d_gaussian_embarrasing.py 2d_gaussian_concurrent.py
    ```
- Use `concurrent.futures` to parallelize this problem and create 1 final figure. Do this all in one script.
- Make use the of `submit` and `as_completed` functions
- Set `max_workers` to 4 for now
- Some Tips:
    - Use the documentation, Google, the example from class etc. to help you figure out how to implement this.
    - If you are having trouble, you can hard code things to make things work first, and then generalize once you have something work
    - You can decrease the size of your problem, or reduce the number of `max_workers` 
    - You might test things in a serial for loop to make sure things work as expected before putting them into `concurrent` futures
    - Remember we are doing **multiprocessing** not multithreading
    

#### Reflection
- Was it worth the manual labor of rewriting your code to fit into this paradigm to get the speedup?

--- 
### Task 4: Scaling
- Increase your problem size by changing `STEP` in `2d_gaussian_serial.py` and run it. Find a value of `STEP` so that it takes on the order of a few minutes to run.
- Note down the serial runtime in seconds
- Now run change the value of `STEP` in `2d_gaussian_concurrent.py` and start at `max_workers==1`
- Note down the runtime, and begin incrementing `max_workers` by 1.
- Once you get past the total number of cores on your laptop (`os.get_cpu()`) you can start incrementing by larger values. Try to find the point where the code crashes.
- Make a plot of `max_workers` versus runtime [s]. 

#### Reflection
- What behavior do you observe in your scaling?
- Are there diminishing returns for scaling up?
- What limitations are we running into when we throw more and more cores at it, going past the physical number of cores on our machine?


---
### Task 5: Final Reflection

- Give 2 examples of geoscience/geophysics problems that are embarassingly parallel
- Give 1 example of a geoscience/geophysics problem that cannot be parallelized
- Is parallelizing your code worth it for already-fast calculations?
- Describe a situation when you would not want to implement multiprocessing in your problem
- So far we have solved problems on a single computer with multiple cores. Think about and describe how this might change when we run on a cluster/high performance computer
    - Hint: You can think of a cluster as multiple laptops sitting next to each other, that are all hooked up to the same external harddrive.
    - Think about this in terms of accessing memory, sharing information etc.


Please Submit:
- The code you have written that contains the parallel implementation (upload to GitHub)
- Please include: figures of runtime scaling
- Reflections (submitted on Canvas)
