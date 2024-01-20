# Experiment to determine if a potentially mutated address entity has the
# highest posterior probability for the entity from which it was derived.
#
# 1. Generate a list of N > 0 address entities.
# 2. For each trial index i of M:
#   2a. Randomly select an entity from the generated list.
#   2b. Mutate the entity given the probability distribution of the number of
#       mutations.
#   2c. Calculate the posterior probability of each entity in the generated
#       list given the tokens in the potentially mutated entity.
#   2d. Record the entity in the generated list that maximises the posterior
#       probaility.
# 3. Present the results as a confusion matrix.
#
# Note that adding or removing tokens from an entity is out of scope of this
# experiment.

import math
import matplotlib.pyplot as plt
import numpy as np
import random

from token_mutation import random_mutations
from strsimpy.optimal_string_alignment import OptimalStringAlignment

from markdown import markdown_row


def generate_postcode():
    """Generate a UK-style postcode of the form XXNN NXX"""

    letters = "ABCDEFGHJKLMNPQRSTUVWXYZ"  # Note I and O removed
    individual_letters = [l for l in letters]

    p1 = "".join(
        [random.choice(individual_letters) for _ in range(random.randint(1, 2))]
    )
    p2 = "".join([str(random.randint(0, 9)) for _ in range(random.randint(1, 2))])
    p3 = str(random.randint(1, 9))
    p4 = "".join([random.choice(individual_letters) for _ in range(2)])

    return ["".join([p1, p2]), "".join([p3, p4])]


def generate_addresses(num_addresses_per_road, num_roads):
    """Generate a list of random UK-style addresses."""

    assert num_addresses_per_road > 0
    assert num_roads > 0

    # Generate a set of num_roads roads
    roads = set()
    while len(roads) < num_roads:
        road_name = random.choice(["Church", "Green", "Main", "Park", "Elm"])
        road_type = random.choice(["Road", "Street", "Terrace", "Way", "Drive"])

        potential_road = (road_name, road_type)
        roads.add(potential_road)

    # Add on a city and a postcode for each road
    locations = []
    for road_name, road_type in roads:
        loc = [
            road_name,
            road_type,
            random.choice(["Bristol", "Birmingham", "Manchester", "York"]),
        ]

        loc.extend(generate_postcode())
        locations.append(loc)

    # Add the required number of addresses per road
    full_addresses = []
    for loc in locations:
        for house_number in range(1, num_addresses_per_road + 1):
            x = loc[:]
            x.insert(0, str(house_number))
            full_addresses.append(x)

    return full_addresses


def mutate(address, p_mutation):
    """Mutate an address."""

    assert type(address) == list
    assert len(address) > 0
    assert type(p_mutation) == list
    assert len(p_mutation) > 0

    mutated = []
    for token in address:
        assert len(token) > 0

        # Randomly select the number of mutations
        num_mutations = np.argmax(np.random.multinomial(1, p_mutation))

        # Mutate the token
        if num_mutations == 0:
            mutated.append(token)
        else:
            mutated.append(random_mutations(token, num_mutations))

    assert len(mutated) == len(address)
    return mutated


def argmax(probs):
    """Returns the argmax of the probs. If there are multiple then one is randomly chosen."""

    matching = [i for i, p in enumerate(probs) if p == max(probs)]

    if len(matching) == 1:
        return matching[0]

    return random.choice(matching)


def calc_likelihood(address, mutated, p_mutations):
    """Calculate p(mutated | address)."""

    assert type(address) == list
    assert type(mutated) == list
    assert len(address) == len(mutated)
    assert type(p_mutations) == list

    total = 0
    for i in range(len(address)):
        distance = OptimalStringAlignment().distance(address[i], mutated[i])

        # Check the distance can be converted to an int
        assert distance - int(distance) < 1e-6
        distance = int(distance)

        if distance > (len(p_mutations) - 1):
            p = 1e-9
        else:
            p = p_mutations[distance]

        total += math.log(p)

    return math.exp(total)


def calc_posteriors(addresses, mutated, p_mutations):
    """Calculate posterior probabilities for each address."""

    assert type(addresses) == list
    assert type(mutated) == list
    assert type(p_mutations) == list

    posteriors = []

    for addr_tokens in addresses:
        assert type(addr_tokens) == list
        assert len(addr_tokens) == len(mutated)

        posteriors.append(calc_likelihood(addr_tokens, mutated, p_mutations))

    total = sum(posteriors)
    posteriors = [p / total for p in posteriors]

    return posteriors


def confusion_matrix(results):
    """Calculates the confusion matrix for the results."""

    assert type(results) == list

    max_address_index = max(max(results))

    # Initialise the confusion matrix
    matrix = np.zeros((max_address_index + 1, max_address_index + 1))

    for actual in range(max_address_index + 1):
        for predicted in range(max_address_index + 1):
            matrix[predicted, actual] = sum(
                [1 for r in results if r == (actual, predicted)]
            )

    return 100.0 * matrix / len(results)


if __name__ == "__main__":
    # Parameters
    num_addresses_per_road = 3
    num_roads = 2
    num_trials = 1000
    p_no_mutations = 0.8
    p_one_mutation = 0.9
    p_two_mutations = 0.1

    # Randomly generate a list of addresses
    addresses = generate_addresses(num_addresses_per_road, num_roads)
    print(f"Generated {len(addresses)} addresses")

    addresses_str = [" ".join(a) for a in addresses]
    print(addresses_str)

    # Probability distribution of the number of mutations
    p_mutations = [
        p_no_mutations,
        (1 - p_no_mutations) * p_one_mutation,
        (1 - p_no_mutations) * p_two_mutations,
    ]

    p_mutations_generate = [
        0,
        p_one_mutation,
        p_two_mutations,
    ]

    results = []

    for i in range(num_trials):
        # Select an address from the list
        selected = random.choice(range(len(addresses)))

        # Mutate the selected address
        mutuated = mutate(addresses[selected], p_mutations_generate)

        # Calculate the posterior probability of each entity given the mutated
        # entity
        posterior_probs = calc_posteriors(addresses, mutuated, p_mutations)
        assert len(posterior_probs) == len(addresses)

        # Find the entity that maximises the posterior probability
        max_posterior = argmax(posterior_probs)
        results.append((selected, max_posterior))

    # Create a confusion matrix of the results
    conf = confusion_matrix(results)
    print(conf)

    fig, ax = plt.subplots()
    ax.matshow(conf, cmap=plt.cm.Blues)

    for i in range(len(addresses)):
        for j in range(len(addresses)):
            c = conf[j, i]
            ax.text(i, j, str(c), va="center", ha="center")

    plt.show()
