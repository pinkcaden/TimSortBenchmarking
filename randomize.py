import numpy as np

## Randomized Iterator Factory encapsulates RandomizedIterator

## Randomized Iterator Class
## Contains original list and uniform distribution random floating point array.
## Iteration can be started with a randomness "percentage"

## Chosen sorting algorithm: Cocktail Shaker Sort. Shaker sort is stable, performs in-place
## swaps, and operates on the entire array in every pass.

class RandomizedIterator:
    def __init__(self, array: list):
        self._passes_requested = None
        self._iter_order = None
        self._array = array
        random_list = np.random.uniform(size=len(array)).tolist()
        self._random_order = []
        for index in range(len(random_list)):
            self._random_order.append({"val": random_list[index], "index": index})
        self._required_passes = 0
        swapped = True
        start = 0
        end = len(array) - 1
        while swapped:
            swapped = False
            for i in range(start, end):
                if random_list[i] > random_list[i + 1]:
                    random_list[i], random_list[i + 1] = random_list[i + 1], random_list[i]
                    swapped = True

            if not swapped:
                break
            self._required_passes += 1
            swapped = False
            end = end - 1
            for i in range(end - 1, start - 1, -1):
                if random_list[i] > random_list[i + 1]:
                    random_list[i], random_list[i + 1] = random_list[i + 1], random_list[i]
                    swapped = True
            start = start + 1

    def __iter__(self):
        if self._passes_requested is None:
            raise RuntimeError("Randomization not set. Must set before each iteration.")
        self._next = 0
        self._iter_order = self._shaker_sort()
        return self

    def __next__(self):
        if self._next < len(self._array):
            ret = self._array[self._iter_order[self._next]["index"]]
            self._next += 1
            return ret
        else:
            self._passes_requested = None
            self._iter_order = None
            raise StopIteration

    def set_randomization(self, percentage: int) -> None:
        if percentage < 0 or percentage > 100:
            raise ValueError("Percentage must be between 0 and 100")
        self._passes_requested = int((percentage / 100 ) * self._required_passes)

    def _shaker_sort(self):
        copy = self._random_order[:]
        swapped = True
        start = 0
        end = len(copy) - 1
        passes = self._passes_requested

        while swapped and passes > 0:
            swapped = False
            for i in range(start, end):
                if copy[i]["val"] > copy[i + 1]["val"]:
                    copy[i], copy[i + 1] = copy[i + 1], copy[i]
                    swapped = True
            if not swapped:
                break
            swapped = False
            passes -= 1
            end = end - 1
            for i in range(end - 1, start - 1, -1):
                if copy[i]["val"] > copy[i + 1]["val"]:
                    copy[i], copy[i + 1] = copy[i + 1], copy[i]
                    swapped = True
            start = start + 1
        return copy

class RandomizedIteratorFactory:
    def __init__(self):
        pass
    @staticmethod
    def get_randomized_iterator(array):
        if len(array) == 0 or array is None:
            raise RuntimeError("Array is empty or None")
        return RandomizedIterator(array)

sout1 = []
sout2 = []
sout3 = []
sout4 = []
ob = RandomizedIteratorFactory.get_randomized_iterator([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,
                                                        17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
                                                        27, 28, 29, 30, 31, 32, 33 ,34, 35, 36, 37, 38,
                                                        39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
                                                        51, 52, 53, 54, 55, 56, 57, 58, 59, 60])
print("______________________________________________________________________________________________")
ob.set_randomization(0)
for n in ob:
    sout1.append(n)

ob.set_randomization(30)
for n in ob:
    sout2.append(n)

ob.set_randomization(60)
for n in ob:
    sout3.append(n)

ob.set_randomization(100)
for n in ob:
    sout4.append(n)

print("0%: " + str(sout1))
print("30%: " + str(sout2))
print("60%: " + str(sout3))
print("100%: " + str(sout4))

sout1 = []
sout2 = []
sout3 = []
sout4 = []
ob = RandomizedIteratorFactory.get_randomized_iterator([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                                        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                                        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,1, 1,  ])
print("______________________________________________________________________________________________")
ob.set_randomization(0)
for n in ob:
    sout1.append(n)

ob.set_randomization(30)
for n in ob:
    sout2.append(n)

ob.set_randomization(60)
for n in ob:
    sout3.append(n)

ob.set_randomization(30)
for n in ob:
    sout4.append(n)

print("0%: " + str(sout1))
print("30%: " + str(sout2))
print("60%: " + str(sout3))
print("100%: " + str(sout4))

sout1 = []
sout2 = []
sout3 = []
sout4 = []
ob = RandomizedIteratorFactory.get_randomized_iterator([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                                        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                                        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                                        2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                                                        2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2])
print("______________________________________________________________________________________________")
ob.set_randomization(0)
for n in ob:
    sout1.append(n)

ob.set_randomization(30)
for n in ob:
    sout2.append(n)

ob.set_randomization(60)
for n in ob:
    sout3.append(n)

ob.set_randomization(100)
for n in ob:
    sout4.append(n)

print("0%: " + str(sout1))
print("30%: " + str(sout2))
print("60%: " + str(sout3))
print("100%: " + str(sout4))