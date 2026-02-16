import time
import subprocess

start = time.time()

step = 25000
for i in range(1, 100001, step):
    subprocess.Popen(f"python is_prime.py {i} {i+step}", 
                     shell=True)

elapsed = time.time() - start
print(f"Total Elapsed {time.time() - start:.2f}s")


