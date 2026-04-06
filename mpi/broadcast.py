from mpi4py import MPI

# Define world
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

# Only Rank 0 defines the data, all other ranks idling
if rank == 0:
    data = {'key1' : [7, 2.72, 2+3j], 'key2' : ( 'abc', 'xyz')}
else:
    data = None

# Broadcast the data from RANK_0 to all workers
data = comm.bcast(data, root=0)

# All tasks append the RANK ID to the data
data['key1'].append(rank)

# Rank 1 does something special to its data
if rank == 1:
    data['key1'] = None

# Print the resulting data
print(f"Rank: {rank}, data: {data}")


