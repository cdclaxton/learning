from hypothesis import assume, example, given, settings, strategies as st
from math import isnan
import re
import string


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


def extract_vrn(s: str) -> list[str]:
    pattern = re.compile(r"[A-Z]{2}[0-9]{2}\s[A-Z]{3}")
    return pattern.findall(s)


@st.composite
def vrn_generator(draw):
    letters1 = draw(st.text(alphabet=string.ascii_uppercase, min_size=2, max_size=2))
    number1 = draw(st.integers(min_value=0, max_value=9))
    number2 = draw(st.integers(min_value=0, max_value=9))
    letters2 = draw(st.text(alphabet=string.ascii_uppercase, min_size=3, max_size=3))
    return f"{letters1}{number1}{number2} {letters2}"


@given(t1=st.text(), t2=st.text(), vrn=vrn_generator())
def test_extract_vrn(t1, t2, vrn):
    t = f"{t1} {vrn} {t2}"
    results = extract_vrn(t)
    assert vrn in results
