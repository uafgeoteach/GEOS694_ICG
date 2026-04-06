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

# Initialize empty arrays to receive the partial data
partial = np.empty(int(num_data/size), dtype='d')

# Send data to the other workers
comm.Scatter(data, partial, root=0)

# Prepare the reduced array to receive the processed data from each rank
reduced = None
if rank == 0:
    reduced = np.empty(size, dtype='d')

# Average the partial arrays, and then gather them to RANK_0
comm.Gather(np.average(partial), reduced, root=0)

if rank == 0:
    print('Full Average:', np.average(reduced))


