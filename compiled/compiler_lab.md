## Lab: Making Python Fast — Time Series Analysis Edition

**Duration:** 2 hours | **Level:** Graduate | **Prerequisites:** Basic Python and NumPy familiarity

---

### Overview

You will take a common geoscience time series computation and progressively speed it up using NumPy vectorization, Numba JIT, and Cython. The computation — a **running climatological anomaly with a centered moving window** — is the kind of calculation that appears constantly in geoscience research and is deliberately chosen because it *cannot* be trivially vectorized, making it a realistic case for JIT and Cython.

---

### Setup (10 minutes)

```bash
mkdir timeseries_speed_lab && cd timeseries_speed_lab
pip install numba cython numpy matplotlib jupyter scipy
jupyter notebook lab.ipynb
```

At the top of your notebook:

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

### The Problem: Rolling Z-Score Anomaly

Given a long daily temperature time series (think 100 years of station data, or a long climate model run), compute at every point `i` the **z-score anomaly** relative to a local window:

```
anomaly[i] = (x[i] - mean(x[i-w : i+w])) / std(x[i-w : i+w])
```

where `w` is the half-window size (e.g. 15 days on either side). This is a standard way to remove seasonal cycles and identify extreme events.

This is harder to vectorize than it looks because:
- Each output point requires a *different* slice of the input
- Edge handling (the start and end of the series) requires special treatment
- The window mean and std must be recomputed at every step

```python
# --- Paste this into your notebook ---

np.random.seed(42)
N = 500_000          # 500,000 time steps — roughly 1,370 years of daily data
                     # or one long climate model run
WINDOW = 15          # 15-day half-window (30-day centered window)

# Synthetic temperature signal: seasonal cycle + noise + slow trend
t = np.arange(N)
signal = (10 * np.sin(2 * np.pi * t / 365.25)   # seasonal cycle
          + 0.001 * t / 365.25                    # slow warming trend
          + np.random.normal(0, 1, N))            # daily noise

signal = signal.astype(np.float64)
```

---

### Exercise 1: Pure Python Baseline (20 minutes)

```python
def rolling_zscore_python(x, w):
    n = len(x)
    result = np.full(n, np.nan)
    for i in range(w, n - w):
        window = x[i - w: i + w + 1]
        mu  = sum(window) / len(window)
        var = sum((v - mu) ** 2 for v in window) / len(window)
        std = var ** 0.5
        if std > 0:
            result[i] = (x[i] - mu) / std
    return result

time_python, result_python = benchmark(rolling_zscore_python, signal, WINDOW)
print(f"Pure Python: {time_python:.3f} seconds")
```

Record your result. This is your **baseline**.

**Checkpoint questions before moving on:**
- How long did it take? If your dataset were 50 climate model ensemble members each with 500,000 time steps, how long would processing all of them take at this speed?
- Look at the inner loop. How many Python operations happen per time step? Try counting them — each `sum()`, comparison, and arithmetic operation is a separate CPython bytecode dispatch.

---

### Exercise 2: NumPy Vectorization (20 minutes)

NumPy provides `np.lib.stride_tricks` and sliding window tools, but rolling z-scores have a subtlety: you need the mean and std of a *different slice* for each point. The standard approach is `np.convolve` for the mean and a cumulative sum trick for the variance.

**Task:** Implement a vectorized version using NumPy. A clean approach uses `np.cumsum` to compute rolling sums in O(n) without a loop:

```python
def rolling_zscore_numpy(x, w):
    n = len(x)
    result = np.full(n, np.nan)
    
    # Use cumsum to compute rolling sums efficiently
    cs    = np.cumsum(x)
    cs_sq = np.cumsum(x ** 2)
    
    # For each point i, sum(x[i-w:i+w+1]) = cs[i+w] - cs[i-w-1]
    win_size = 2 * w + 1
    
    i_start = w
    i_end   = n - w
    
    left  = np.arange(i_start - w - 1, i_end - w - 1)
    right = np.arange(i_start + w,     i_end + w)
    
    sum_x   = cs[right]    - np.where(left >= 0, cs[left], 0)
    sum_x2  = cs_sq[right] - np.where(left >= 0, cs_sq[left], 0)
    
    mu  = sum_x / win_size
    var = sum_x2 / win_size - mu ** 2
    var = np.maximum(var, 0)           # guard against floating point negatives
    std = np.sqrt(var)
    
    valid = std > 0
    idxs  = np.arange(i_start, i_end)
    result[idxs[valid]] = (x[idxs[valid]] - mu[valid]) / std[valid]
    
    return result

time_numpy, result_numpy = benchmark(rolling_zscore_numpy, signal, WINDOW)
print(f"NumPy:   {time_numpy:.3f} seconds")
print(f"Speedup vs Python: {time_python / time_numpy:.1f}x")

# Verify — compare only non-nan values
mask = ~np.isnan(result_python) & ~np.isnan(result_numpy)
np.testing.assert_allclose(result_python[mask], result_numpy[mask], rtol=1e-5)
print("Results match.")
```

