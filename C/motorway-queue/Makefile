CC=gcc
CFLAGS=-I -Wall

.PHONY: build test clean

build:
	$(CC) $(CFLAGS) -o simulation simulation.c simulation.h main.c

lib:
	$(CC) $(CFLAGS) -fPIC -shared -o libmotorway.so lib.c simulation.c simulation.h

clean:
	rm simulation test libmotorway.so

test:
	$(CC) $(CFLAGS) -o test test.c simulation.c simulation.h -lm && ./test

# Run tests and main program with memory leak check
leak:
	$(CC) $(CFLAGS) -O0 -O1 -o test test.c simulation.c simulation.h -lm && valgrind --leak-check=yes ./test