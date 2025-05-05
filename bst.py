import random
import time
import platform
import psutil
import math
import matplotlib.pyplot as plt

random.seed()

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

def get_size(t):
    if not t:
        return 0
    return 1 + get_size(t.left) + get_size(t.right)

def partition(t, key):
    if not t:
        return (None, None)
    if key < t.key:
        left, right = partition(t.left, key)
        t.left = right
        return (left, t)
    else:
        left, right = partition(t.right, key)
        t.right = left
        return (t, right)

def insert(t, key):
    if not t:
        return Node(key)
    if random.randint(0, get_size(t)) == 0:
        new_node = Node(key)
        left, right = partition(t, key)
        new_node.left = left
        new_node.right = right
        return new_node
    if key < t.key:
        t.left = insert(t.left, key)
    else:
        t.right = insert(t.right, key)
    return t

def merge(a, b):
    if not a or not b:
        return a if a else b
    if random.randint(0, get_size(a) + get_size(b) - 1) < get_size(a):
        a.right = merge(a.right, b)
        return a
    else:
        b.left = merge(a, b.left)
        return b

def search(t, key):
    count = 0
    while t:
        count += 1
        if key == t.key:
            break
        elif key < t.key:
            t = t.left
        else:
            t = t.right
    return count

print("CPU:", platform.processor())
print("RAM:", round(psutil.virtual_memory().total / (1024**3), 2), "GB")

num = [500, 1000, 2000, 4000, 8000]
runtime = []

for n in num:
    start = time.time()

    v = set()
    while len(v) < n:
        v.add(random.randint(0, n * 10))
    val = list(v)
    root = None
    for el in val:
        root = insert(root, el)

    steps = 0
    for i in range(1_000_000):
        if i % 2 == 0:
            q = random.choice(val)
        else:
            q = random.randint(n * 10 + 1, n * 20)
        steps += search(root, q)

    runTime = time.time() - start
    runtime.append(runTime)

    avgStep = steps / 1_000_000
    logTime = math.log10(runTime + 1e-9)

    error = 0
    for _ in range(1000):
        A = random.randint(1, 10000)
        B = random.randint(1, 10000)
        correct_C = A * B
        if random.random() < 0.5:
            C = correct_C
        else:
            C = correct_C + random.randint(1, 100)

        if A * B != C:
            if C == correct_C:
                error += 1

    error_rate = error / 1000

    print(f"Оролт = {n}, дундаж очих орой = {avgStep:.2f}, Хугацаа = {runTime:.4f} сек (log={logTime:.2f}), AxB!=C алдаа = {error_rate:.2%}")

plt.figure(figsize=(8, 5))
plt.plot(num, runtime, marker='o', linestyle='-', color='blue')
plt.xscale('linear')
plt.yscale('log')
plt.xlabel("Оролтын хэмжээ n")
plt.ylabel("Хугацаа (сек, log)")
plt.title("BST хайлт (log scale)")
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.tight_layout()

plt.savefig("bst.png")

plt.show()
