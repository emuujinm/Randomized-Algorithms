import random
import time
import math
import platform
import psutil
import matplotlib.pyplot as plt

class Node:
    def __init__(self, val, lvl):
        self.val = val
        self.next = [None] * lvl

class SkipList:
    def __init__(self):
        self.head = Node(float('-inf'), 32)
        self.level = 1

    def rand_level(self):
        lvl = 1
        while lvl < 32 and random.random() < 0.5:
            lvl += 1
        return lvl

    def insert(self, val):
        update = [None] * 32
        cur = self.head
        for i in reversed(range(self.level)):
            while cur.next[i] and cur.next[i].val < val:
                cur = cur.next[i]
            update[i] = cur
        lvl = self.rand_level()
        if lvl > self.level:
            for i in range(self.level, lvl):
                update[i] = self.head
            self.level = lvl
        node = Node(val, lvl)
        for i in range(lvl):
            node.next[i] = update[i].next[i]
            update[i].next[i] = node

    def search(self, val):
        cur = self.head
        cnt = 0
        for i in reversed(range(self.level)):
            while cur.next[i] and cur.next[i].val < val:
                cur = cur.next[i]
                cnt += 1
            if cur.next[i] and cur.next[i].val == val:
                return cnt
            cnt += 1
        return cnt

def axb_test():
    errors = 0
    for _ in range(100):
        A = random.randint(1, 10000)
        B = random.randint(1, 10000)
        correct = A * B
        C = correct if random.random() < 0.5 else correct + random.randint(1, 100)
        if A * B != C and C == correct:
            errors += 1
    return errors / 1000

if __name__ == "__main__":
    print("CPU:", platform.processor())
    print("RAM:", round(psutil.virtual_memory().total / (1024**3), 2), "GB")

    tasks = [5_000_000, 10_000_000, 20_000_000]
    times = []
    log_times = []
    avg_steps_list = []
    error_rates = []

    for n in tasks:
        start_time = time.time()
        sl = SkipList()
        values = set()
        while len(values) < n:
            values.add(random.randint(0, n * 10 - 1))
        val_list = list(values)
        for val in val_list:
            sl.insert(val)

        s = 0
        for i in range(1_000_000):
            if i % 2:
                q = random.choice(val_list)
            else:
                q = random.randint(n * 10, n * 20)
            s += sl.search(q)

        elapsed = time.time() - start_time
        avg_steps = s / 1_000_000
        log_elapsed = math.log10(elapsed + 1e-9)
        error_rate = axb_test()

        print(f"Оролт = {n}, дундаж очих орой = {avg_steps:.2f}, Хугацаа = {elapsed:.4f} сек (log = {log_elapsed:.2f}), AxB!=C алдаа = {error_rate:.2%}")

        times.append(elapsed)
        log_times.append(log_elapsed)
        avg_steps_list.append(avg_steps)
        error_rates.append(error_rate)

    plt.figure(figsize=(8, 5))
    plt.plot(tasks, log_times, marker='o', color='blue', label='Log(Time)')
    plt.xscale('linear')
    plt.yscale('log')
    plt.xlabel("Оролтын хэмжээ n")
    plt.ylabel("Хугацаа (секунд, log)")
    plt.title("Skip List (log-scale)")
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.tight_layout()

    plt.savefig("skiplist.png")

    plt.show()
