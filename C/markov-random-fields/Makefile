CC=gcc
CFLAGS=-I -Wall

.PHONY: test clean example1 example2 example3 example4

clean:
	rm -f test example1 example2 example3 example4

test:
	$(CC) $(CFLAGS) -o test test.c factor.h factor.c permutations.c permutations.h sum_product_utilities.c sum_product_utilities.h matrix.c matrix.h -lm && ./test

example1:
	$(CC) $(CFLAGS) -o example1 example1.c factor.h factor.c -lm && ./example1

example2:
	$(CC) $(CFLAGS) -o example2 example2.c -lm && ./example2 -0.1 2 1

example3:
	$(CC) $(CFLAGS) -o example3 example3.c -lm && ./example3

example4:
	$(CC) $(CFLAGS) -o example4 example4.c permutations.c permutations.h sum_product_utilities.c sum_product_utilities.h matrix.c matrix.h -lm && ./example4