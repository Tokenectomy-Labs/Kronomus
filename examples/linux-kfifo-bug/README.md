# Linux Kernel Circular Buffer (`kfifo`) Boundary Bug Benchmark

This example demonstrates an authentic off-by-one boundary defect in a lockless circular buffer (`kfifo`), modeled after the Linux kernel's `include/linux/kfifo.h` subsystem.

## The Architectural Defect

The circular buffer relies on power-of-two capacity sizing and bitwise masking (`fifo->in & (fifo->size - 1)`) to avoid expensive hardware modulo operations during lockless interrupt handling.

In `kfifo.c`, `kfifo_is_full` checks capacity using a strict greater-than comparison:

```c
bool kfifo_is_full(const struct kfifo *fifo) {
    if (!fifo) return false;
    return (fifo->in - fifo->out) > fifo->size; // BUG: Should be >= fifo->size
}
```

When exactly `fifo->size` (8 bytes) are placed into the buffer:
- `in - out == size` evaluates to `8 > 8` (`false`).
- The buffer incorrectly reports that it is **not full**.
- A subsequent `kfifo_put` writes a 9th byte, lapping the read pointer and silently overwriting the oldest unread byte, causing fatal data corruption across the circular stream.

## Step 1: Reproduce the Defect

Run the test harness:

```bash
make test
```

### Observed Failure Output:

```text
gcc -Wall -Wextra -O2 -g -c kfifo.c -o kfifo.o
gcc -Wall -Wextra -O2 -g test_kfifo.c kfifo.o -o test_kfifo
./test_kfifo
[TEST] Initializing kfifo with capacity 8...
[TEST] Filling buffer to full capacity...
[TEST] Asserting kfifo_is_full on full capacity...
FAIL: kfifo_is_full(&fifo) returned false when 8 bytes filled in 8-byte buffer!
make: *** [Makefile:13: test] Error 1
```

## Step 2: Autonomous Remediation via Kronumos

From within this directory, engage Kronumos in autonomous TDD healing mode:

```bash
kronumos --fix
```

### Autonomous Execution Lifecycle:

1. **Auto-Detection**: Kronumos detects `Makefile` (`Make Project`) and sets `make test` as the verification harness.
2. **AST Diagnosis**: Kronumos inspects `kfifo.c` and `test_kfifo.c`, pinpointing the strict `>` vs `>=` boundary discrepancy.
3. **Atomic Patch**: Kronumos synthesizes a 1-line surgical diff using `apply_patch` (zero dirty diffs, zero compiler warnings on `-Wall -Wextra`).
4. **Closed-Loop Verification**: Kronumos re-executes `make test`, verifying that all assertions pass cleanly with exit code 0 in under 20 seconds.

```text
🎉 ────────────────────────────────────────────────────────────
✓ Fix Verified! All tests passed in round 4.
  📊 Verified Changes:
  M kfifo.c
──────────────────────────────────────────────────────────────
```
