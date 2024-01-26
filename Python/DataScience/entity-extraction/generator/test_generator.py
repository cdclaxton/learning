from .generator import *


def test_generate_tokens():
    for n_tokens in range(1, 20):
        tokens = generate_tokens(n_tokens, 20)
        assert len(tokens) == n_tokens
        assert all([int(ti[1:]) < 20 for ti in tokens])


def test_generate_entity_tokens():
    for n_tokens in range(1, 20):
        tokens = generate_entity_tokens(n_tokens, 20)
        assert len(tokens) == n_tokens
        assert len(set(tokens)) == n_tokens


def test_make_uniform_num_entity_tokens_generator():
    # Minimum and maximum value are the same
    min_value = max_value = 3
    f = make_uniform_num_entity_tokens_generator(min_value, max_value)
    for _ in range(100):
        assert f() == 3

    # Minimum and maximum value are different
    min_value = 2
    max_value = 5
    f = make_uniform_num_entity_tokens_generator(min_value, max_value)
    for _ in range(100):
        assert min_value <= f() <= max_value


def test_make_generator_fns():
    n_tokens = 100
    prop_entity_tokens = 0.5
    min_num_entity_tokens = 2
    max_num_entity_tokens = 5
    n_entity_tokens_fn = make_uniform_num_entity_tokens_generator(
        min_num_entity_tokens, max_num_entity_tokens
    )

    text_generator, entity_generator = make_generator_fns(
        n_tokens, prop_entity_tokens, n_entity_tokens_fn
    )

    # Check the text token generator
    for _ in range(100):
        num_tokens_to_generate = random.randint(1, 10)
        tokens = text_generator(num_tokens_to_generate)
        assert type(tokens) == list
        assert len(tokens) == num_tokens_to_generate
        for t in tokens:
            assert type(t) == str
            assert 0 <= int(t[1:]) < n_tokens

    # Check the entity generator
    for _ in range(100):
        tokens = entity_generator()
        assert type(tokens) == list
        assert min_num_entity_tokens <= len(tokens) <= max_num_entity_tokens
        for t in tokens:
            assert type(t) == str
            assert 0 <= int(t[1:]) < int(n_tokens * prop_entity_tokens)


def test_generate_entities():
    n_tokens = 100
    prop_entity_tokens = 0.5
    min_num_entity_tokens = 2
    max_num_entity_tokens = 5
    n_entity_tokens_fn = make_uniform_num_entity_tokens_generator(
        min_num_entity_tokens, max_num_entity_tokens
    )

    _, entity_generator = make_generator_fns(
        n_tokens, prop_entity_tokens, n_entity_tokens_fn
    )

    for num_entities in range(1, 10):
        entities = generate_entities(num_entities, entity_generator)

        # Check there are the correct number of entities
        assert len(entities) == num_entities

        # Check the tokens in the entity are unique
        set_tokens = {tuple(tokens) for tokens in entities.values()}
        assert len(set_tokens) == num_entities
