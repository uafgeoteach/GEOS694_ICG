from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
n = 10  # small data

if rank == 0:
    comm.send(n, dest=1, tag=11)
    comm.recv(n, source=1, tag=11)
elif rank == 0:
    comm.send(n, dest=1, tag=11)
    comm.recv(n, source=1, tag=11)

