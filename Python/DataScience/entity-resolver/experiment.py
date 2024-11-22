import itertools
import random


def generate_addresses(counts, n):
    """Generate n addresses where counts is the number of distinct tokens in each part."""
    assert len(counts) <= 26
    slot_identifer = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[: len(counts)]

    return [
        [
            f"{slot_identifer[i]}{random.randint(1, counts[i])}"
            for i in range(len(counts))
        ]
        for _ in range(n)
    ]


class AddressLookup:
    def __init__(self, k: int):
        assert type(k) == int and k > 0
        self.k = k

        self._id_to_address_tokens: dict[int, list[str]] = {}
        self._tokens_to_address_count: dict[tuple[str, ...], int] = {}
        self._tokens_to_address_ids: dict[tuple[str, ...], set[int]] = {}

    def add(self, address: list[str]):
        address_id = len(self._id_to_address_tokens)
        self._id_to_address_tokens[address_id] = address

        for ki in range(1, min(len(address), self.k) + 1):
            for comb in itertools.combinations(address, ki):
                t = tuple(sorted(list(comb)))
                if t in self._tokens_to_address_count:
                    self._tokens_to_address_count[t] += 1
                    self._tokens_to_address_ids[t].add(address_id)
                else:
                    self._tokens_to_address_count[t] = 1
                    self._tokens_to_address_ids[t] = set([address_id])

    def add_all(self, addresses: list[list[str]]) -> None:
        for a in addresses:
            self.add(a)

    def address(self, address_id: int) -> list[str] | None:
        return self._id_to_address_tokens.get(address_id, None)

    def num_addresses_for_tokens(self, tokens: tuple[str, ...]) -> int:
        return self._tokens_to_address_count.get(tokens, 0)

    def address_ids_for_tokens(self, tokens: tuple[str, ...]) -> set[int] | None:
        return self._tokens_to_address_ids.get(tokens, None)


def tuple_for_lookup(tokens: list[str], additional: str | None = None):
    """Tuple that can be used in the AddressLookup class."""
    one_extra_token = tokens[:]
    if additional is not None:
        one_extra_token.append(additional)
    return tuple(sorted(one_extra_token))


def index_of_least_common_token(
    tokens: list[str],
    previous: list[str],
    usable_indices: set[int],
    lookup: AddressLookup,
) -> int | None:
    """Returns the index of the next least common token."""

    lowest_count = None
    token_index_with_lowest_count = None

    for idx in usable_indices:
        tpl = tuple_for_lookup(previous, tokens[idx])
        c = lookup.num_addresses_for_tokens(tpl)

        if c == 0:
            continue
        elif c == 1:
            return idx

        if (lowest_count is None) or (lowest_count is not None and c < lowest_count):
            lowest_count = c
            token_index_with_lowest_count = idx

    return token_index_with_lowest_count


def unused_token_indices(
    tokens: list[str], lookup: AddressLookup, address_ids: set[int]
) -> set[int]:

    unused_indices = {i for i in range(len(tokens))}

    for address_id in address_ids:

        candidate_address_tokens = lookup.address(address_id)
        assert candidate_address_tokens is not None
        set_candidate_address_tokens = set(candidate_address_tokens)

        overlapping = [
            i for i, token in enumerate(tokens) if token in set_candidate_address_tokens
        ]

        for idx in overlapping:
            if idx in unused_indices:
                unused_indices.remove(idx)

        if len(unused_indices) == 0:
            return set()

    return unused_indices


def resolutions_given_starting_indices(
    starting_indices: set[int], lookup: AddressLookup, tokens: list[str]
) -> tuple[set[int], set[int]]:

    usable_indices = set(starting_indices)
    least_common_tokens: list[str] = []

    for _ in range(0, lookup.k):
        token_index = index_of_least_common_token(tokens, [], usable_indices, lookup)
        if token_index is None:
            break
        least_common_tokens.append(tokens[token_index])
        usable_indices.remove(token_index)

    if len(least_common_tokens) == 0:
        return set(), set()

    address_ids = lookup.address_ids_for_tokens(tuple_for_lookup(least_common_tokens))
    assert address_ids is not None
    assert len(address_ids) > 0

    next_starting_indices = unused_token_indices(tokens, lookup, address_ids)

    return (address_ids, next_starting_indices)


def potential_resolutions(lookup: AddressLookup, tokens: list[str]) -> set[int]:
    """Potential address IDs."""

    starting_indices = {i for i in range(len(tokens))}
    potential_ids: set[int] = set()

    while len(starting_indices) > 0:
        address_ids, starting_indices = resolutions_given_starting_indices(
            starting_indices, lookup, tokens
        )
        potential_ids.update(address_ids)

    return potential_ids


if __name__ == "__main__":
    # Generate a list of random addresses
    addresses = generate_addresses([10, 5, 3, 5, 5, 2], 100)

    # Create a lookup of the addresses and their tokens
    max_tuple_length = 2
    lookup = AddressLookup(max_tuple_length)
    lookup.add_all(addresses)

    for _ in range(10000):

        # Randomly select an address
        selected_address = random.choice(addresses)[:]
        mutated_selected_address = selected_address[:]

        # Shuffle the tokens of the address
        random.shuffle(mutated_selected_address)

        # Retain some of the tokens
        num_tokens_keep = random.randint(1, len(selected_address))
        mutated_selected_address = random.sample(
            mutated_selected_address, num_tokens_keep
        )

        # Add additional tokens

        selected_address_found = False
        potential_ids = potential_resolutions(lookup, mutated_selected_address)
        for id in potential_ids:
            address_tokens = lookup.address(id)
            if address_tokens == selected_address:
                selected_address_found = True

        assert selected_address_found
