import os
import sys
import time
import math
from multiprocessing import Process, Queue

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def prime_finder(start, end, filename, q):
    while True:
        for i in range(start, end):
            if is_prime(i):
                with open(filename, "a") as f:
                    f.write(str(i) + "\n")
        q.put(end)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: prime_finder start_value output_file")
        sys.exit(1)

    start = int(sys.argv[1])
    filename = sys.argv[2]

    num_processes = os.cpu_count()
    chunk_size = 10000
    q = Queue()
    processes = []

    while True:
        end = start + chunk_size
        for i in range(num_processes):
            p = Process(target=prime_finder, args=(start, end, filename, q))
            processes.append(p)
            p.start()
            start = end
        for p in processes:
            p.join()
        processes = []
        time.sleep(60)
