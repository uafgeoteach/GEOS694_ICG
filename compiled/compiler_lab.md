## Lab: Making Python Fast — A Practical Guide to JIT and Cython

**Duration:** 2 hours | **Level:** Graduate | **Prerequisites:** Basic Python and NumPy familiarity

---

### Overview

You will take a single slow geoscience computation and progressively speed it up using three approaches: pure Python, Numba JIT, and Cython. You'll measure the speedup at each step and reflect on whether the performance gain was worth the effort. By the end you should have an intuition for *when* to reach for these tools in your own research.

---

### Setup (10 minutes)

Create a fresh directory and install the required packages:

```bash
mkdir python_speed_lab && cd python_speed_lab
pip install numba cython numpy matplotlib jupyter
```

All exercises will be done in a single Jupyter notebook. Create it:

```bash
jupyter notebook lab.ipynb
```

At the top of your notebook, add this timing helper that you'll reuse throughout:

```python
import numpy as np
import time
import matplotlib.pyplot as plt

def benchmark(func, *args, repeats=5):
    """Run a function several times and return the median runtime in seconds."""
    times = []
    for _ in range(repeats):
        start = time.perf_counter()
        result = func(*args)
        end = time.perf_counter()
        times.append(end - start)
    return np.median(times), result
```

---

### The Problem: Computing a Heat Index Field

You have a 2D grid of temperature and relative humidity values — think of a reanalysis field over a continent. Your task is to compute the **Heat Index** at every grid point using a simplified version of the NOAA formula, which involves a polynomial with cross terms and is deliberately *not* expressible as a simple NumPy vectorized operation in its full form.

```python
# --- Paste this into your notebook ---

def heat_index_point(T, RH):
    """
    Compute heat index at a single grid point.
    T in Fahrenheit, RH in percent (0-100).
    Simplified Rothfusz regression.
    """
    HI = (-42.379
          + 2.04901523 * T
          + 10.14333127 * RH
          - 0.22475541 * T * RH
          - 0.00683783 * T * T
          - 0.05481717 * RH * RH
          + 0.00122874 * T * T * RH
          + 0.00085282 * T * RH * RH
          - 0.00000199 * T * T * RH * RH)
    return HI

# Generate a realistic test grid — 500x500 points
np.random.seed(42)
NLAT, NLON = 500, 500
temperature = np.random.uniform(90, 110, (NLAT, NLON))   # degrees F
humidity    = np.random.uniform(40, 90,  (NLAT, NLON))   # percent
```

---

### Exercise 1: Pure Python Baseline (20 minutes)

**Task:** Implement the heat index computation as a nested loop over the grid. This is the "naive" approach a researcher might write first.

```python
def heat_index_python(temp, rh):
    nlat, nlon = temp.shape
    result = np.empty((nlat, nlon))
    for i in range(nlat):
        for j in range(nlon):
            result[i, j] = heat_index_point(temp[i, j], rh[i, j])
    return result

# Benchmark it
time_python, result_python = benchmark(heat_index_python, temperature, humidity)
print(f"Pure Python: {time_python:.3f} seconds")
```

Record your result. This is your **baseline**.

**Checkpoint questions before moving on:**
- How long did it take? Does that feel fast or slow to you?
- If this grid were 5000×5000 (roughly global reanalysis at 0.1° resolution), how long would you expect it to take? Make a prediction.

---

### Exercise 2: NumPy Vectorization (15 minutes)

Before reaching for Numba or Cython, the first question is always: *can I just vectorize it?* Here the formula is a polynomial — it can be expressed directly on arrays.

**Task:** Rewrite `heat_index_python` to operate on entire arrays at once using NumPy, with no Python loops.

```python
def heat_index_numpy(temp, rh):
    T, RH = temp, rh
    HI = (-42.379
          + 2.04901523 * T
          + 10.14333127 * RH
          # ... complete the formula yourself
         )
    return HI

time_numpy, result_numpy = benchmark(heat_index_numpy, temperature, humidity)
print(f"NumPy:       {time_numpy:.3f} seconds")
print(f"Speedup vs Python: {time_python / time_numpy:.1f}x")

# Verify correctness
np.testing.assert_allclose(result_python, result_numpy, rtol=1e-5)
print("Results match.")
```

**Checkpoint questions:**
- How much faster is NumPy? Were you surprised?
- How long did the rewrite take you? Was it straightforward?
- NumPy vectorization isn't always possible. Can you think of a geoscience calculation that *can't* be expressed this way? (Hint: think about anything where the value at one grid point depends on a neighbor, or involves a conditional that varies per point.)

---

### Exercise 3: Numba JIT (20 minutes)

Now apply Numba to the *original loop version* — no rewriting required.

```python
from numba import jit

@jit(nopython=True)
def heat_index_numba(temp, rh):
    nlat, nlon = temp.shape
    result = np.empty((nlat, nlon))
    for i in range(nlat):
        for j in range(nlon):
            T  = temp[i, j]
            RH = rh[i, j]
            result[i, j] = (-42.379
                            + 2.04901523 * T
                            + 10.14333127 * RH
                            - 0.22475541 * T * RH
                            - 0.00683783 * T * T
                            - 0.05481717 * RH * RH
                            + 0.00122874 * T * T * RH
                            + 0.00085282 * T * RH * RH
                            - 0.00000199 * T * T * RH * RH)
    return result

# First call triggers compilation — time it separately
start = time.perf_counter()
_ = heat_index_numba(temperature, humidity)
compile_time = time.perf_counter() - start
print(f"Numba first call (includes compilation): {compile_time:.3f} seconds")

# Now benchmark the compiled version
time_numba, result_numba = benchmark(heat_index_numba, temperature, humidity)
print(f"Numba (after warmup): {time_numba:.3f} seconds")
print(f"Speedup vs Python: {time_python / time_numba:.1f}x")
print(f"Speedup vs NumPy:  {time_numpy / time_numba:.1f}x")

np.testing.assert_allclose(result_python, result_numba, rtol=1e-5)
print("Results match.")
```

