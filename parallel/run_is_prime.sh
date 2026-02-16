#!/bin/bash

time \
	(python is_prime.py 1 25000 & \
	 python is_prime.py 25001 50000 & \
	 python is_prime.py 50001 75000 & \
	 python is_prime.py 75001 100000)


