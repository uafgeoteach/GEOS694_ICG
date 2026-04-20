## Lab: Making Python Fast 


### Overview

You will take a common geoscience time series computation and progressively speed it up using NumPy vectorization, Numba JIT (Just in Time), and Cython (pre-compiling). The computation — a **running climatological anomaly with a centered moving window** — is the kind of calculation that appears constantly in geoscience research and is deliberately chosen because it *cannot* be trivially vectorized, making it a realistic case for JIT and Cython.

> *Disclaimer: This lab assingment was written by Claude prompting for a Python-based lab exercise to explore the different ways of compiling Python for code speed, applied to a geoscience problem. It was  modified extensively by me to fit the course*

---

### Instructions

1. Follow along with the instructions below
2. For each implementation, please create a new Python script. There will be similarities amongst all the scripts so you can copy-paste. 
3. Example code blocks will be given but you will have to paste them together to get a cohesive script.
3. Do not upload your Python scripts at the end, they will all look the same.
4. Please answer the reflection questions and upload your answers to Canvas

---


### Setup 


Each of your Python scripts will use the following timer function to get an estimate of compute time.

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

Install `numba` and `Cython` into your GEOS694 Conda environment

```bash
conda install numba Cython
```
---

### The Problem: STA/LTA

The STA/LTA (short term average to long term average) ratio compares the average signal energy in a short window to the average energy in a long window, and is used to identify impulsive arrivals from background noise, e.g., in earthquake detection.

```
At every sample i:

STA[i] = mean(x[i - nsta: i]²)     # short-term average of squared amplitude
LTA[i] = mean(x[i - nlta: i]²)     # long-term average of squared amplitude

ratio[i] = STA[i] / LTA[i]
```

If the ratio exceeds a certain threshold, then an event is said to be detected.


### Seismic Data

Each script will use the following code block to get example data and upsample it so that the calculations take slightly longer. 

Use the `plot` variable to look at the data before you continue so you know what you are working with

```python
from obspy import read

def get_example_data(plot=False):
    """Returns 1Hz highpassed vertical (Z) component seismometer data"""
    st = read()
    st.filter("highpass", freq=1)
    st = st.select(component="Z")
    st.resample(250)  # upsample from 100 Hz
    if plot:
        st.plot()
    return st[0]  

# Define input variablers used by the STA/LTA functions
tr = get_example_data()
x = tr.data
nsta = int(tr.stats.sampling_rate * 0.5)
nlta = int(tr.stats.sampling_rate * 10)
```

---

### Exercise 1: STA/LTA in Pure Python 

Below you will implement the STA/LTA algorithm with a pure Python approach, by 
looping through the data. 

```python
def stalta_python(x, nsta, nlta):
    n = len(x)
    ratio = []

    for i in range(nlta, n):
        # STA: mean squared amplitude over short window
        sta = 0.0
        for j in range(i - nsta, i):
            sta += x[j] * x[j]
        sta /= nsta

        # LTA: mean squared amplitude over long window
        lta = 0.0
        for j in range(i - nlta, i):
            lta += x[j] * x[j]
        lta /= nlta

        if lta > 0:
            ratio.append(sta / lta)
        else:
            ratio.append(0)

    return np.array(ratio)

time_python, result_python = benchmark(
    stalta_python, x, nsta, nlta
)

print(f"Pure Python: {time_python:.3f} seconds")
```

- Plot the results and make sure the output STA/LTA makes sense to you
- Write down the time so you can compare it to later methods

#### Reflection Questions

- The inner loop computes STA and LTA completely from scratch at every sample. Count the floating point operations per sample. How does this scale with window size?

---

### Exercise 2: NumPy Vectorization (20 minutes)

NumPy provides sliding window tools that are used for quickly calculating sums
over arrays. Below is the STA/LTA code rewritten taking advantage of NumPy. Run and reflect.

```python
def stalta_numpy(x, nsta, nlta):
    """Calculate STA/LTA with NumPy calls only"""
    n  = len(x)
    x2 = x ** 2                    # squared amplitude
    cs = np.cumsum(x2)             # cumulative sum of squared amplitude

    # Prepend a zero so that cs[i] - cs[i-w] gives the sum over w samples
    cs = np.concatenate([[0], cs])

    ratio = np.zeros(n)

    # Valid range: need at least nlta samples behind us
    i = np.arange(nlta, n)

    sta = (cs[i] - cs[i - nsta]) / nsta
    lta = (cs[i] - cs[i - nlta]) / nlta

    valid = lta > 0
    ratio[i[valid]] = sta[valid] / lta[valid]

    return ratio

time_numpy, result_numpy = benchmark(stalta_numpy, x, nsta, nlta)
print(f"NumPy:   {time_numpy:.3E} seconds")
```

