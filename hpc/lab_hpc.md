# Lab 8: High Performance Computing (on Chinook)

## Motivation:
- Give you a general understanding of Chinook's available compute systems, 
  including partitions, priority, reservations, hardware
- Familiarize you with interfacing with Chinook through SSH
- Let you practice with common SLURM calls for understanding the job system
- Familiarize you with the `module` system which contains pre-compiled software
  stacks
- Expose you to an example SBATCH script for running jobs on Chinook
- Show you how to access interactive mode for accessing a compute node
- Run a toy problem on Chinook using 1 compute node 
- Understand the outputs from a batch job

## Student Learning Outcomes
By the end of this lab you should know:
- How to navigate the terminal interface of Chinook
- How to check queue, storage, and resources on Chinook
- How to run a simple job and request specific resources
- How to check the status of the job and cancel it
- How to understand job submission returns

## Instructions

- Please complete tasks and reflections, and submit reflections in Canvas submission box. Short answers for questions is okay.
- Each Task is worth 1 point of the total lab. Each question will have equal weight to distribute that 1 point
- Upload the script you create in `Task 2` to your class repository GitHub 
- In `Task 2`, half of the point in this task will be for a correctly formatted SBATCH script, and the other half point will be for answered questions.
- Becuase there are limited debug nodes on Chinook, there is a good chance the class will compete with each other for resources in many of the lab tasks. If you find the debug queue full, move onto other steps and check the queue regularly until you get access. These steps are short so students should be able to finish them relatively quickly, freeing up resources for others.


