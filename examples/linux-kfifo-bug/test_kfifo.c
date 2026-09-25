#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include "kfifo.h"

int main(void) {
    struct kfifo fifo;
    const unsigned int CAPACITY = 8;
    int ret;

    printf("[TEST] Initializing kfifo with capacity %u...\n", CAPACITY);
    ret = kfifo_alloc(&fifo, CAPACITY);
    assert(ret == 0);
    assert(kfifo_is_empty(&fifo) == true);
    assert(kfifo_len(&fifo) == 0);
    assert(kfifo_avail(&fifo) == CAPACITY);

    printf("[TEST] Filling buffer to full capacity...\n");
    for (unsigned int i = 0; i < CAPACITY; i++) {
        ret = kfifo_put(&fifo, (unsigned char)(i + 1));
        assert(ret == 0);
    }

    assert(kfifo_len(&fifo) == CAPACITY);
    assert(kfifo_avail(&fifo) == 0);

    /*
     * Boundary Verification:
     * When capacity (8 bytes) is reached, kfifo_is_full MUST return true,
     * and any subsequent kfifo_put MUST return -1 without overwriting data.
     */
    printf("[TEST] Asserting kfifo_is_full on full capacity...\n");
    if (!kfifo_is_full(&fifo)) {
        fprintf(stderr, "FAIL: kfifo_is_full(&fifo) returned false when %u bytes filled in %u-byte buffer!\n",
                kfifo_len(&fifo), CAPACITY);
        kfifo_free(&fifo);
        return 1;
    }

    printf("[TEST] Attempting write to full buffer (expecting rejection)...\n");
    ret = kfifo_put(&fifo, 0xEE);
    if (ret != -1) {
        fprintf(stderr, "FAIL: kfifo_put succeeded on full buffer (ret=%d), corrupting circular stream!\n", ret);
        kfifo_free(&fifo);
        return 1;
    }

    printf("[TEST] Verifying FIFO stream integrity...\n");
    for (unsigned int i = 0; i < CAPACITY; i++) {
        unsigned char val = 0;
        ret = kfifo_get(&fifo, &val);
        assert(ret == 0);
        if (val != (unsigned char)(i + 1)) {
            fprintf(stderr, "FAIL: Data corruption at offset %u (expected %u, got %u)\n",
                    i, i + 1, val);
            kfifo_free(&fifo);
            return 1;
        }
    }

    assert(kfifo_is_empty(&fifo) == true);
    kfifo_free(&fifo);

    printf("[PASS] All kfifo unit assertions passed cleanly.\n");
    return 0;
}
