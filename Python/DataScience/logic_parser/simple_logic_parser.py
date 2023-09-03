# Simple logic parser
#
# The parser evaluates Boolean expressions of the form:
#
# p_0 + p_1 + ... + p_{N-1}
#
# where p_i represents either a single variable or multiple variables
# ANDed together. The variables in the combination for p_i can be NOTed.
#
# An example of a valid expression is:
# 
# A.B + !C.B.D
#

import re

OR_SYMBOL = "+"
AND_SYMBOL = "."
NOT_SYMBOL = "!"
SPACE_SYMBOL = " "

def logic_or(values):
    """Logical OR on the values."""
    assert type(values) == list
    assert all([type(v) == bool for v in values])

    if len(values) == 1:
        return values[0]

    partial = values[0] or values[1]
    for i in range(2, len(values)):
        partial = partial or values[i]
    
    return partial

def logic_and(values):
    """Logical AND on the values."""
    assert type(values) == list
    assert all([type(v) == bool for v in values])

    if len(values) == 1:
        return values[0]

    partial = values[0] and values[1]
    for i in range(2, len(values)):
        partial = partial and values[i]
    
    return partial        

def logic_not(value):
    """Logical NOT."""

    assert type(value) == bool
    return not value

def split_by_or(eqn):
    """Split the terms by the highest level OR symbol."""

    parts = []
    current_group = ""
    in_brackets = False

    for token in eqn:
        if not in_brackets:
            if token == OR_SYMBOL and len(current_group) > 0:

                parts.append(current_group.strip())
                current_group = ""

            elif token == "(":
                in_brackets = True
                current_group += token
            else:
                current_group += token

        else:
            if token == ")":
                in_brackets = False

            current_group += token

    parts.append(current_group.strip())

    return parts

def test_split_by_or():
    """Unit tests for split_by_or()."""
    
    test_cases = [
        {
            "eqn": "A",
            "expected": ["A"]
        },
        {
            "eqn": "A.B",
            "expected": ["A.B"]
        },        
        {
            "eqn": "A + B",
            "expected": ["A", "B"]
        },
        {
            "eqn": "A.(C+D) + B",
            "expected": ["A.(C+D)", "B"]
        },
        {
            "eqn": "(C+D).A + B",
            "expected": ["(C+D).A", "B"]
        },
        {
            "eqn": "(C+D).A + B.(A)",
            "expected": ["(C+D).A", "B.(A)"]
        },        
    ]

    for test_case in test_cases:
        actual = split_by_or(test_case['eqn'])
        assert actual == test_case['expected'], \
            f"Eqn: {test_case['eqn']}, expected: {test_case['expected']}, got {actual}"
        
def expand_pair(eqn):
    """Expand a pair of terms."""

    parts = []

    # Pattern to match: (A + !B).C
    p1 = r"\(([A-Za-z0-9\+!\s]+)\)\.([A-Za-z0-9!])"
    m1 = re.match(p1, eqn)

    # Pattern to match: C.(A + !B)
    p2 = r"([A-Za-z0-9!])\.\(([A-Za-z0-9\+!\s]+)\)"
    m2 = re.match(p2, eqn)

    # Pattern to match: (A + B).(C + !D)
    p3 = r"\(([A-Za-z0-9\+!\s]+)\)\.\(([A-Za-z0-9\+!\s]+)\)"
    m3 = re.match(p3, eqn)

    if m1 is not None:
        group = m1.groups()[0]
        singleton = m1.groups()[1]

        for term in group.split(OR_SYMBOL):
            parts.append(term.strip() + AND_SYMBOL + singleton)

    elif m2 is not None:
        singleton = m2.groups()[0]   
        group = m2.groups()[1]
        
        for term in group.split(OR_SYMBOL):
            parts.append(singleton + AND_SYMBOL + term.strip())        
    
    elif m3 is not None:
        group1 = m3.groups()[0]
        group2 = m3.groups()[1]

        for term1 in group1.split(OR_SYMBOL):
            for term2 in group2.split(OR_SYMBOL):
                parts.append(term1.strip() + AND_SYMBOL + term2.strip())   

    else:
        raise Exception(f"Unknown eqn: {eqn}")

    return f" {OR_SYMBOL} ".join(parts)

def test_expand_pair():
    """Unit tests for expand_pair()."""

    test_cases = [
        {
            "eqn": "A.(B + C)",
            "expected": "A.B + A.C"
        },
        {
            "eqn": "A.(B + C)",
            "expected": "A.B + A.C"
        },
        {
            "eqn": "A.(B + C + D)",
            "expected": "A.B + A.C + A.D"
        },
        {
            "eqn": "(A + B).C",
            "expected": "A.C + B.C"
        },
        {
            "eqn": "(A + B).C",
            "expected": "A.C + B.C"
        },
        {
            "eqn": "(A + B + D).C",
            "expected": "A.C + B.C + D.C"
        },
        {
            "eqn": "(A + B).(C + D)",
            "expected": "A.C + A.D + B.C + B.D"
        }
    ]

    for test_case in test_cases:
        actual = expand_pair(test_case['eqn'])
        assert actual == test_case['expected'], \
            f"Eqn: {test_case['eqn']}, expected: {test_case['expected']}, got: {actual}"

