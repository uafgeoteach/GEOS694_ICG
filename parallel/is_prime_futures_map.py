"""
Check if a number is prime or not, in parallel
the `map` function preserves the order in which tasks are submitted
"""
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed


def is_prime(n):
    for divisor in range(2, n):
        if n % divisor == 0:
            return False
    else:
        return True


def get_prime(bounds):
    i, j = bounds
    prime_numbers = []
    for n in range(i, j, 1):
        if is_prime(n):
            prime_numbers.append(n)
    return prime_numbers


def main(N):
    nproc = os.cpu_count()  # num. cores on PC
    step = N // nproc  # break up problem into even parts

    # Map requires a list of iteratbles, like a large list of data, here we 
    # provide a list of tuples (i, j)
    iterables = [(i, i + step) for i in range(1, N, step)]
   
    # Execute `nproc` processes in parallel. 
    with ProcessPoolExecutor(max_workers=nproc) as executor:
        results = executor.map(get_prime, iterables)
 
    # As each task completes, append to our list of primes
    primes = []
    for result in results:
        primes += result

    print(f"{len(primes)}/{N} Prime Numbers found")


if __name__ == "__main__":
    start = time.time()
    main(int(sys.argv[1]))
    elapsed = time.time() - start

    print(f"Total Elapsed: {elapsed:.2f}s")




