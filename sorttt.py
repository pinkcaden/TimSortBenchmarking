import numpy as np
import timeit
import datetime
def bubble_sort_iterative(collection: list) -> list:

    length = len(collection)
    for i in reversed(range(length)):
        swapped = False
        for j in range(i):
            if collection[j] > collection[j + 1]:
                swapped = True
                collection[j], collection[j + 1] = collection[j + 1], collection[j]
        if not swapped:
            break  # Stop iteration if the collection is sorted.
    return collection
l = []
for n in range(100):
    l.append(np.random.rand())



time = datetime.datetime.now()
times = 1000000
for n in range(times):
    bubble_sort_iterative(l)
bubble_time = datetime.datetime.now() - time
time = datetime.datetime.now()
for n in range(times):
    sorted(l)
py_time = datetime.datetime.now()- time
print (bubble_time)
print(py_time)
print(bubble_time - py_time)



