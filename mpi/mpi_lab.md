# MPI Lab
**GEOS694 Intro Computational Geoscience**

## Instructions
The following lab assignment will give you some toy problems to practice implementing MPI in Python using the library `mpi4py`. 

For each Toy Problem prompt below, create a separate Python program to accomplish the given task. Check out the `references` listed below for code snippet examples and reference information.

**When you are finished, upload all your scripts to your class repository under the directory `mpi_lab`.**

> *Note: Some of these Toy Problems were inspired by exercises found online and listed in the Lecture Slide references, some were prompted from ChatGPT starting with prompt "Can you provide simple python toy example problems to practice using Mpi4Py with emphasis on point-to-point and collective communication?".*

## References
1. The [MPI4PY tutorial page](https://mpi4py.readthedocs.io/en/4.0.3/tutorial.html) provides a good overview and code snippets.
2. [Class lecture slides](https://docs.google.com/presentation/d/1N1gnfif7GR1DzqyTJcz76fmQyizCBlWaXkxOSBy3SLU/edit?usp=sharing) have code examples and background information.
3. Example code blocks from the lecture are available on the [course GitHub page](https://github.com/uafgeoteach/GEOS694_ICG/tree/main/mpi).

## Setup
1. Activate your GEOS694 Conda environment
2. Install mpi4py using conda: `conda install mpi4py`
3. Ensure MPI works by running: `mpiexec -h`
    - You should see a help message appear

## Tasks

### 1. Point-to-Point: Ring Message Passing
Here you will use `send` and `recv` to pass a message around a ring of processes. Be careful to avoid deadlock situations.

#### Description
- Each process has a given rank `r`
- Rank 0 starts with a message `"hello world!"` and appends a random number between 1 and 10
- The message is passsed to the rank neighbor `r+1`. 
- Each process takes the value in the message, multiplies it by its own rank, and appends it to the message. 
- The last process ends the message with `"goodbye world!"`
- The last process sends the message back to Rank 0 who prints the message
- The expected outcome is a print message that looks like:
    ```
    hello world! n n*1 n*1*2 ... n*1*2*...*{N-1} goodbye world!
    ```
- Where `n` is the random number between 0 and 10, and `{N-1}` is the rank of the last process.


### 2. Parallel Sum with Scatter and Gather

Here you will use `scatter` and `gather` to distribute work and recombine results.

#### Description
- Process 0 creates an array of numbers 1-N
- Use `scatter` to divide this array amongst all processes
- Each Process `r` computes the **sum** of their array chunk
- Use `gather` to send array chunk sums back to Process 0
- Process 0 computes the final total sum
- Find a way to check that the calculated sum is correct, maybe Process 0 calculates the sum on its own, maybe you pre-compute the answer, up to you.
- Process 0 prints the sum, and confirmation of the check value
    ```
    The sum of 1-N is X == Y.
    ```
- Where X is the distributed sum value, and Y is the check value.
- Check that this works for values 10, 1000, 10000.


### 3. Global Max 
We will use `bcast` (broadcast) and `reduce` to find the global maximum value 

#### Description
- Each process generates a random number between 0 and 1000
- Use `reduce` to compute the global maximum at the root process
- Root process broadcasts its result back to all other processes
- Each process will then check its value against the global max and determine if it is less than or equal to the global max
- Each process prints its random value, and the max value, something like:
    ```
    Rank R has value X which is less than global max Y
    ```
    or
    ```
    Rank R has value X which is the global max Y
    ```

### 4. Matrix-Vector Multiplication

This is such a common operation in computing that GPU hardware is optimized to calculate matrix-matrix products. Here we will solve the problem:

$$\mathbf{y = A \cdot x} $$

Where for $N$ processes:
- $A$ is an $N\times N$ matrix
- $x$ is vector of size $N$
- $y$ is a resultant vector

Our goal is to parallelize the matrix-vector operation by splitting the problem up **row-rise** across different processes. Each process computes the partial result of the resulting vector and all results are gathered onto root.

#### Description
- The value of $N$ is defined by the number of processes involved.
- Root process generates the matrix $A$ and the vector $x$ with random numbers. 
    - Use NumPy arrays here
- Use `scatter` to distribute the **rows** of $A$ to all processes
- Use `bcast` (broadcast) to distribute the entire vector $x$ to all processes
- Each process should compute their piece of the vector: $y_n = A_n \cdot x $
- Use `barrier` to ensure that all processes have finished their calculation before proceeding
- Use `Igather` to do non-blocking collection of all pieces of $y$ on the root process
- Have Root print out the resulting matrix-vector operation and result. The output message should look something like this:
    ```
    A_11 ... A_1N  * x_1 = y_1
    ...  ... ...     ...   ...
    A_N1 ... A_NN    x_N   y_N
    ```
    >*Note: Don't focus too hard on the formatting, as long as the information is understandable.*
