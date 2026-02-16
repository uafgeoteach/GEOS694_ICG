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
- Start a new Python script called `2d_gaussian_serial.py`
- Copy the following code block into your new script
```python
import time
import numpy as np
import matplotlib.pyplot as plt

STEP = .001

def gaussian2D(x, y, sigma):
    return (1/(2*np.pi*sigma**2))*np.exp(-1*(x**2+y**2)/(2*sigma**2))
def plot(z):
    plt.imshow(z)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(f"{len(z)} points")
    plt.gca().invert_yaxis()
def main(xmin, xmax, ymin, ymax, sigma=1):
    X = np.arange(xmin, xmax, STEP)
    Y = np.arange(ymin, ymax, STEP)
    z = []
    for x in X:
        for y in Y:
            z.append(gaussian2D(x, y, sigma))

    z = np.array(z)
    z = z.reshape(len(X), len(Y))
    plot(z)
if __name__ == "__main__":
    start = time.time()
    main(-2, 2, -2, 2, 0.5)
    elapsed = time.time() - start
    print(f"Elapsed Time: {elapsed}s")
    plt.show()
```
- Fix up the script by formatting to PEP-8 and adding appropriate docstrings/comments
- Run it in your Python interpreter and make sure you get a plot
- Use the `time` library to determine how long this takes

#### Reflection
- Is this task embarassingly parallel? Why or why not?
- Is this task IO-bound or CPU-bound? Why? 
- What approach do we need to solve this problem, multithreading or multiprocessing? 
- What can you change about the problem to make it the other type? (i.e., if you chose multithreading, what would be required to make it a multiprocess problem)

---

### Task 2: Easy Parallel
- Copy your script into a new file: `2d_gaussian_embarassing.py`
- Rewrite the script so that is can be "easily" parallelized with a multiple terminal, Bash script, or subprocess approach (see lecture slides and example scripts in this directory)
- Consider what tasks can be independent, and what tasks require communication
- You can write additional scripts, make new files, etc. to make this work, but do not use any concurrency libraries.
- Break the problem into 4 tasks and create the same output figure as you

---

### Task 2: Parallelize
- Use `concurrent.futures` to parallelize this problem
- Use their documentation, Google, etc. to help you figure out how to implement this
- Use the `time` library to see if you speed things up
- Try different values of `max_workers` and make a plot of time versus `max_workers`
- Try using more workers than there are CPUs on your computer

#### Reflection
- Does this take shorter or longer than the serial approach, why?
- Is this what you expected?
- Does including more processes always lead to faster processing?
- Is speedup linear?
- What happens when you use more workers than there are CPUs?

---
### Task 3: Understanding Overhead
- Make your problem much smaller
- Now time your parallel implementation
- Calculate the time difference

#### Reflection
- Which approach is faster?
- What is the time difference between serial and implementation?
- What do you you attribute that time difference to? 
- Is parallelizing your code worth it for already-fast calculations?

---
### Task 4: Exploring `concurrent.futures`
- Try using the `wait` function
- Try using the `as_completed` function


#### Reflection
- In what situation would you want to use `map` versus `wait` and `as_completed`?
- What if some simulations are more expensive/take longer than others?

--- 
### Task 5: Scaling
- Increase your problem size so that it takes a lot longer to run in serial
- Plot runtime as you scale up to larger and larger problems

#### Reflection
- Are there diminishing returns for scaling up?
- What limitations are we running into when we solve bigger and bigger problems?


---
### Task 6: Final Reflection

- Give 2 examples of geoscience/geophysics problems that are embarassingly parallel
- Give 1 example of a geoscience problem that cannot be parallelized
- Describe a situation when you would not want to implement multiprocessing in your problem
- So far we have solved problems on a single computer with multiple cores. Think about and describe how this might change when we run on a cluster/high performance computer
    - Hint: You can think of a cluster as multiple laptops sitting next to each other, that are all hooked up to the same external harddrive.
    - Think about this in terms of accessing memory, sharing information etc.


Please Submit:
- The code you have written that contains the parallel implementation (upload to GitHub)
- Please include: figures of runtime scaling
- Reflections (submitted on Canvas)
