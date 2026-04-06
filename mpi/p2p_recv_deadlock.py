from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
n = 10  # small data

if rank == 0:
    comm.recv(n, source=1, tag=10)
    comm.send(n, dest=1, tag=11)
elif rank == 1:
    comm.recv(n, source=0, tag=11)
    comm.send(n, dest=0, tag=10)



