import sys
import threading
import math

# 多线程，只会占用大约14%的cpu

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

def prime_finder(start, filename):
    i = start
    while True:
        if is_prime(i):
            with open(filename, "a") as f:
                f.write(str(i) + "\n")
        i += 1

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: prime_finder start_value output_file")
        sys.exit(1)

    start = int(sys.argv[1])
    filename = sys.argv[2]

    # 计算线程数
    num_threads = threading.active_count()

    # 分配线程任务
    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=prime_finder, args=(start + i, filename))
        threads.append(t)
        t.start()

    # 等待所有线程完成
    for t in threads:
        t.join()
