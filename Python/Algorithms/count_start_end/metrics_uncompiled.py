import pickle
from collections import Counter
from typing import Dict, List, Tuple


def entities_list_of_pickled_list(
    data: List[bytes],
    min_count: int,
    num_entities: int,
) -> List[Tuple[int, int, int]]:

    counts: Counter = Counter()
    starts: Dict[int, int] = {}
    ends: Dict[int, int] = {}

    for idx, picked_list in enumerate(data):

        # Unpickle the list of entity IDs
        entity_ids = pickle.loads(picked_list)
        assert type(entity_ids) == list

        counts.update(entity_ids)

        for entity_id in entity_ids:
            starts.setdefault(entity_id, idx)
            ends[entity_id] = idx

    result = []
    for entity_id, count in counts.items():
        if count >= min_count:
            result.append((entity_id, starts[entity_id], ends[entity_id]))

    return result


def entities_list_of_pickled_set(
    data: List[bytes],
    min_count: int,
    num_entities: int,
) -> List[Tuple[int, int, int]]:

    counts: Counter = Counter()
    starts: Dict[int, int] = {}
    ends: Dict[int, int] = {}

    for idx, picked_list in enumerate(data):

        # Unpickle the set of entity IDs
        entity_ids = pickle.loads(picked_list)
        assert type(entity_ids) == set

        counts.update(entity_ids)

        for entity_id in entity_ids:
            starts.setdefault(entity_id, idx)
            ends[entity_id] = idx

    result = []
    for entity_id, count in counts.items():
        if count >= min_count:
            result.append((entity_id, starts[entity_id], ends[entity_id]))

    return result


def entities_list_of_strings(
    data: List[str],
    min_count: int,
    num_entities: int,
) -> List[Tuple[int, int, int]]:

    counts: Counter = Counter()
    starts: Dict[int, int] = {}
    ends: Dict[int, int] = {}

    counts: Counter = Counter()
    starts: Dict[int, int] = {}
    ends: Dict[int, int] = {}

    for idx, concatenated_entity_ids in enumerate(data):

        # Unpickle the list of entity IDs
        entity_ids = [int(e) for e in concatenated_entity_ids.split(" ")]

        counts.update(entity_ids)

        for entity_id in entity_ids:
            starts.setdefault(entity_id, idx)
            ends[entity_id] = idx

    result = []
    for entity_id, count in counts.items():
        if count >= min_count:
            result.append((entity_id, starts[entity_id], ends[entity_id]))

    return result
