import os
from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
PID = os.getpid()

print(f"hello world from rank {rank}/{size}, process ID: {PID}")




