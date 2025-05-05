CC=gcc
CFLAGS=-I -Wall

.PHONY: build test clean

build:
	$(CC) $(CFLAGS) -o experiment main.c experiment.h experiment.c

clean:
	rm experiment test

test:
	$(CC) $(CFLAGS) -o test test.c experiment.h experiment.c && ./test

# Run tests and main program with memory leak check
leak:
	$(CC) $(CFLAGS) -O0 -O1 -o test test.c experiment.h experiment.c && valgrind --leak-check=yes ./test
	$(CC) $(CFLAGS) -O0 -O1 -o experiment main.c experiment.h experiment.c && valgrind --leak-check=yes ./experiment
