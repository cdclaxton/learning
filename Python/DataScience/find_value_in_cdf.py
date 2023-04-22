# Algorithm to find a probability in a CDF where the CDF has a sparse 
# representation.

def method(sparse_cdf, required_value):

    # If the value can be directly looked up, then return it
    if required_value in sparse_cdf:
        return sparse_cdf[required_value]

    # Get a sorted list of the keys
    keys = sorted(sparse_cdf.keys())

    if required_value < keys[0]:
        return 0.0
    
    for i in range(len(keys) - 1):
        if keys[i] < required_value < keys[i+1]:
            return sparse_cdf[keys[i]]
    
    return 1.0


if __name__ == '__main__':
    
    # sparse_cdf, required_value, expected
    test_cases = [
        ({0:1.0}, -1, 0.0),
        ({0:1.0}, 0, 1.0),
        ({0:1.0}, 1, 1.0),
        ({0:0.2, 1:1.0}, 0, 0.2),
        ({0:0.2, 1:1.0}, 0.5, 0.2),
        ({0:0.2, 1:1.0}, 1, 1.0),
        ({0:0.2, 1:1.0}, 1.5, 1.0),
        ({0:0.2, 1:0.4, 3:1.0}, -0.5, 0.0),
        ({0:0.2, 1:0.4, 3:1.0}, 0, 0.2),
        ({0:0.2, 1:0.4, 3:1.0}, 0.5, 0.2),
        ({0:0.2, 1:0.4, 3:1.0}, 1, 0.4),
        ({0:0.2, 1:0.4, 3:1.0}, 1.5, 0.4),
        ({0:0.2, 1:0.4, 3:1.0}, 2, 0.4),
        ({0:0.2, 1:0.4, 3:1.0}, 3, 1.0),
        ({0:0.2, 1:0.4, 3:1.0}, 4, 1.0),
    ]

    for idx, test_case in enumerate(test_cases):
        actual = method(test_case[0], test_case[1])
        assert test_case[2] == actual, f"{idx}: Expected {test_case[2]}, got {actual}"
    