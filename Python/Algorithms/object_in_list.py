# Ensure only unique objects are added to a list


class Cat:
    def __init__(self, name):
        self.name = name

    def __repr__(self) -> str:
        return f"Cat('{self.name}')"

    def __eq__(self, value: object) -> bool:
        return type(value) == Cat and value.name == self.name


if __name__ == "__main__":

    cats = [Cat("Bob"), Cat("Bob"), Cat("Kiki")]

    unique = []
    for c in cats:
        if c not in unique:
            unique.append(c)

    assert len(unique) == 2, f"Got: {unique}"