def split_terms(eqn):
    """Split an equation into multiplied terms."""

    parts = []

    group_start = 0
    in_brackets = False

    for i,t in enumerate(eqn):

        if t == "(":
            in_brackets = True
            if group_start < i and i>=1 and eqn[i-1] == ".":
                parts.append(eqn[group_start:(i-1)])
                group_start = i
    
        elif t == ")" and in_brackets:
            parts.append(eqn[group_start:(i+1)])
            group_start = i+2

    if group_start < len(eqn):
        parts.append(eqn[group_start:])

    return parts


def test_split_terms():
    """Unit tests for split_terms()."""

    test_cases = [
        {
            "eqn": "A",
            "expected": ["A"]
        },
        {
            "eqn": "A.B",
            "expected": ["A.B"]
        },
        {
            "eqn": "A.(B)",
            "expected": ["A", "(B)"]
        },
        {
            "eqn": "A.(B).C",
            "expected": ["A", "(B)", "C"]
        },
        {
            "eqn": "(A).B",
            "expected": ["(A)", "B"]
        },
        {
            "eqn": "(A + C).B",
            "expected": ["(A + C)", "B"]
        },
        {
            "eqn": "(A + B).(C + D)",
            "expected": ["(A + B)", "(C + D)"]
        },
        {
            "eqn": "A.(B + C).D",
            "expected": ["A", "(B + C)", "D"]
        },
        {
            "eqn": "A.(B + C).(D + E)",
            "expected": ["A", "(B + C)", "(D + E)"]
        },        
    ]

    for test_case in test_cases:
        actual = split_terms(test_case['eqn'])
        assert actual == test_case['expected'], \
            f"Eqn: {test_case['eqn']}, expected: {test_case['expected']}, actual: {actual}"

def enclose(eqn):
    """Enclose the equation in brackets if not already present."""

    if not eqn.startswith("(") and not eqn.endswith(")"):
        return f"({eqn})"
    else:
        return eqn

def expand_part(eqn):
    """Expand all parts"""

    # Split the terms into multiplied groups
    all_terms = split_terms(eqn)
    if len(all_terms) < 2:
        return eqn
    
    first = enclose(all_terms[0])
    second = enclose(all_terms[1])
    combined = f"{first}{AND_SYMBOL}{second}"
    expanded = expand_pair(combined)

    for i in range(2, len(all_terms)):
        third = enclose(all_terms[i])
        expanded = enclose(expanded)
        combined = f"{expanded}{AND_SYMBOL}{third}"
        expanded = expand_pair(combined)        

    return expanded

def test_expand_part():
    """Unit tests for expand_part()."""

    test_cases = [
        {
            "eqn": "A",
            "expected": "A"
        },
        {
            "eqn": "A.B",
            "expected": "A.B"
        },
        {
            "eqn": "A.!B",
            "expected": "A.!B"
        },        
        {
            "eqn": "A.(B+C)",
            "expected": "A.B + A.C"
        },
        {
            "eqn": "A.(B+!C)",
            "expected": "A.B + A.!C"
        },        
        {
            "eqn": "(B+C).A",
            "expected": "B.A + C.A"
        },
        {
            "eqn": "(B+!C).A",
            "expected": "B.A + !C.A"
        },        
        # {
        #     "eqn": "A.(B+C).D",
        #     "expected": "A.B.D + A.C.D"
        # },  
        # {
        #     "eqn": "A.(B+!C).D",
        #     "expected": "A.B.D + A.!C.D"
        # },                
        # {
        #     "eqn": "A.(B+C).!D",
        #     "expected": "A.B.!D + A.C.!D"
        # },
    ]

    for test_case in test_cases:
        actual = expand_part(test_case['eqn'])
        assert actual == test_case['expected'], \
            f"Eqn: {test_case['eqn']}, expected: {test_case['expected']}, got: {actual}"


def expand(eqn):
    """Expand terms in brackets."""

    # Split terms by the OR symbol
    parts = split_by_or(eqn)
    assert type(parts) == list
    print(f"Parts: {parts}")

    all_expanded_terms = []
    for p in parts:
        print(f"  {p}")
        expanded = expand_part(p)
        if type(expanded) == str:
            all_expanded_terms.extend([expanded])
        else:
            all_expanded_terms.extend(expanded)

    print(f"  all_expanded_terms = {all_expanded_terms}")
    if len(all_expanded_terms) > 1:
        return f" {OR_SYMBOL} ".join(all_expanded_terms)
    else:
        return all_expanded_terms[0]

