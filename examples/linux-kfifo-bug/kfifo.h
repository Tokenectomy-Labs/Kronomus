#ifndef LINUX_KFIFO_H
#define LINUX_KFIFO_H

#include <stddef.h>
#include <stdbool.h>

/*
 * Kernel-style lockless circular buffer (kfifo)
 * Buffers are sized as powers of two to allow bitwise masking
 * instead of expensive modulo division.
 */
struct kfifo {
    unsigned char *buffer;
    unsigned int size;  /* Buffer capacity (must be power of 2) */
    unsigned int in;    /* Data added / write pointer */
    unsigned int out;   /* Data extracted / read pointer */
};

int kfifo_alloc(struct kfifo *fifo, unsigned int size);
void kfifo_free(struct kfifo *fifo);
unsigned int kfifo_len(const struct kfifo *fifo);
unsigned int kfifo_avail(const struct kfifo *fifo);
bool kfifo_is_empty(const struct kfifo *fifo);
bool kfifo_is_full(const struct kfifo *fifo);
int kfifo_put(struct kfifo *fifo, unsigned char val);
int kfifo_get(struct kfifo *fifo, unsigned char *val);

#endif /* LINUX_KFIFO_H */
