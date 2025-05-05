import random
import time
import platform
import psutil
import matplotlib.pyplot as plt

def quicksort(arr, left, right):
    if left < right:
        pi = partition(arr, left, right)
        quicksort(arr, left, pi - 1)
        quicksort(arr, pi + 1, right)

def partition(arr, left, right):
    pivot = arr[right]
    i = left - 1
    for j in range(left, right):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[right] = arr[right], arr[i + 1]
    return i + 1

def quickselect(val, left, right, k):
    if left == right:
        return val[left]
    
    pos = random.randint(left, right)
    val[pos], val[right] = val[right], val[pos]
    pivot = val[right]

    i = left - 1

    for j in range(left, right):
        if val[j] < pivot:
            i += 1
            val[i], val[j] = val[j], val[i]

    val[i + 1], val[right] = val[right], val[i + 1]
    count = right - (i + 1) + 1

    if count == k:
        return pivot
    elif count < k:
        return quickselect(val, left, i, k - count)
    else:
        return quickselect(val, i + 2, right, k)

if __name__ == "__main__":
    print("CPU:", platform.processor())
    print("RAM:", round(psutil.virtual_memory().total / (1024**3), 2), "GB")

    sizes = [10_000 * (2 ** i) for i in range(5)]
    q_times = []
    s_times = []
    errors = []

    for n in sizes:
        val = [random.randint(0, n - 1) for _ in range(n)]

        # QuickSelect хугацаа
        runtime = 0
        for _ in range(1000):
            tmp = val[:]
            k = random.randint(1, n)
            start = time.time()
            quickselect(tmp, 0, n - 1, k)
            runtime += (time.time() - start) * 1000

        q_avg = runtime / 1000
        q_times.append(q_avg)

        # QuickSort хугацаа
        tmp = val[:]
        start = time.time()
        quicksort(tmp, 0, len(tmp) - 1)
        s_elapsed = (time.time() - start) * 1000
        s_times.append(s_elapsed)

        # AxB != C алдааны тест
        error_count = 0
        for _ in range(1000):
            A = random.randint(1, 10000)
            B = random.randint(1, 10000)
            correct = A * B
            if random.random() < 0.5:
                C = correct
            else:
                C = correct + random.randint(1, 100)
            if A * B != C and C == correct:
                error_count += 1
        error_rate = error_count / 1000
        errors.append(error_rate)

        print(f"Оролт = {n}: QuickSelect = {q_avg:.2f}ms, QuickSort = {s_elapsed:.2f}ms, AxB!=C алдаа: {error_rate:.2%}")

    plt.figure(figsize=(10, 6))
    plt.plot(sizes, q_times, label="QuickSelect", marker='o')
    plt.plot(sizes, s_times, label="QuickSort", marker='runtime', linestyle='--')
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Оролт (log scale)")
    plt.ylabel("Хугацаа (ms, log scale)")
    plt.title("QuickSelect, QuickSort харьцуулалт")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig("quickselect.png")

    plt.show()