## References
- [Class lecture](https://docs.google.com/presentation/d/1FdpiCo89N5pSayILo-aX3JQs2hbjQ0Kzlgb3KCgUKsA/edit?usp=sharing) (see references link on last slide, too)
- [UAF RCS Chinook Documentation](https://uaf-rcs.gitbook.io/uaf-rcs-hpc-docs/hpc)
- Linux manual pages:  `man <program>` 
- Help messages: `<program> -h`

## Task 1: Common Commands Chinook & SLURM [1 pt]
Here you will get familiar with the directory structure and common SLURM commands for navigating and using Chinook and the SLURM job scheduling system. Remember this is just a Linux system with a few extra bells and whistles, so your experience navigating your laptop translates.


1. SSH onto login node `Chinook03` or `Chinook04` **and** change directory: `cd /`. Use `ls -l /import/*` to list out all of the filesystems attached to Chinook. Referencing the [Chinook documentation on filesystems](https://uaf-rcs.gitbook.io/uaf-rcs-hpc-docs/available-filesystems/available-filesystems), answer the following:
> - 1A: Based on the directories here, what are the names of the available file systems, and what types of file systems are they? (Lustre, archive, normal)
2. Change directory to `/import/c1/GEOS694/$USER`
> - 1B: What filesystem are you on here in the class project directory (Lustre, archive, normal)? Is this the same as your home directory (`cd ~`)?
3. Run the command: `show_storage`
> - 1C: What does this command do?  
> - 1D: What is the maximum allowed storage in the GEOS694 `/scratch` and `/archive` directories?
> - 1E: What do you think is the difference between `Soft_GiB` and `Hard_GiB`?  
4. Go to the [RCS Chinook documentation](https://uaf-rcs.gitbook.io/uaf-rcs-hpc-docs/hpc) and go to the page on `Available Partitions`
> - 1F: Describe different scenarios for why you would use the following partitions: debug, t1small, t1standard, bio (don't just copy-paste what the 'Purpose' is, describe an actual research task that might require each of these partitions)
5. Run the command: `squeue`
> - 1G: What does this command do?  
> - 1H: Name and briefly describe each of the columns shown in the `squeue` output. Use values from one of rows in the queue to make your explanation more specific.
6. Run the command: `qmap`
> - 1I: Below the job queue, there are 4 separate blocks separated by different partition names. For the block labelled: t1small, t2small, t1standard t2standard, describe what you are viewing.   
> - 1J: How many nodes could you could occupy right now on the partitions: t1small, t2small, t1standard, t2standard.  
> - 1K: How many 'debug; nodes are available to you?
7. Run the command: `sinfo`
> - 1L: What does this command do?
> - 1M: How many total nodes are available on partition `t1standard` that are not down or drained? (Node State Codes are [listed here](https://slurm.schedmd.com/sinfo.html#SECTION_NODE-STATE-CODES))
8. Run command: `module avail`
> - 1N: Describe what the output of this command tells you  
9. Run command: `module spider python`
> - 1O: Looking through the output, what versions of Python are available by default on Chinook through `modules`?
9. Run command: `module purge` 
- This will unload all modules (you can check this worked by running `module list` and confirming that it says 'No modules loaded')
- Load the lowest version number Python with `module load <PYTHON/VERSION>`. You will likely run into some intermediate issues, make sure to follow the provided tips. Confirm you correctly loaded this version of Python by typing `python`
> - 1P: What (if any) intermediate modules did you need to load?
> - 1Q: What is the compile date of this version of Python? (this is given when you call `python`)
10. Start up an interactive job on the debug node: `srun -p debug --nodes=1 --exclusive --pty /bin/bash`
> - 1R: Are all filesystems available to you on the compute node? Remember that we checked mounted filesystems in an earlier question, the same approach may give you different results now that you're on the compute node.
11. Run command `squeue`
> - 1S: How many nodes were you allocated for this interactive job? What are their node numbers?
11. Run the command: `scontrol show nodes <node_number>` for the node number(s) you found in the last question. Note that this won't actually work because of a command we ran earlier! Figure out how to re-load Slurm to get access to command `scontrol`.
> - 1T: How many cores and how much memory are available on this node?
12. Using the `JOBID` of your interactive job, run: `sacct -j <JOBID>`
> - 1U: What does this command do?
> - 1V: Describe what each of the rows in the `sacct` output represents. 
13. Run the command: `scancel <JOBID>`
> - 1W: What happened when you ran `scancel`?
> - 1X: Rerun `sacct -j <JOBID>` and explain why there are different 'States' of your job.


## Task 2: Submitting your Own Job [1 pt]

### References
1. [SLURM Sbatch Manual](https://slurm.schedmd.com/sbatch.html)
2. [RCS: Sbatch Documentation](https://uaf-rcs.gitbook.io/uaf-rcs-hpc-docs/using-batch/batch-scripts)
3. [Common SLURM environment variables](https://docs.hpc.shef.ac.uk/en/latest/referenceinfo/scheduler/SLURM/SLURM-environment-variables.html#gsc.tab=0)
4. [The srun command](https://hpc.nmsu.edu/onboarding/supercomputing/slurm/slurm-commands/#_the_srun_command)

---

### Task
1. Still logged into Chinook, using a text editor, create a new file called `my_batch_script.sh`. 
2. Using references/Google/Stack Overflow, etc., figure out how to structure your batch script so that it enforces the following `SBATCH Directives` and runs the following `Commands.
3. Run your job using the command `sbatch my_batch_script.sh`
4. Check that your job is running using `squeue`
5. Allow your job to finish
6. Check the output file, which should be named how you specified in the same directory
7. Answer the following `Questions` in your Canvas submission box
8. Upload `my_batch_script.sh` to your class repository GitHub

#### SBATCH Directives
In the header of `my_batch_script.sh` enforce the following directives
- Submit to the `debug` partition
- Specifies that 2 task will be run
- Requests 2 nodes
- Has a job name: "hello world!"
- Creates an output file that has the following name format: `<JOB_ID>_<JOB_NAME>.out`
- Has a maximum walltime of 5 seconds

#### Commands
In the body of `my_batch_script.sh`, have the script run the following **in order**: 

> Note: Run all of these commands using `srun`, see reference 4 above for an example or ask me if this is confusing.
 
1. Prints "Hello"
2. Print the SLURM environment variable that lists the nodes that this script is run on
3. Print the SLURM environment variable that lists the cpus for each node that this script is run on
3. Sleeps for 10 seconds
4. Prints "World!" 

### Questions
- 2A: What nodes did your job run on? (give node numbers)
- 2B: How many CPUs does each node have?
- 2C: Did your job time out based on the walltime?
- 2D: Copy-paste the output of `sacct -j <JOB_ID>`, and explain why you have the number of job steps you do, and what each job step refers to.