**Checkpoint questions:**
- How much faster is NumPy? Was it what you expected?
- The cumsum trick is not obvious — it took real mathematical insight to reformulate the loop this way. How long did it take you to understand it? Would you have arrived at it yourself under time pressure?
- This version allocates several large intermediate arrays (`cs`, `cs_sq`, `sum_x`, etc.). For very long time series or many ensemble members, could memory become a concern?

---

### Exercise 3: Numba JIT (20 minutes)

Now apply Numba to a clean loop version — no mathematical reformulation needed:

```python
from numba import jit

@jit(nopython=True)
def rolling_zscore_numba(x, w):
    n = len(x)
    result = np.full(n, np.nan)
    win_size = 2 * w + 1
    
    for i in range(w, n - w):
        mu = 0.0
        for j in range(i - w, i + w + 1):
            mu += x[j]
        mu /= win_size
        
        var = 0.0
        for j in range(i - w, i + w + 1):
            diff = x[j] - mu
            var += diff * diff
        var /= win_size
        
        if var > 0:
            result[i] = (x[i] - mu) / var ** 0.5
    
    return result

# Warmup — first call compiles
start = time.perf_counter()
_ = rolling_zscore_numba(signal, WINDOW)
compile_time = time.perf_counter() - start
print(f"Numba first call (includes compilation): {compile_time:.3f} seconds")

time_numba, result_numba = benchmark(rolling_zscore_numba, signal, WINDOW)
print(f"Numba (after warmup):  {time_numba:.3f} seconds")
print(f"Speedup vs Python: {time_python  / time_numba:.1f}x")
print(f"Speedup vs NumPy:  {time_numpy   / time_numba:.1f}x")

mask = ~np.isnan(result_python) & ~np.isnan(result_numba)
np.testing.assert_allclose(result_python[mask], result_numba[mask], rtol=1e-5)
print("Results match.")
```

**Checkpoint questions:**
- Compare the Numba loop to the pure Python loop. How different are they? What did you actually have to change?
- How does the compilation time compare to the runtime? If you were processing one short time series in a script that runs once, would Numba help?
- Numba's loop here is O(n × w) — it recomputes the window from scratch at every point. A smarter algorithm would update the running mean incrementally. Would it be worth implementing that? (For bonus work below.)

---

### Exercise 4: Cython (30 minutes)

**Step 1:** Create `rolling_zscore_cy.pyx`:

```python
# rolling_zscore_cy.pyx
import numpy as np
cimport numpy as np
from libc.math cimport sqrt

def rolling_zscore_cython(np.ndarray[double, ndim=1] x, int w):
    cdef int n = len(x)
    cdef int win_size = 2 * w + 1
    cdef int i, j
    cdef double mu, var, diff, std
    cdef np.ndarray[double, ndim=1] result = np.full(n, np.nan)

    for i in range(w, n - w):
        mu = 0.0
        for j in range(i - w, i + w + 1):
            mu += x[j]
        mu /= win_size

        var = 0.0
        for j in range(i - w, i + w + 1):
            diff = x[j] - mu
            var += diff * diff
        var /= win_size

        if var > 0:
            result[i] = (x[i] - mu) / sqrt(var)

    return result
```

**Step 2:** Create `setup.py`:

```python
# setup.py
from setuptools import setup
from Cython.Build import cythonize
import numpy as np

setup(
    ext_modules=cythonize("rolling_zscore_cy.pyx"),
    include_dirs=[np.get_include()]
)
```

**Step 3:** Compile:

```bash
python setup.py build_ext --inplace
```

**Step 4:** Back in your notebook:

```python
from rolling_zscore_cy import rolling_zscore_cython

time_cython, result_cython = benchmark(rolling_zscore_cython, signal, WINDOW)
print(f"Cython: {time_cython:.3f} seconds")
print(f"Speedup vs Python: {time_python / time_cython:.1f}x")
print(f"Speedup vs NumPy:  {time_numpy  / time_cython:.1f}x")

mask = ~np.isnan(result_python) & ~np.isnan(result_cython)
np.testing.assert_allclose(result_python[mask], result_cython[mask], rtol=1e-5)
print("Results match.")
```

