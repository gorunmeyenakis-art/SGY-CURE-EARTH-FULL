#ifndef SECURE_MEMORY_H
#define SECURE_MEMORY_H
#include <stdio.h>
#include <stdlib.h>

static inline void* safe_malloc_array(size_t count, size_t element_size) {
    size_t total_bytes;
    if (__builtin_mul_overflow(count, element_size, &total_bytes)) {
        fprintf(stderr, "[GÜVENLİK İHLALİ] Bellek taşması engellendi!\n");
        return NULL;
    }
    void *ptr = malloc(total_bytes);
    if (!ptr) {
        fprintf(stderr, "[HATA] Yetersiz bellek!\n");
        return NULL;
    }
    return ptr;
}
#endif
