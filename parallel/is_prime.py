"""Check if a number is prime or not, in parallel"""
import sys
import time


def is_prime(n):
    for divisor in range(2, n):
        if n % divisor == 0:
            return False
    else:
        return True

def main(i, j):
    prime_numbers = []
    for n in range(i, j, 1):
        if is_prime(n):
            prime_numbers.append(n)

    print(f"{len(prime_numbers)}/{j-i} Prime Numbers found")


if __name__ == "__main__":
    start = time.time()
    main(int(sys.argv[1]), int(sys.argv[2]))
    elapsed = time.time() - start

    print(f"Elapsed: {elapsed:.2f}s")




