separator = " "

def entities_above_threshold(entities: str, min_count: int):
    
    entity_ids = entities.split(separator)

    counts = {}
    for e in entity_ids:
        if e not in counts:
            counts[e] = 1
        else:
            counts[e] += 1

    entity_ids_above_count = []

    for entity_id, count in counts:
        if count > min_count:
            entity_ids_above_count.append(entity_id)

    return entities_above_threshold