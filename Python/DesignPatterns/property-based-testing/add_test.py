from hypothesis import assume, given, strategies as st
import math


# Commutativity, i.e. x + y == y + x
@given(x=st.integers(), y=st.integers())
def test_add_commutativity(x, y):
    assume(not math.isinf(x))
    assume(not math.isinf(y))
    assert x + y == y + x


# Associativity, i.e. (x + y) + z == x + (y + z)
@given(x=st.integers(), y=st.integers(), z=st.integers())
def test_add_associativity(x, y, z):
    assume(not math.isinf(x))
    assume(not math.isinf(y))
    assume(not math.isinf(z))
    assert (x + y) + z == x + (y + z)


# Identity, i.e. x + 0 = x
@given(x=st.integers())
def test_add_identity(x):
    assume(not math.isinf(x))
    assert x + 0 == x
