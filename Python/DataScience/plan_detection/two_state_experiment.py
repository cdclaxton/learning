# Two-state experiment
import math
import numpy as np
import random


def sample_from_multinomial(p):
    """Generate a sample from a multinomial distribution."""

    return int(np.argmax(np.random.multinomial(1, p)))


def generate_observations(p_n1, cpt, num_obs):
    """Generate a list of observations for a model."""

    assert type(p_n1) == float and 0.0 <= p_n1 <= 1.0
    assert type(cpt) == list
    assert type(num_obs) == int and num_obs > 0

    # Choose the number of states in the model
    num_states = np.random.binomial(1, 1 - p_n1) + 1
    assert num_states in [1, 2]

    if num_states == 1:
        observations = [sample_from_multinomial(cpt[0]) for _ in range(num_obs)]
        return 0, observations

    else:
        # Changepoint in the range [1, num_obs - 1]
        tau = random.randint(1, num_obs - 1)

        observations = []
        for i in range(num_obs):
            if i < tau:
                observation = sample_from_multinomial(cpt[0])
            else:
                observation = sample_from_multinomial(cpt[1])

            observations.append(int(observation))

        return tau, observations


def likelihood_two_stages(x, cpt, s0_upper):
    """Likelihood of a model with two states."""

    assert type(x) == list and len(x) > 0
    assert type(cpt) == list and len(cpt) > 0
    assert type(s0_upper) == int

    log_likelihoods = 0
    for i in range(len(x)):
        # Event type of the observation
        event_type = x[i]
        assert (
            type(event_type) == int
        ), f"expected an int, got {type(event_type)}: {event_type}"

        if i < s0_upper:
            p = cpt[0][event_type]
        else:
            p = cpt[1][event_type]

        if p == 0:
            return 0.0

        log_likelihoods += math.log(p)

    return math.exp(log_likelihoods)


def latex_matrix(matrix):
    """Returns a matrix in Latex format."""

    latex = "\\begin{bmatrix} \n"
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if j < matrix.shape[1] - 1:
                latex += str(matrix[i, j]) + " & "
            else:
                latex += str(matrix[i, j])

        latex += " \\\\ \n"

    return latex + r"\end{bmatrix}"


def row_to_markdown(row):
    """Create a row in markdown format."""

    assert type(row) == list
    assert len(row) > 0

    y = [f"${xi}$" for xi in row]
    return "| " + " | ".join(y) + " |"


def make_separator(n):
    """Make a markdown table separator row."""

    assert type(n) == int
    assert n > 0

    row = ["--" for _ in range(n)]
    return "| " + " | ".join(row) + " |"


def markdown_cpt(cpt):
    # Make the header
    header = [f"e_{i}" for i in range(cpt.shape[1])]
    header.insert(0, " ")
    print(row_to_markdown(header))

    print(make_separator(cpt.shape[1] + 1))

    for idx in range(cpt.shape[0]):
        row = [cpt[idx][i] for i in range(cpt.shape[1])]
        row.insert(0, f"S_{idx}")
        print(row_to_markdown(row))


def show_experiment_config(p_n1, cpt, num_trials):
    assert 0.0 <= p_n1 <= 1.0
    assert type(num_trials) == int and num_trials > 0

    print(
        f"Probability of only one state is {p_n1} and the number of trials in the experiment is 1000. The CPT is:"
    )
    markdown_cpt(cpt)
    print()


def show_confusion_matrix(confusion_matrix, model_name):
    num_trials = np.sum(confusion_matrix)
    confusion_matrix = confusion_matrix / num_trials

    accuracy = np.trace(confusion_matrix)
    print(
        f"The confusion matrix for the {model_name} model (with an accuracy of {accuracy:.5f}) is:"
    )
    print("$$")
    print(latex_matrix(confusion_matrix))
    print("$$")


def single_model_approach(observations, cpt, p_n1):
    # Calculate the likelihood of each model
    likelihood_model_0 = likelihood_two_stages(observations, cpt, 4)
    likelihood_model_1 = likelihood_two_stages(observations, cpt, 1)
    likelihood_model_2 = likelihood_two_stages(observations, cpt, 2)
    likelihood_model_3 = likelihood_two_stages(observations, cpt, 3)

    # Likelihoods of each model given the observations
    likelihoods = np.array(
        [
            likelihood_model_0,
            likelihood_model_1,
            likelihood_model_2,
            likelihood_model_3,
        ]
    )

    # Prior probability of each model
    priors = np.array(
        [
            p_n1,
            (1 / 3) * (1 - p_n1),
            (1 / 3) * (1 - p_n1),
            (1 / 3) * (1 - p_n1),
        ]
    )

    # Unnormalised probability of each model
    p_model_given_x = likelihoods * priors

    # Find the most likely model and check that only one model is the
    # most likely
    most_likely_model_idx = np.argmax(p_model_given_x)
    assert len(np.where(p_model_given_x == p_model_given_x[most_likely_model_idx])) == 1

    return most_likely_model_idx


