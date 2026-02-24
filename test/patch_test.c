
    #include <stdlib.h>
    #include <stdint.h>
    void* allocate_array(int num_elements) {
        if (num_elements < 0 || num_elements > 2147483647 / 4) {
            return NULL; 
        }
        size_t size = num_elements * sizeof(int);
        return malloc(size);
    }
    