- Plot the results from the NumPy approach and make sure they match with the pure python.

**Reflection questions:**
- Approximately what speed up did you get with the NumPy approach, is this suprising to you?
- There is a difference in approach when using NumPy regarding memory allocation. Can you describe how the different functions approach this and speculate on why the NumPy approach is more optimal?

---

### Exercise 3: Numba JIT (20 minutes)

Now we implement Numba, a Just in Time compiler that attempts to analyze and 
speed up compute loops that take up most of the time in a program.

```python
from numba import jit

@jit(nopython=True)
def stalta_numba(x, nsta, nlta):
    n = len(x)
    ratio = []

    for i in range(nlta, n):
        # STA: mean squared amplitude over short window
        sta = 0.0
        for j in range(i - nsta, i):
            sta += x[j] * x[j]
        sta /= nsta

        # LTA: mean squared amplitude over long window
        lta = 0.0
        for j in range(i - nlta, i):
            lta += x[j] * x[j]
        lta /= nlta

        if lta > 0:
            ratio.append(sta / lta)
        else:
            ratio.append(0)

    return np.array(ratio)

# Warmup call — triggers compilation
start = time.perf_counter()
_ = stalta_numba(x, nsta, nlta)
compile_time = time.perf_counter() - start
print(f"Numba first call (includes compilation): {compile_time:.3f} seconds")

time_numba, result_numba = benchmark(stalta_numba, x, nsta, nlta)
print(f"Numba (after warmup): {time_numba:.3f} seconds")

```

- Plot the results of all three implementations to make sure they match


**Reflection questions:**
- Compare the Numba implementation to the pure Python one line by line. What changed?
- The Numba loop is still O(n × nlta) — the same algorithmic complexity as pure Python. Yet it is much faster. Where does the speedup come from if not from a better algorithm?
- How does the compilation time compare to the runtime for this problem? Would there be a time series length at which this would become an issue?

---
### Exercise 4: Cython

Cython is a static compiler for writing Python code that achieves C-like perfomance by adding static type declarations. You will see below that using Cython require additional development steps, trading human/development time for faster compute time. Cython does this by building a Python module (library) out of your Cython code, which can then be called through the standard Python intepreter.


1) Create the following `stalta_cy.pyx`

```python
import numpy as np
cimport numpy as np

def stalta_cython(np.ndarray[double, ndim=1] x, int nsta, int nlta):
    cdef int n = len(x)
    cdef int i, j
    cdef double sta, lta
    cdef np.ndarray[double, ndim=1] ratio = np.zeros(n)
    cdef np.ndarray[double, ndim=1] x2    = x ** 2

    # Initialize at position nlta
    cdef double sta_sum = 0.0
    cdef double lta_sum = 0.0

    for j in range(nlta - nsta, nlta):
        sta_sum += x2[j]
    for j in range(0, nlta):
        lta_sum += x2[j]

    for i in range(nlta, n):
        sta_sum += x2[i]     - x2[i - nsta]
        lta_sum += x2[i]     - x2[i - nlta]

        if lta_sum > 0:
            ratio[i] = (sta_sum / nsta) / (lta_sum / nlta)

    return ratio
```

2) Create `setup.py`

```python
from setuptools import setup
from Cython.Build import cythonize
import numpy as np

setup(
    ext_modules=cythonize("stalta_cy.pyx"),
    include_dirs=[np.get_include()]
)
```

3) Compile your code

```bash
python setup.py build_ext --inplace
```

4) Create a new Python script that contains your example data and benchmarking function, but now calls your Cython code as a module import:

```python
from stalta_cy import stalta_cython

time_cython, result_cython = benchmark(stalta_cython, x,  nsta, nlta)

print(f"Cython: {time_cython:.3f} seconds")
print(f"Speedup vs Python:           {time_python     / time_cython:.1f}x")
print(f"Speedup vs NumPy:            {time_numpy      / time_cython:.1f}x")
print(f"Speedup vs Numba:      {time_numba      / time_cython:.1f}x")

np.testing.assert_allclose(result_python, result_cython, rtol=1e-5)
print("Results match.")
```

**Reflection Questions**
- How does Cython compare to the other implementations in terms of speed?
- The Cython version required you to declare types for every variable (cdef double, cdef int). What happens to the mental overhead of writing code when you have to think about types explicitly?
- Cython produces a compiled .so file that you import like a normal module. How does this change how you would distribute your code compared to the other implementations? 

