# MPI Lab
GEOS694 Intro Computational Geoscience


## Tasks
### Install
1. Activate your GEOS694 Conda environment
2. Install mpi4py using conda: `conda install mpi4py`
3. Ensure MPI works by running: `mpiexec`

### Point-to-Point Toy Problems
Use `send` and `recv` to create the following programs. Make sure every `send` matches a corresponding `recv`. Be careful about avoiding deadlocks.

1. **Circular Shift Program:** Write a Python MPI program where every process sends its rank to its right neighbor. The process with the largest rank should send its rank to process 0
2. **Ring Program**: Pass a value around all processes in a ring-like fashion. The passing sequence is `0 -> 1 -> ... -> N -> 0` where `N` is the maximum number of processes.




