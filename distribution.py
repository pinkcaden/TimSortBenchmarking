import math

def get_q1(sample):
    return sorted(sample)[math.floor(len(sample)/4)]

def get_q3(sample):
    return sorted(sample)[math.floor(3 * (len(sample) / 4))]

def get_iqr(sample):
    return get_q3(sample) - get_q1(sample)

def get_l_outlier(sample):
    return get_q1(sample) - (1.5 * get_iqr(sample))

def get_r_outlier(sample):
    return get_q3(sample) + (1.5 * get_iqr(sample))

def get_range(sample):
    sorted_sample = sorted(sample)
    return sorted_sample[len(sample) - 1] - sorted_sample[0]

def get_median(sample):
    sorted_sample = sorted(sample)
    sample_size = len(sample)
    if sample_size % 2 == 0:
        return (sorted_sample[int((sample_size / 2) - 1)] + sorted_sample[int((sample_size / 2))]) / 2
    return sorted_sample[int((sample_size / 2) - 1)]


def get_mean(sample):
    run_total = 0
    for num in sample:
        run_total += num
    return run_total/len(sample)

def get_sample_variance(sample):
    mean = get_mean(sample)
    run_total = 0
    for num in sample:
        run_total += (num - mean) ** 2
    return run_total/(len(sample) - 1)

def get_standard_deviation(sample):
    return math.sqrt(get_sample_variance(sample))
