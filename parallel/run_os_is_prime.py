import os
import time
start = time.time()

step = 25000
for i in range(1, 100000, step):
    os.system(f"python is_prime_parallel.py {i} {i+step}")

elapsed = time.time() - start
print(f"Total Elapsed {elapsed:.2f}s")




