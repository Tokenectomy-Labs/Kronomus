CC = gcc
CFLAGS = -Wall -Wextra -O2 -g

all: test_kfifo

kfifo.o: kfifo.c kfifo.h
	$(CC) $(CFLAGS) -c kfifo.c -o kfifo.o

test_kfifo: test_kfifo.c kfifo.o
	$(CC) $(CFLAGS) test_kfifo.c kfifo.o -o test_kfifo

test: test_kfifo
	./test_kfifo

clean:
	rm -f *.o test_kfifo

.PHONY: all test clean
