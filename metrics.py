import numpy as np


class ArrayMetrics:

    @staticmethod
    def _count_inversions(array: list[float]):
        length = len(array)
        if length == 1:
            return array, 0
        left = array[:length//2]
        right = array[length//2:]
        left, li = ArrayMetrics._count_inversions(left)
        right, ri = ArrayMetrics._count_inversions(right)
        merged = []

        l, r = 0, 0
        inversions = 0 + li + ri
        while l < len(left) and r < len(right):
            if left[l] < right[r]:
                merged.append(left[l])
                l += 1

            else:
                merged.append(right[r])
                r += 1
                inversions += len(left) - l

        merged += left[l:]
        merged += right[r:]
        return merged, inversions

    @staticmethod
    def get_array_metrics(array: list[float]):
        return {
            "size": len(array),
            "mean" : np.mean(array),
            "median" : np.median(array),
            "std" : np.std(array),
            "range" : max(array) - min(array),
            "max" : max(array),
            "min" : min(array),
            "inversions" : ArrayMetrics._count_inversions(array),

        }