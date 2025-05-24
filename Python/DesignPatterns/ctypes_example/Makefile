CC=gcc
CFLAGS=-I -Wall

.PHONY: clean build

clean:
	rm -f libsum.so

build:
	$(CC) $(CFLAGS) -fPIC -shared -o libsum.so sum.c