**Checkpoint questions:**
- How does the first-call time compare to subsequent calls? What does this tell you about when Numba is and isn't appropriate?
- You added exactly one decorator (`@jit`) and inlined the formula. How long did that take you? How does the effort compare to the speedup?
- When would you *not* want to use Numba? (Hint: think about code you run once, or code that uses libraries Numba doesn't support.)

---

### Exercise 4: Cython (30 minutes)

Cython requires more effort — you write a separate file and compile it. This is intentional: the goal is to feel the difference in workflow.

**Step 1:** Create a file called `heat_index_cy.pyx`:

```python
# heat_index_cy.pyx
import numpy as np
cimport numpy as np

def heat_index_cython(np.ndarray[double, ndim=2] temp,
                      np.ndarray[double, ndim=2] rh):
    cdef int nlat = temp.shape[0]
    cdef int nlon = temp.shape[1]
    cdef double T, RH
    cdef int i, j
    cdef np.ndarray[double, ndim=2] result = np.empty((nlat, nlon))

    for i in range(nlat):
        for j in range(nlon):
            T  = temp[i, j]
            RH = rh[i, j]
            result[i, j] = (-42.379
                            + 2.04901523 * T
                            + 10.14333127 * RH
                            - 0.22475541 * T * RH
                            - 0.00683783 * T * T
                            - 0.05481717 * RH * RH
                            + 0.00122874 * T * T * RH
                            + 0.00085282 * T * RH * RH
                            - 0.00000199 * T * T * RH * RH)
    return result
```

**Step 2:** Create `setup.py` to compile it:

```python
# setup.py
from setuptools import setup
from Cython.Build import cythonize
import numpy as np

setup(
    ext_modules=cythonize("heat_index_cy.pyx"),
    include_dirs=[np.get_include()]
)
```

**Step 3:** Compile it from your terminal:

```bash
python setup.py build_ext --inplace
```

**Step 4:** Back in your notebook:

```python
from heat_index_cy import heat_index_cython

time_cython, result_cython = benchmark(heat_index_cython, temperature, humidity)
print(f"Cython: {time_cython:.3f} seconds")
print(f"Speedup vs Python: {time_python / time_cython:.1f}x")
print(f"Speedup vs NumPy:  {time_numpy / time_cython:.1f}x")

np.testing.assert_allclose(result_python, result_cython, rtol=1e-5)
print("Results match.")
```

**Checkpoint questions:**
- How does Cython's performance compare to Numba? Were you expecting one to be faster?
- Count the steps you had to take: writing the `.pyx` file, writing `setup.py`, running the compiler, importing the result. How does this workflow compare to adding `@jit`?
- If you needed to change the formula, what would you have to do in each approach?

---

### Exercise 5: Summary Plot (10 minutes)

Visualize everything you measured:

```python
labels  = ['Pure Python', 'NumPy', 'Numba', 'Cython']
times   = [time_python, time_numpy, time_numba, time_cython]
speedup = [time_python / t for t in times]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

ax1.bar(labels, times, color=['#d62728','#1f77b4','#2ca02c','#ff7f0e'])
ax1.set_ylabel("Median runtime (seconds)")
ax1.set_title("Absolute Runtime")

ax2.bar(labels, speedup, color=['#d62728','#1f77b4','#2ca02c','#ff7f0e'])
ax2.set_ylabel("Speedup vs pure Python (×)")
ax2.set_title("Speedup Factor")
ax2.axhline(1, color='gray', linestyle='--')

plt.tight_layout()
plt.savefig("speedup_comparison.png", dpi=150)
plt.show()
```

---

### Reflection Questions (15 minutes)

Write a short answer (3–5 sentences) to each of these in your notebook as a markdown cell.

**1. The real cost of optimization**
You spent different amounts of time on each approach. If your pure Python baseline took 30 seconds to run and you only needed to run it twice, was any optimization worth it? At what point — in terms of how often you run the code and how long it takes — does it make sense to invest time in Numba or Cython?

**2. Correctness vs speed**
Every exercise included an `assert_allclose` check. Why is this important? Have you ever changed code to make it faster and introduced a subtle bug? What's the risk of doing this in a research context?

**3. Portability and collaboration**
Imagine sharing your code with a collaborator who has never heard of Numba or Cython. Which approach is easiest to share and have them run immediately? Which requires the most setup? How does this affect your choice in a research group setting?

**4. Knowing when to stop**
NumPy was likely fast enough for this grid size. Given that Numba required minimal extra effort, can you articulate a personal rule of thumb for when you would stop at NumPy, when you would add Numba, and when you would go all the way to Cython?

**5. The 80/20 rule**
In your own current research code, where do you think most of the runtime is spent? Do you know? (If not — that's the answer. Look up Python's `cProfile` module.) Does it change how you think about where to invest optimization effort?

---

### Expected Results (Rough Benchmarks)

Results vary by machine, but you should see approximately:

| Method | Typical Speedup |
|---|---|
| Pure Python | 1× (baseline) |
| NumPy | 50–200× |
| Numba | 100–400× |
| Cython | 100–400× |

If Numba and Cython aren't significantly faster than NumPy for this problem, that's actually an interesting result worth reflecting on — it suggests NumPy's vectorization was already near-optimal for this particular computation.
