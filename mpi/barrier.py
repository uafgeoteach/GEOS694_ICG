from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

i = 0
while i < rank:
    comm.barrier()
    i += 1

print(f"Hello World! {rank}")

while i < size:
    comm.barrier()
    i += 1
