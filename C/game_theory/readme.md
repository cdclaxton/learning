# Game theory experiment

Each **game** consists of a given number of **rounds**. In each round, a player choses an **action**, which can be **cooperate** or **defect**.

In a **tournament**, the different strategies compete against each other and themselves. Each pairing of strategies play against each other in a single game.

## Build

```bash
# Run the tests
make test

# Run the tests and executables with Valgrind to detect memory leaks
make leak

# Build the executable
make build

# Clean (remove executables)
make clean
```

## Run the experiment

```bash
make build
./experiment
```