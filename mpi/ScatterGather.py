"""
Example of Scatter/Gather using capital 'S' and 'G' versions, which work on 
single-segment buffer interface, i.e., all data needs to be continuous, i.e.,
NumPy arrays in Python. Here we need to establish buffer objects to fill in when
calling Scatter and Gather, rather than creating variables directly.
"""
from mpi4py import MPI
import numpy as np

# set up MPI world
comm = MPI.COMM_WORLD
size = comm.Get_size() 
rank = comm.Get_rank()

# Generate a large array of data on RANK_0
num_data = 100000000 

if rank == 0:
    data = np.random.normal(loc=10, scale=5, size=num_data)
else:
    data = None

# Initialize empty arrays to receive the partial data. 
# Each partial array is only 1/N'th the size of the full array.
partial = np.empty(int(num_data/size), dtype='d')

# Root sends chunks of data to the other workers' `partial`
comm.Scatter(data, partial, root=0)

# Calculate the partial average for each chunk
partial_average = np.average(partial)

# Prepare the reduced array to receive the processed data from each rank
if rank == 0:
    reduced = np.empty(size, dtype='d')
else:
    reduced = None

# Average the partial arrays, and then gather them to RANK_0
comm.Gather(partial_average, reduced, root=0)

# Take the final average of all partial array averages
if rank == 0:
    print('Full Average:', np.average(reduced))


