# Build a truth table given an arbitrary number of inputs.


def build_table(num_inputs):
    """Build a truth table with num_inputs inputs."""

    assert num_inputs > 0

    num_rows = 2**num_inputs
    rows = []

    for comb in range(num_rows):
        row = [1 * (((comb >> i) & 1) > 0) for i in range(num_inputs - 1, -1, -1)]
        rows.append(row)

    return rows


def row_to_markdown(row, is_boolean=True):
    """Create a row in markdown format."""

    assert type(row) == list
    assert len(row) > 0

    if is_boolean:
        y = ["1" if xi == True else "0" for xi in row]
    else:
        y = [f"${xi}$" for xi in row]

    return "| " + " | ".join(y) + " |"


def make_separator(n):
    """Make a markdown table separator row."""

    assert type(n) == int
    assert n > 0

    row = ["--" for _ in range(n)]
    return "| " + " | ".join(row) + " |"


def markdown_table(inputs, outputs, input_names, output_names):
    """Returns a truth table in markdown format."""

    assert len(inputs) == len(outputs)

    rows = []

    # Make the header
    header = input_names[:]
    header.extend(output_names)
    rows.append(row_to_markdown(header, False))

    # Make the separator
    rows.append(make_separator(len(input_names) + len(output_names)))

    for idx in range(len(inputs)):
        boolean_row = inputs[idx][:]
        boolean_row.extend(outputs[idx])
        rows.append(row_to_markdown(boolean_row, True))

    return rows


def make_table(fns, input_names, output_names):
    """Make a truth table for a given list of functions."""

    assert type(fns) == list
    assert type(input_names) == list
    assert type(output_names) == list
    assert len(fns) == len(output_names)

    # Make the truth table
    rows = build_table(len(input_names))

    # Initialise the output table
    output = [[0 for _ in range(len(fns))] for _ in range(len(rows))]

    for fn_idx, fn in enumerate(fns):
        for row_idx, row in enumerate(rows):
            boolean_row = [xi == 1 for xi in row]
            output[row_idx][fn_idx] = fn(boolean_row)

    return markdown_table(rows, output, input_names, output_names)


if __name__ == "__main__":
    examples = [
        {
            "name": "Example 1",
            "input_names": ["A"],
            "fns": [lambda x: x[0], lambda x: not x[0]],
            "output_names": ["T_0", "T_1"],
            "equations": [
                r"T_0 = A",
                r"T_1 = \bar{A}",
            ],
        },
        {
            "name": "Example 2",
            "input_names": ["B", "A"],
            "fns": [lambda x: x[1] and not x[0], lambda x: x[0]],
            "output_names": [r"T_{low}", r"T_{high}"],
            "equations": [r"T_{low} = A \bar{B}", r"T_{high} = B"],
        },
        {
            "name": "Example 3",
            "input_names": ["C", "B", "A"],
            "fns": [
                lambda x: (x[2] and not x[0]) or (x[1] and not x[0]),
                lambda x: x[0],
            ],
            "output_names": [r"T_{low}", r"T_{high}"],
            "equations": [r"T_{low} = (A + B)\bar{C}", r"T_{high} = C"],
        },
        {
            "name": "Example 4",
            "input_names": ["D", "C", "B", "A"],
            "fns": [
                lambda x: (x[3] or x[2]) and not (x[1] or x[0]),
                lambda x: x[1] or x[0],
            ],
            "output_names": [r"T_{low}", r"T_{high}"],
            "equations": [
                r"T_{low} = (A + B) \overline{(C + D)} = (A + B) \bar{C} \bar{D}",
                r"T_{high} = C + D",
            ],
        },
        {
            "name": "Example 5",
            "input_names": ["C", "B", "A"],
            "fns": [
                lambda x: x[2] and not (x[1] or x[0]),
                lambda x: x[1] and not x[0],
                lambda x: x[0],
            ],
            "output_names": [r"T_{low}", r"T_{medium}", r"T_{high}"],
            "equations": [
                r"T_{low} = A \overline{(B + C)} = A \bar{B} \bar{C}",
                r"T_{medium} = B \bar{C}",
                r"T_{high} = C",
            ],
        },
        {
            "name": "Example 6",
            "input_names": ["F", "E", "D", "C", "B", "A"],
            "fns": [
                lambda x: (x[5] or x[4]) and not (x[3] or x[2] or x[1] or x[0]),
                lambda x: (x[3] or x[2]) and not (x[1] or x[0]),
                lambda x: x[1] or x[0],
            ],
            "output_names": [r"T_{low}", r"T_{medium}", r"T_{high}"],
            "equations": [
                r"T_{low} = (A + B) \overline{(C + D + E + F)} = (A + B) \bar{C} \bar{D} \bar{E} \bar{F}",
                r"T_{medium} = (C + D) \overline{(E + F)} = (C + D) \bar{E} \bar{F}",
                r"T_{high} = E + F",
            ],
        },
        {
            "name": "Example 7",
            "input_names": ["C", "B", "A"],
            "fns": [
                lambda x: (x[2] or x[1]) and not x[0],
                lambda x: (x[2] or x[1]) and x[0],
            ],
            "output_names": [r"T_{low}", r"T_{high}"],
            "equations": [r"T_{low} = (A + B) \bar{C}", r"T_{high} = (A + B) C"],
        },
        {
            "name": "Example 8",
            "input_names": ["D", "C", "B", "A"],
            "fns": [
                lambda x: (x[3] or x[2]) and not (x[1] or x[0]),
                lambda x: (x[3] or x[2]) and (x[1] or x[0]),
            ],
            "output_names": [r"T_{low}", r"T_{high}"],
            "equations": [
                r"T_{low} = (A + B) \overline{(C + D)} = (A + B) \bar{C} \bar{D}",
                r"T_{high} = (A + B) (C + D)",
            ],
        },
        {
            "name": "Example 9",
            "input_names": ["F", "E", "D", "C", "B", "A"],
            "fns": [
                lambda x: (x[5] or x[4]) and not (x[3] or x[2]) and not (x[1] or x[0]),
                lambda x: (x[3] or x[2]) and not (x[1] or x[0]),
                lambda x: (x[3] or x[2]) and (x[1] or x[0]),
            ],
            "output_names": ["D0", "D1", "D2"],
            "equations": [
                r"T_{low} = (A + B) \overline{(C + D)} \cdot \overline{(E + F)} = (A + B) \bar{C} \bar{D} \bar{E} \bar{F}",
                r"T_{medium} = (C + D) \overline{(E + F)} = (C + D) \bar{E} \bar{F}",
                r"T_{high} = (C + D)(E + F)",
            ],
        },
    ]

    for example in examples:
        print(f"## {example['name']}")
        result = make_table(
            example["fns"], example["input_names"], example["output_names"]
        )
        for row in result:
            print(row)

        print("\nEquations:")
        for eqn in example["equations"]:
            print(f"* ${eqn}$")

        print("\n")