def test_expand():
    """Unit tests for expand()."""

    test_cases = [
        {
            "eqn": "A",
            "expected": "A"
        },
        {
            "eqn": "A.B",
            "expected": "A.B"
        },
        {
            "eqn": "A.B + C",
            "expected": "A.B + C"
        },
        {
            "eqn": "A.(C+D)",
            "expected": "A.C + A.D"
        },
        {
            "eqn": "(C+D).A",
            "expected": "C.A + D.A"
        },        
        {
            "eqn": "A.B.(C+D)",
            "expected": "A.B.C + A.B.D"
        }
        # {
        #     "eqn": "A.(B+C).D",
        #     "expected": "A.B.D + A.C.D"
        # },
        # {
        #     "eqn": "A.(B+C) + D.(E+F)",
        #     "expected": "A.B + A.C + D.E + D.F"
        # },
        # {
        #     "eqn": "A.(C+!D)",
        #     "expected": "A.C + A.!D"
        # },
    ]

    for test_case in test_cases:

        actual = expand(test_case['eqn'])

        assert actual == test_case['expected'], \
            f"Eqn: {test_case['eqn']}, expected: {test_case['expected']}, got: {actual}"



def calc_part(eqn, variables):
    """Calculate the part where the variables are ANDed together."""

    assert type(eqn) == str
    assert OR_SYMBOL not in eqn
    assert " " not in eqn
    assert len(eqn) > 0
    assert type(variables) == dict

    parts = eqn.split(AND_SYMBOL)
    part_values = []
    for p in parts:
        perform_not = False
        if p.startswith(NOT_SYMBOL):
            perform_not = True
            name = p[1:]
        else:
            name = p

        # Is the variable known?
        if name not in variables:
            return False, f"Unknown variable: {name}"
        
        name_value = variables[name]
        if perform_not:
            name_value = logic_not(name_value)
        
        part_values.append(name_value)
        
    # The values are combined using a logical AND
    return logic_and(part_values), None


def calc(eqn, variables):
    """Calculate the result of the boolean equation."""

    parts = [p.strip() for p in eqn.split(OR_SYMBOL)]

    # Calculate the result of each part
    parts_result = []
    for part in parts:
        result, err = calc_part(part, variables)
        if err is not None:
            return False, 0, err
        
        parts_result.append(result)
        
    num_true_parts = sum([p for p in parts_result])

    return logic_or(parts_result), num_true_parts, None


def test_calc():
    """Unit tests for calc()."""

    test_cases = [
        {
            "variables": {"A": False},
            "eqn": "A",
            "expected": False,
            "num_true_parts": 0,
            "error": False
        },
        {
            "variables": {"A": True},
            "eqn": "A",
            "expected": True,
            "num_true_parts": 1,
            "error": False
        },
        {
            "variables": {"A": False},
            "eqn": "!A",
            "expected": True,
            "num_true_parts": 1,
            "error": False
        },  
        {
            "variables": {"A": True},
            "eqn": "!A",
            "expected": False,
            "num_true_parts": 0,
            "error": False
        },                  
        {
            "variables": {"A": False, "B": True},
            "eqn": "A.B",
            "expected": False,
            "num_true_parts": 0,
            "error": False
        },
        {
            "variables": {"A": True, "B": False},
            "eqn": "A.!B",
            "expected": True,
            "num_true_parts": 1,
            "error": False
        },
        {
            "variables": {"A": True, "B": False, "C": False},
            "eqn": "A.B + C",
            "expected": False,
            "num_true_parts": 0,
            "error": False
        },
        {
            "variables": {"A": True, "B": False, "C": True},
            "eqn": "A.B + C",
            "expected": True,
            "num_true_parts": 1,
            "error": False
        },
        {
            "variables": {"A": True, "B": False, "C": True},
            "eqn": "A.B + !C",
            "expected": False,
            "num_true_parts": 0,
            "error": False
        },
        {
            "variables": {"A": True, "B": False, "C": False},
            "eqn": "A.B + !C",
            "expected": True,
            "num_true_parts": 1,
            "error": False
        },
        {
            "variables": {"A": True, "B": True, "C": False},
            "eqn": "A.B + !C",
            "expected": True,
            "num_true_parts": 2,
            "error": False
        },        
        {
            "variables": {"A": True, "B": True, "C": True},
            "eqn": "A.B + !C",
            "expected": True,
            "num_true_parts": 1,
            "error": False
        },
        {
            "variables": {"A": True, "B": True},
            "eqn": "A.B + !C",
            "expected": False,
            "num_true_parts": 0,
            "error": True
        }
    ]

    for test_case in test_cases:
        result, num_true_parts, err = calc(test_case["eqn"], test_case["variables"])

        s = f"{test_case['eqn']}: {test_case['variables']}"
        assert result == test_case["expected"], f"Expected {test_case['expected']}, got {result} for {s}"
    
        assert num_true_parts == test_case["num_true_parts"], f"Expected {test_case['num_true_parts']}, got {num_true_parts} for {s}"

        if test_case['error']:
            assert err is not None, f"Expected error, got {err} for {s}"
        else:
            assert err is None


if __name__ == '__main__':

    # Run the unit tests
    test_split_by_or()
    test_expand_pair()
    test_split_terms()
    test_expand_part()
    
    test_expand()
    #test_calc()
