import random

from randomize import RandomizedIteratorFactory

class Record:
    def __init__(self):
        self._operation_counts = {
            "<" : 0,
            ">" : 0,
            ">=" : 0,
            "<=" : 0,
            "==" : 0
        }

    def scratch_lt(self):
        self._operation_counts["<"] += 1

    def scratch_lte(self):
        self._operation_counts["<="] += 1

    def scratch_gt(self):
        self._operation_counts[">"] += 1

    def scratch_gte(self):
        self._operation_counts["<="] += 1

    def scratch_eq(self):
        self._operation_counts["=="] += 1

    def get_counts(self):
        return self._operation_counts


class Term(float):

    def __init__(self, value, record):
        self._value = value
        self._record = record

    def __new__(cls, value, record):
        return super().__new__(cls, value)

    def __eq__(self, other) -> bool:
        self._record.scratch_eq()
        return float.__eq__(self, other)

    def __lt__(self, other) -> bool:
        self._record.scratch_lt()
        return float.__lt__(self, other)

    def __gt__(self, other) -> bool:
        self._record.scratch_gt()
        return float.__gt__(self, other)


    def __le__(self, other) -> bool:
        self._record.scratch_lte()
        return float.__le__(self, other)

    def __ge__(self, other) -> bool:
        self._record.scratch_gte()
        return float.__ge__(self, other)


class Sorts:
    @staticmethod
    def _binary_search(lst, item, start, end):
        if start == end:
            return start if lst[start] > item else start + 1
        if start > end:
            return start

        mid = (start + end) // 2
        if lst[mid] < item:
            return Sorts._binary_search(lst, item, mid + 1, end)
        elif lst[mid] > item:
            return Sorts._binary_search(lst, item, start, mid - 1)
        else:
            return mid

    @staticmethod
    def _insertion_sort(lst):
        length = len(lst)

        for index in range(1, length):
            value = lst[index]
            pos = Sorts._binary_search(lst, value, 0, index - 1)
            lst = [*lst[:pos], value, *lst[pos:index], *lst[index + 1:]]

        return lst
    @staticmethod
    def merge(left, right):
        if not left:
            return right

        if not right:
            return left

        if left[0] < right[0]:
            return [left[0], *Sorts.merge(left[1:], right)]

        return [right[0], *Sorts.merge(left, right[1:])]
    @staticmethod
    def tim_sort(array):

        length = len(array)
        runs, sorted_runs = [], []
        new_run = [array[0]]
        sorted_array = []
        i = 1
        while i < length:
            if array[i] < array[i - 1]:
                runs.append(new_run)
                new_run = [array[i]]
            else:
                new_run.append(array[i])
            i += 1
        runs.append(new_run)

        for run in runs:
            sorted_runs.append(Sorts._insertion_sort(run))
        for run in sorted_runs:
            sorted_array = Sorts.merge(sorted_array, run)

        return sorted_array

    @staticmethod
    def quick_sort(array):

        if len(array) < 2:
            return array

        pivot_index = random.randrange(len(array))
        pivot = array.pop(pivot_index)

        lesser = [item for item in array if item <= pivot]
        greater = [item for item in array if item > pivot]

        return [*Sorts.quick_sort(lesser), pivot, *Sorts.quick_sort(greater)]

