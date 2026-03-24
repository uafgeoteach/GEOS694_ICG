# Homework 8: HPC On Your Own

## Motivation:
- Take the knowledge you learned in lab and apply it to your own codes
- Get experience running your own jobs directly on Chinook
- Reinforce usage of SLURM commands tools for checking the queue and resources

## Tasks

The homework will have you get set up on Chinook so that you can run your own Python scripts, we will build on this later. 

## Instructions
- Complete the tasks below
- Answer text reflections in the Canvas text box
- Complete `ACTION` at the end

### Setup

1. Install `Mamba` to your `/home` directory 
> Note: *RCS recommends using `Mamba` over `Conda` for package management as it is lightweight and fast (ttps://uaf-rcs.gitbook.io/uaf-rcs-hpc-docs/third-party-software/miniconda).*
2. Create a class Conda environment (`GEOS694`) in your `/home` directory and install: `obspy`, `ipython`, `ipdb`
3. Clone the class GitHub repository to your `/home` directory (or a directory of your choice)
4. Clone your forked class repository to your `/home` directory (or a directory of your choice)
> **QUESTION 1**: Why do we install all of these files into the `/home` directory? And not `/CENTER1` or `/archive`

### Toy Problem
5. Write an SBATCH script to run the Python script `GEOS694/hpc/is_prime.py` from the class repository on the `debug` node
    - The argument of `is_prime.py` is the number of cores to use
    - In your SBATCH script, use environment variables to set the optimal number of cores when calling `is_prime.py`
    - Do not modify `is_prime.py` directly
6. Modify your SBATCH script:
    - Add the directive:  `$SBATCH --array=0-1`
    - Modify the output directive to `$SBATCH --output=%j_%a.out`
    - Run your script again

- **QUESTION 2:** What does the array function do?
- **QUESTION 3:** How could you use the `array` directive to do multi-node multi-processor calculations? Discuss if and how you modify `is_prime.py`, your SBATCH script, or both.

### Run your own script
7. Pick a research script that you have and write an sbatch script to run it on the `debug` node
    - **REFLECTION 4**: Does your script take advantage of all the cores on the node?
    - **REFLECTION 5**: How could you modify your script to run faster on Chinook (CPU or GPU cluster)? Be somewhat specific (i.e., "I could parallelize the calculation in the for loop of lines X-Y", or "I could replace the NumPy operations in Lines X-Y with CuPy")

**ACTION**: Upload the SBATCH script from 7 to your personal GitHub from Chinook. You should already have SSH keys setup so this should be straightforward. 







