from distributions import *
from itertools import chain, combinations
import math
import matplotlib.pyplot as plt
import numpy as np
import random


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)  # allows duplicate elements
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


if __name__ == "__main__":

    # Number of elements in a vector
    N = discrete_uniform(3, 20)
    N_features = N()

    # Probability of each element occurring in a vector
    p = [bernoulli(beta(1, 5)()) for _ in range(N_features)]

    # Number of vectors of noise
    M_noise = discrete_uniform(1, 20)

    # Number of vectors of signal
    M_signal = discrete_uniform(3, 5)

    # Number of features in the signal set to 1
    max_features_signal = max(1, math.floor(N_features / 5))
    N_feature_signal = discrete_uniform(1, max_features_signal)()
    print(f"Number of features in signal: {N_feature_signal}")

    # Indices of the features to set to 1
    feature_indices = random.sample(range(N_features), N_feature_signal)

    # Generate the noise vectors
    noise_vectors = []
    for _ in range(M_noise()):
        v = [pi() for pi in p]
        assert len(v) == N_features
        noise_vectors.append(v)

    # Generate the signal vectors
    signal_vectors = []
    for _ in range(M_signal()):
        v = [1 if idx in feature_indices else 0 for idx in range(N_features)]
        signal_vectors.append(v)

    # Combine the vectors
    vectors = noise_vectors[:]
    vectors.extend(signal_vectors)

    ground_truth = [0 for _ in range(len(noise_vectors))]
    ground_truth.extend([1 for _ in range(len(signal_vectors))])

    # Shuffle the vectors
    z = list(zip(vectors, ground_truth))
    random.shuffle(z)
    vectors, ground_truth = list(zip(*z))
    vectors = list(vectors)
    ground_truth = list(ground_truth)

    # Indices of the signal vectors
    ground_truth_signal_indices = [i for i, v in enumerate(ground_truth) if v == 1]
    print(f"Ground truth signal indices: {ground_truth_signal_indices}")

    # Calculate the empirical probability of each feature occurring
    p_feature_estimated = list(np.sum(vectors, axis=0) / len(vectors))
    assert len(p_feature_estimated) == N_features, f"length of p vector: {len(p_feature_estimated)}, n elements: {N_features}"

    results = []

    for seed_vector_idx, seed_vector in enumerate(vectors):

        # Find the indices where the seed vector is set to 1
        seed_vector_indices_true = (
            np.argwhere(np.array(seed_vector) == 1).flatten().tolist()
        )
        if len(seed_vector_indices_true) == 0:
            continue

        # Walk through all possible combinations of the features
        for combo in powerset(seed_vector_indices_true):
            if len(combo) == 0:
                continue

            matching_candidate_indices = []

            for candidate_vector_idx, candidate_vector in enumerate(vectors):
                if seed_vector_idx == candidate_vector_idx:
                    continue

                if all([candidate_vector[i] == 1 for i in combo]):
                    matching_candidate_indices.append(candidate_vector_idx)

            if len(matching_candidate_indices) == 0:
                continue

            all_vector_indices = [seed_vector_idx]
            all_vector_indices.extend(matching_candidate_indices)
            all_vector_indices = sorted(all_vector_indices)

            # Ensure all of the probabilities of the features set to 1 are 
            # greater than zero
            assert all([pi > 0 for i, pi in enumerate(p_feature_estimated) if i in combo]), f"combo: {combo}, p: {p_feature_estimated}"

            # Calculate the probability of the occurrences of the features
            prob = np.exp(
                len(all_vector_indices)
                * np.sum(
                    [
                        np.log(pi)
                        for i, pi in enumerate(p_feature_estimated)
                        if i in combo
                    ]
                )
            )

            results.append([all_vector_indices, combo, prob])

    # Remove duplicates
    deduplicated_results=  []
    for r in results:
        if r not in deduplicated_results:
            deduplicated_results.append(r)
    
    deduplicated_results = sorted(deduplicated_results, key=lambda x: x[2])
    for r in deduplicated_results:
        if r[0] == ground_truth_signal_indices:
            print(f"{r} <-- ground truth signal")
        else:
            print(r)
