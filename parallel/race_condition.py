"""
Forcing a race condition
https://medium.com/yavar/understanding-race-conditions-in-python-and-how-to-handle-them-98f998708b2c
"""
import threading

counter = 0  # Shared resource

def increment():
    global counter
    for _ in range(1000000):
        counter += 1

threads = []
for _ in range(10):  # Create 5 threads
    t = threading.Thread(target=increment)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"Final counter value: {counter}")
