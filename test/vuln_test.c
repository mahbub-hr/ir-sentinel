
    #include <stdlib.h>
    void* allocate_array(int num_elements) {
        size_t size = num_elements * sizeof(int);
        return malloc(size);
    }
    