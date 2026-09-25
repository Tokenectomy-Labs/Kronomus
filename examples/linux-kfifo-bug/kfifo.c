#include <stdlib.h>
#include <string.h>
#include "kfifo.h"

static bool is_power_of_2(unsigned int n) {
    return (n != 0) && ((n & (n - 1)) == 0);
}

int kfifo_alloc(struct kfifo *fifo, unsigned int size) {
    if (!fifo || !is_power_of_2(size)) {
        return -1;
    }
    fifo->buffer = (unsigned char *)malloc(size);
    if (!fifo->buffer) {
        return -1;
    }
    fifo->size = size;
    fifo->in = 0;
    fifo->out = 0;
    return 0;
}

void kfifo_free(struct kfifo *fifo) {
    if (fifo && fifo->buffer) {
        free(fifo->buffer);
        fifo->buffer = NULL;
        fifo->size = 0;
        fifo->in = 0;
        fifo->out = 0;
    }
}

unsigned int kfifo_len(const struct kfifo *fifo) {
    if (!fifo) return 0;
    return fifo->in - fifo->out;
}

unsigned int kfifo_avail(const struct kfifo *fifo) {
    if (!fifo) return 0;
    return fifo->size - kfifo_len(fifo);
}

bool kfifo_is_empty(const struct kfifo *fifo) {
    if (!fifo) return true;
    return fifo->in == fifo->out;
}

/*
 * Checks whether the buffer has reached maximum capacity.
 * BUG: Uses strict greater-than (>) instead of greater-than-or-equal (>=),
 * causing full capacity (in - out == size) to be reported as NOT full.
 */
bool kfifo_is_full(const struct kfifo *fifo) {
    if (!fifo) return false;
    return (fifo->in - fifo->out) > fifo->size;
}

int kfifo_put(struct kfifo *fifo, unsigned char val) {
    if (!fifo || kfifo_is_full(fifo)) {
        return -1;
    }

    fifo->buffer[fifo->in & (fifo->size - 1)] = val;
    fifo->in++;
    return 0;
}

int kfifo_get(struct kfifo *fifo, unsigned char *val) {
    if (!fifo || !val || kfifo_is_empty(fifo)) {
        return -1;
    }

    *val = fifo->buffer[fifo->out & (fifo->size - 1)];
    fifo->out++;
    return 0;
}
