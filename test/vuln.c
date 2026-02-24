
#include <string.h>
void func(char *str) {
    char buffer[10];
    strcpy(buffer, str); // Buffer overflow
}