**Checkpoint questions:**
- The Cython code looks almost identical to the Numba code — what are the actual differences in what you had to write?
- You had to leave the notebook, write a separate file, write a build script, and run a compiler. How does this friction feel compared to the `@jit` decorator?
- When might Cython's extra friction be worth it over Numba? (Hint: think about distributing your code as a package, or integrating with existing C libraries.)

---

### Bonus Exercise: Incremental Window Update (Optional, 15 minutes)

The current loop recomputes the entire window sum from scratch at every step — O(n × w) operations. But a rolling window has a simple incremental update: when you slide one step forward, you add one new value and drop one old value.

**Task:** Implement this optimization in Numba and measure whether it makes a meaningful difference:

```python
@jit(nopython=True)
def rolling_zscore_numba_fast(x, w):
    n = len(x)
    result = np.full(n, np.nan)
    win_size = 2 * w + 1

    # Initialize the first window
    win_sum   = np.sum(x[0 : win_size])
    win_sum_sq = np.sum(x[0 : win_size] ** 2)

    for i in range(w, n - w):
        # Update window incrementally rather than recomputing
        if i > w:
            win_sum    += x[i + w]     - x[i - w - 1]
            win_sum_sq += x[i + w]**2  - x[i - w - 1]**2

        mu  = win_sum / win_size
        var = win_sum_sq / win_size - mu ** 2
        if var > 0:
            result[i] = (x[i] - mu) / var ** 0.5

    return result

# Warmup
_ = rolling_zscore_numba_fast(signal, WINDOW)

time_fast, result_fast = benchmark(rolling_zscore_numba_fast, signal, WINDOW)
print(f"Numba incremental: {time_fast:.3f} seconds")
print(f"Speedup vs basic Numba: {time_numba / time_fast:.1f}x")
```

This bonus exercise illustrates an important point: **algorithmic improvement and compiler optimization are separate tools**, and often the algorithm matters more.

---

### Exercise 5: Summary Plot (10 minutes)

```python
labels  = ['Pure Python', 'NumPy', 'Numba', 'Cython']
times   = [time_python, time_numpy, time_numba, time_cython]
speedup = [time_python / t for t in times]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

colors = ['#d62728', '#1f77b4', '#2ca02c', '#ff7f0e']

ax1.bar(labels, times, color=colors)
ax1.set_ylabel("Median runtime (seconds)")
ax1.set_title("Absolute Runtime")

ax2.bar(labels, speedup, color=colors)
ax2.set_ylabel("Speedup vs pure Python (×)")
ax2.set_title("Speedup Factor")
ax2.axhline(1, color='gray', linestyle='--')

plt.tight_layout()
plt.savefig("timeseries_speedup.png", dpi=150)
plt.show()
```

---

### Reflection Questions (15 minutes)

**1. Human time vs. computer time**
Rank the four approaches by how long they took *you* to implement, from fastest to slowest. Now rank them by runtime performance. Is the fastest to implement also the fastest to run? What does this suggest about how you should approach optimization in your own research workflow?

**2. The vectorization ceiling**
The NumPy solution required reformulating the algorithm using cumulative sums — a non-obvious mathematical trick. In your own research, do you always have a clean mathematical reformulation available? What kinds of geoscience algorithms (think: iterative solvers, agent-based models, recursive filters) might resist vectorization entirely?

**3. Warmup and use patterns**
Numba has a compilation cost on the first call. Describe two scenarios from your own research: one where this warmup cost is irrelevant, and one where it would be a real problem. How would you handle the second case?

**4. The algorithmic vs. compiler tradeoff**
If you did the bonus exercise: did the incremental window update outperform the basic Numba version? What does this tell you about the relationship between choosing a better algorithm versus applying a faster compiler? Which would you invest time in first?

**5. Collaboration and reproducibility**
Imagine submitting your analysis code alongside a paper. Which implementation would be easiest for a reviewer or future researcher to read, verify, and modify? Does the answer change if the code needs to run on a computing cluster you don't control? How do you weigh performance against reproducibility in a research context?

---

### Expected Results

| Method | Typical Speedup |
|---|---|
| Pure Python | 1× (baseline) |
| NumPy | 20–80× |
| Numba | 200–800× |
| Cython | 200–800× |
| Numba incremental (bonus) | 2–5× over basic Numba |

Note that for this problem — unlike the heat index exercise — Numba and Cython are likely to **significantly outperform NumPy**, because the cumsum vectorization still allocates large intermediates and does redundant work that the compiled loop avoids entirely. This is the key teaching point: NumPy vectorization is not always the performance ceiling.