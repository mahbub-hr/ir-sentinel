
#include <string.h>
void func(char *str) {
    char buffer[10];
    if (strlen(str) < 10) { // Safety check
        strcpy(buffer, str);
    }
}
