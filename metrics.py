import datetime
import platform
import socket
import sys

import numpy as np
import psutil
import scipy.stats as stats


class ArrayMetrics:
    @staticmethod
    def _count_runs(arr: list[float]):
        asc = 0
        desc = 0
        i = 0
        l = len(arr)
        while i < l - 1:
            if arr[i] < arr[i + 1]:
                while i < l - 1 and arr[i] < arr[i + 1]:
                    i += 1
                asc += 1
            elif arr[i] > arr[i + 1]:
                while i < l - 1 and arr[i] > arr[i + 1]:
                    i += 1
                desc += 1
            else:
                i += 1
        return asc, desc

    @staticmethod
    def _count_inversions(array: list[float]):
        length = len(array)
        if length == 1:
            return array, 0
        left = array[:length // 2]
        right = array[length // 2:]
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
    def get_array_metrics(array):
        runs = ArrayMetrics._count_runs(array)
        asc_runs = runs[0]
        desc_runs = runs[1]
        inversions = ArrayMetrics._count_inversions(array)[1]
        l = len(array)
        return {
            "length": l,
            "mean": float(np.mean(array)),
            "median": float(np.median(array)),
            "std": float(np.std(array)),
            "range": float(max(array) - min(array)),
            "max": float(max(array)),
            "min": float(min(array)),
            "inversions": inversions,
            "ascRuns": asc_runs,
            "descRuns": desc_runs,
            "kendallTau": float(stats.stats.kendalltau(array, sorted(array)).statistic),
            "runDensity" : (asc_runs + desc_runs) / l,
        }

class EnvironmentCapture:
    @staticmethod
    def capture(env_config):
        env_data = {}

        if env_config.get('cpuInfo'):
            env_data['cpu_model'] = platform.processor()
            env_data['cpu_cores'] = psutil.cpu_count(logical=False)
            env_data['cpu_threads'] = psutil.cpu_count(logical=True)
            freq = psutil.cpu_freq()
            env_data['cpu_frequency_mhz'] = freq.current if freq else None

        if env_config.get('ramInfo'):
            env_data['ram_total_gb'] = psutil.virtual_memory().total / (1024 ** 3)
            env_data['ramAvailableGB'] = psutil.virtual_memory().available / (1024 ** 3)

        if env_config.get('OSInfo'):
            env_data['OSName'] = platform.system()
            env_data['OSVersion'] = platform.version()

        if env_config.get('pythonVersion'):
            env_data['pythonVersion'] = sys.version

        if env_config.get('timeStamp'):
            env_data['timeStamp'] = datetime.datetime.now().isoformat()

        if env_config.get('hostName'):
            env_data['hostName'] = socket.gethostname()

        return env_data