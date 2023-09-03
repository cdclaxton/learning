# Build a truth table given an arbitrary number of inputs.

def build_table(num_inputs):
    """Build a truth table with num_inputs inputs."""

    assert num_inputs > 0

    num_rows = 2**num_inputs
    rows = []

    for comb in range(num_rows):
        row = [1 * (((comb >> i) & 1) > 0) for i in range(num_inputs-1, -1, -1)]
        rows.append(row)

    return rows


if __name__ == '__main__':

    table = build_table(num_inputs=3)
    for row in table:
        print(row)