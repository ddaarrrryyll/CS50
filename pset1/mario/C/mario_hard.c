#include <stdio.h>

int main(void) {
    // Get height
    int height;
    do {
        printf("Height: ");
        scanf("%d", &height);
    }
    while (height < 1 || height > 8);

    // Each row
    for (int i = 0; i < height; i ++) {
        int spaces = height - i -1;
        int hashes = i + 1;

        // Left side
        for (int j = 0; j < spaces; j ++) {
            printf(" ");
        }

        for (int j = 0; j < hashes; j ++) {
            printf("#");
        }

        // Middle
        printf("  ");
        
        // Right side
        for (int j = 0; j < hashes; j ++) {
            printf("#");
        }
        printf("\n");
    }
}