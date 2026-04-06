from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

data = f"hello from rank {rank}"
if rank == 0:
    dest = 1
elif rank == 1:
    dest = 0

recv_data = comm.sendrecv(data, dest=dest)

print(f"Rank {rank} received message: '{recv_data}'")



