# MPI Lab
GEOS694 Intro Computational Geoscience


## Tasks
### Install
1. Activate your GEOS694 Conda environment
2. Install mpi4py using conda: `conda install mpi4py`
3. Ensure MPI works by running: `mpiexec`
4. For each of the Toy Problem prompts below, create a separate Python program that uses `mpi4py` to accomplish the given task.
5. Unless explcitely told, assume that each task should run with 4 processes. That means you can hard code ranks to make things easier.


### Point-to-Point Toy Problems
Use `send` and `recv` to create the following programs. Make sure every `send` matches a corresponding `recv`. Be careful about avoiding deadlocks.

1. **Circular Shift Program:** Write a Python MPI program where every process sends its rank to its right neighbor. The process with the largest rank should send its rank to process 0
2. **Ring Program**: Pass a value around all processes in a ring-like fashion. The passing sequence is `0 -> 1 -> ... -> N -> 0` where `N` is the maximum number of processes.

### Collective Communication Toy Problems

3. Use `bcast` (broadcast) to write a program that gives the following output. Do not use `send` or `recv`, lines 2-4 can print in any order
```
I am process 1 and I broadcast value 10
I am process 0 and I have value 0 after broadcast
I am process 2 and I have value 20 after broadcast
I am process 3 and I have value 30 after broadcast
```
4. Use `reduce` to write a program that prints the following:
```
Value held by MPI process 0: 0.
Value held by MPI process 1: 100.
Value held by MPI process 3: 300.
Value held by MPI process 4: 400.
Value held by MPI process 2: 200.
Total sum reduced at MPI process 0: 1000.
```
5. On Rank 0 create a 1x4 matrix of random numbers, `scatter` to all other ranks, multiply all values by their respective rank values, then use `reduce` to get the sum of all values.

### Matrix Vector Multiplication
Matrix operations are one of the most common tasks in computing and is easily parallelizable but requires communication between processes. Given the simple matrix-vector operation below:

$$ 
A\mathbf{b} = 
\begin{bmatrix}
    a_{11} & a_{12} & a_{13} & a_{14} \\
    a_{21} & a_{22} & a_{23} & a_{24} \\
    a_{31} & a_{32} & a_{33} & a_{34} \\
    a_{41} & a_{42} & a_{43} & a_{44} \\
\end{bmatrix}
\begin{bmatrix}
    b_{1} \\
    b_{2} \\
    b_{3} \\
    b_{4} \\
\end{bmatrix} 
= 
\begin{bmatrix}
    a_{11}b_{1} + a_{12}b_2 + a_{13}b_3 + a_{44}b_4 \\
    \dots \\
    \dots \\
    \dots \\
\end{bmatrix}
$$

Write an MPI program for 4 processes that uses whatever approach you want to solve the matrix vector operation in parallel following the structure below
- Rank 0 should estabish the matrix **A**  with random numbers (use `numpy` array)
- Rank 1 should establish the vector **b** with random numbers (use `numpy` array)
- Ranks 1 and 0 should communicate their information to all the other ranks
- Each rank should calculate it's respective matrix-vector operation
- Use a `barrier` to ensure that all calculations wait for each other to finish
- Rank 0 should collect the resulting matrix values and calculate the sum of all elements in the final matrix

