"""
scatter-gather example using lowercase 's' and 'g' scatter and gather which work
on Python objects through pickling. Remember that this is slower than the 
capital 'S' and 'G' versions. Syntax is also different.
"""
from mpi4py import MPI
import numpy as np

# set up MPI world
comm = MPI.COMM_WORLD
size = comm.Get_size() 
rank = comm.Get_rank()

# Generate a large array of data on RANK_0
num_data = 100000000 
data = None
if rank == 0:
    data = np.random.normal(loc=10, scale=5, size=num_data)
    data = np.array_split(data, size)  # `scatter` assumes data length == `size`

# Send Python object to the other workers as pickle
partial = comm.scatter(data, root=0)
partial_average = np.average(partial)

# Average the partial arrays, and then gather them to RANK_0
reduced = comm.gather(partial_average, root=0)

if rank == 0:
    print('Full Average:', np.average(reduced))


