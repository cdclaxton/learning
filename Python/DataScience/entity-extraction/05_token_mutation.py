# For each distance measure and a given number of mutations to a single
# token, calculate the distance over a set number of trials. The results
# are stored in a dict of the form:
#
# {
#   "<distance measure>": {
#       <number of mutations>: [<distances for each trial>]
#   }
# }

import random
import numpy as np

from faker import Faker
from strsimpy.levenshtein import Levenshtein
from strsimpy.damerau import Damerau
from strsimpy.optimal_string_alignment import OptimalStringAlignment
from strsimpy import SIFT4

from visualisation.markdown import markdown_row
from generator.token_mutation import random_mutation


fake = Faker()


def run_experiment(token, num_mutations, distance_measure, num_trials):
    """Run experiment using a given distance measure."""

    assert type(num_trials) == int
    assert num_trials > 0
    assert type(token) == str
    assert type(num_mutations) == int
    assert num_mutations >= 0

    results = []
    for _ in range(num_trials):
        token_as_list = [t for t in token]
        for _ in range(num_mutations):
            random_mutation(token_as_list)

        mutated_token = "".join(token_as_list)
        results.append(distance_measure(token, mutated_token))

    return results


def random_token():
    """Generate a random token."""

    text = fake.street_name()

    # If there are multiple tokens, then randomly select one of them
    if " " in text:
        text = random.choice(text.split())

    return text


def build_markdown_table(results, max_num_mutations):
    """Build a table in Markdown format."""

    assert type(results) == dict
    assert type(max_num_mutations) == int
    assert max_num_mutations >= 0

    # Rows of the table
    rows = []

    # Build the header
    header = [
        f"{i} mutations" if i != 1 else f"{i} mutation"
        for i in range(max_num_mutations + 1)
    ]
    header.insert(0, "Algorithm")
    header.append("Correlation")
    rows.append(markdown_row(header))

    # Add the divider between the header and the data rows
    rows.append(markdown_row(["--" for i in range(max_num_mutations + 3)]))

    for alg in results:
        row = [alg]
        expected = []
        actual = []

        for num_mutations in range(max_num_mutations + 1):
            mu = np.mean(results[alg][num_mutations])
            sigma = np.std(results[alg][num_mutations])
            cell = f"{mu} ({sigma:.3f})"
            row.append(cell)

            actual.extend(results[alg][num_mutations])
            expected.extend(
                [num_mutations for _ in range(len(results[alg][num_mutations]))]
            )

        # Calculate the correlation coefficient for the algorithm
        cc = np.corrcoef([expected, actual])[1, 0]
        row.append(f"{cc:.4f}")

        # Append a markdown version of the row to the table
        rows.append(markdown_row(row))

    return rows


if __name__ == "__main__":
    n_trials = 10000
    max_num_mutations = 3
    distance_measures = [
        {"fn": Damerau().distance, "name": "Damerau-Levenshtein"},
        {"fn": Levenshtein().distance, "name": "Levenshtein"},
        {"fn": OptimalStringAlignment().distance, "name": "Optimal string alignment"},
        {"fn": SIFT4().distance, "name": "SIFT4"},
    ]

    results = {}
    for measure in distance_measures:
        results[measure["name"]] = {}

        for num_mutations in range(0, max_num_mutations + 1):
            results[measure["name"]][num_mutations] = run_experiment(
                random_token(), num_mutations, measure["fn"], n_trials
            )

    # Build a table of the results in Markdown format
    table = build_markdown_table(results, max_num_mutations)
    for row in table:
        print(row)
