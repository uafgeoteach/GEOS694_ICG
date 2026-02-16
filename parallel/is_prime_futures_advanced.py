"""Check if a number is prime or not, in parallel"""
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


def get_prime(i, j):
    prime_numbers = []
    for n in range(i, j, 1):
        if is_prime(n):
            prime_numbers.append(n)
    return prime_numbers


def main(N):
    nproc = os.cpu_count()  # num. cores on PC
    step = N // nproc  # break up problem into even parts
   
    # Execute `nproc` processes in parallel
    with ProcessPoolExecutor(max_workers=nproc) as executor:
        futures = [executor.submit(get_prime, i, i + step) 
                   for i in range(1, N, step)]
  
    # As each task completes, append to our list of primes
    primes = []
    for future in as_completed(futures):
        primes += future.result()

    print(f"{len(primes)}/{N} Prime Numbers found")


if __name__ == "__main__":
    start = time.time()
    main(int(sys.argv[1]))
    elapsed = time.time() - start

    print(f"Total Elapsed: {elapsed:.2f}s")