def max_likelihood(observations, cpt, p_n1):
    likelihood_model_0 = likelihood_two_stages(observations, cpt, 4)

    # Find the most likely two-stage model
    two_stages_likelihoods = [
        likelihood_two_stages(observations, cpt, 1),
        likelihood_two_stages(observations, cpt, 2),
        likelihood_two_stages(observations, cpt, 3),
    ]
    max_likelihood_two_stages = np.argmax(two_stages_likelihoods)

    # Calculate p(m|x)
    likelihoods = np.array(
        [
            likelihood_model_0,
            two_stages_likelihoods[max_likelihood_two_stages],
        ]
    )
    priors = np.array(
        [
            p_n1,
            1 - p_n1,
        ]
    )
    p_model_given_x = likelihoods * priors

    # Find the most likely model from the two selected
    most_likely_model_idx = np.argmax(p_model_given_x)

    if most_likely_model_idx == 0:
        return 0
    else:
        return 1 + max_likelihood_two_stages


def monte_carlo_simulations(num_experiments):
    assert type(num_experiments) == int and num_experiments > 0

    # Initialise the confusion matrices
    confusion_matrix = [[0, 0, 0, 0] for _ in range(4)]
    confusion_matrix_ml = [[0, 0, 0, 0] for _ in range(4)]
    confusion_matrix_random = [[0, 0, 0, 0] for _ in range(4)]

    for _ in range(num_experiments):
        # Generate a random value of p_n1
        p_n1 = np.random.random()

        # Generate a random CPT
        p00 = np.random.random()
        p11 = np.random.random()
        cpt = [[p00, 1.0 - p00], [1.0 - p11, p11]]

        # Generate the observations
        actual_model, observations = generate_observations(p_n1, cpt, num_obs)

        # Single model approach
        most_likely_model_idx = single_model_approach(observations, cpt, p_n1)
        confusion_matrix[actual_model][most_likely_model_idx] += 1

        # Find the most likely model using the maximum likelihood approach
        most_likely_model_idx_ml = max_likelihood(observations, cpt, p_n1)
        confusion_matrix_ml[actual_model][most_likely_model_idx_ml] += 1

        # Generate a sample using the priors
        random_choice = sample_from_multinomial(
            [p_n1, (1 / 3) * (1 - p_n1), (1 / 3) * (1 - p_n1), (1 / 3) * (1 - p_n1)]
        )
        confusion_matrix_random[actual_model][random_choice] += 1

    return {
        "confusion_matrix_single_model": confusion_matrix,
        "confusion_matrix_max_likelihood": confusion_matrix_ml,
        "confusion_matrix_random": confusion_matrix_random,
    }


if __name__ == "__main__":
    # Number of observations
    num_obs = 4

    # Number of trials per experiment
    num_trials = 10000

    # List of experiments to perform
    experiments = [
        {
            "name": "No uncertainty in the observation to state mapping",
            "p_n1": 0.99,
            "cpt": [[1, 0], [0, 1]],
        },
        {
            "name": "Probability of 0.5 for each state, no uncertainty in the observation to state mapping",
            "p_n1": 0.5,
            "cpt": [[1, 0], [0, 1]],
        },
        {
            "name": "Probability of 0.5 for each state",
            "p_n1": 0.5,
            "cpt": [[0.9, 0.1], [0.1, 0.9]],
        },
        {
            "name": "Probability of 0.3 for state 0",
            "p_n1": 0.3,
            "cpt": [[0.7, 0.3], [0.2, 0.8]],
        },
    ]

    for idx, experiment in enumerate(experiments):
        print(f"### Experiment {idx + 1}: {experiment['name']}")

        # Initialise the confusion matrices
        confusion_matrix = [[0, 0, 0, 0] for _ in range(4)]
        confusion_matrix_ml = [[0, 0, 0, 0] for _ in range(4)]
        confusion_matrix_random = [[0, 0, 0, 0] for _ in range(4)]

        for _ in range(num_trials):
            p_n1 = experiment["p_n1"]
            cpt = experiment["cpt"]

            # Generate the observations
            actual_model, observations = generate_observations(p_n1, cpt, num_obs)

            # Single model approach
            most_likely_model_idx = single_model_approach(observations, cpt, p_n1)
            confusion_matrix[actual_model][most_likely_model_idx] += 1

            # Find the most likely model using the maximum likelihood approach
            most_likely_model_idx_ml = max_likelihood(observations, cpt, p_n1)
            confusion_matrix_ml[actual_model][most_likely_model_idx_ml] += 1

            # Generate a sample using the priors
            random_choice = sample_from_multinomial(
                [p_n1, (1 / 3) * (1 - p_n1), (1 / 3) * (1 - p_n1), (1 / 3) * (1 - p_n1)]
            )
            confusion_matrix_random[actual_model][random_choice] += 1

        # Display the results of the trials
        show_experiment_config(p_n1, np.array(cpt), num_trials)
        show_confusion_matrix(np.array(confusion_matrix), "changepoint")
        print()
        show_confusion_matrix(np.array(confusion_matrix_ml), "max likelihood")
        print()
        show_confusion_matrix(np.array(confusion_matrix_random), "random")
        print()

    # Perform Monte Carlo experiments
    print("#### Monte Carlo experiments:")
    results = monte_carlo_simulations(10000)
    show_confusion_matrix(
        np.array(results["confusion_matrix_single_model"]), "changepoint"
    )
    print()
    show_confusion_matrix(
        np.array(results["confusion_matrix_max_likelihood"]), "max likelihood"
    )
    print()
    show_confusion_matrix(np.array(results["confusion_matrix_random"]), "random")
