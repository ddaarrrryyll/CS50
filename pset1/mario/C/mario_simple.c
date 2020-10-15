#include <stdio.h>

int main(void) {
    
    // Height input
    int height;
    do {
        printf("Height: ");
        scanf("%d", &height);
    }
    while (height < 1 || height > 8);
    
    for (int i = 0; i < height; i ++) {

        // first row for height = 4 > "xxxy"
        // spaces = 4 - 0 - 1
        int spaces = height - i - 1;
        
        // hashes = 0 + 1
        int hashes = i + 1;

        // print spaces
        for (int j = 0; j < spaces; j ++) {
            printf(" ");
        }
        
        // print hashes
        for (int j = 0; j < hashes; j ++) {
            printf("#");
        }
        printf("\n");
    }
}