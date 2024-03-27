from metrics_compiled_c_array_hash import calc_metrics_array_hash

if __name__ == "__main__":

    s = "2 6|6|6 2".encode()
    maxEntityId = 3
    minCount = 1
    result = calc_metrics_array_hash(s, 10, 10, minCount, 10)
    print(result)
