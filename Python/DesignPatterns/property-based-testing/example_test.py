from hypothesis import assume, example, given, settings, strategies as st
from math import isnan


@settings(max_examples=500)  # explicitly set the number of cases to run
@given(x=st.integers(), y=st.integers())
def test_commutative(x: int, y: int):
    assert x + y == y + x


@given(x=st.lists(st.integers()))
@example([])  # ensures this case is always tested
def test_double_reverse(x):
    y = list(x)
    y.reverse()
    y.reverse()
    assert x == y


@given(x=st.integers().filter(lambda x: x % 2 == 0))
def test_odd_integers(x):
    assert (2 * x) % 2 == 0


@given(x=st.floats())
def test_double_negation(x):
    assume(not isnan(x))  # required to avoid assert nan == --nan
    assert x == -(-x)


class Person:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    def has_birthday(self):
        self.age += 1


# Strategy for generating random names
names = st.text(min_size=1, max_size=100)

# Strategy for generating random ages
ages = st.integers(min_value=0, max_value=120)


# Strategy for generating random Person objects
@st.composite
def person_object(draw):
    return Person(name=draw(names), age=draw(ages))


@given(person_object())
def test_person(person: Person):
    assert person.age >= 0
    assert len(person.name) > 0
    current_age = person.age
    person.has_birthday()
    new_age = person.age
    assert new_age > current_age
