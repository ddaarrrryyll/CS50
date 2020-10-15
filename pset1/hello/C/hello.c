#include <stdio.h>

int main(void) {
    char name[100];
    printf("What is your name?\n");
    fgets(name, 100, stdin);
    printf("Hello, %s", name);
    return 0;
}