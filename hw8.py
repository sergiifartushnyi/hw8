import multiprocessing
import time

def collatz_check(n):
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
    return True

def worker(start, end, queue):
    for n in range(start, end):
        if not collatz_check(n):
            queue.put(n)
            return
    queue.put(None)

def main():
    N = 10000000
    num_workers = multiprocessing.cpu_count()
    step = N // num_workers

    queue = multiprocessing.Queue()
    processes = []

    for i in range(num_workers):
        start = i * step + 1
        end = (i + 1) * step if i < num_workers - 1 else N + 1
        p = multiprocessing.Process(target=worker, args=(start, end, queue))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    while not queue.empty():
        result = queue.get()
        if result is not None:
            print(f"Гіпотеза Коллатца не підтверджена для числа {result}")
            return

    print("Гіпотеза Коллатца підтверджена для всіх чисел у заданому діапазоні.")

if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"Час виконання: {time.time() - start_time:.2f} секунд")
