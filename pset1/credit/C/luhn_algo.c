int valid(unsigned long long card) {
    // unsigned long long card = 4003600000000014ULL;
    // unsigned long long card = 378282246310005ULL;
    const unsigned long long number = card;
    int counter = 0;
    int x[8] = {};
    int y[8] = {};
    while (card > 0) {
        int digit = card % 10;
        if (counter % 2 == 0) {
            x[counter / 2] = digit;
            counter += 1;
        }
        else {
            int multiplied = digit * 2;
            if (multiplied >= 10) {
                y[counter / 2] = 1 + multiplied - 10;
            }
            else {
                y[counter / 2] = multiplied;
            }
            counter += 1;
        }
    card /= 10;
    }
    // printf("x = ");
    // for (int i = 0; i < 8; i++) {
    //     printf("%d", x[i]);
    //     if (i < 7) {
    //         printf(",");
    //     }
    //     else {
    //         printf("\n");
    //     }
    // }
    // printf("y = ");
    // for (int i = 0; i < 8; i++) {
    //     printf("%d", y[i]);
    //     if (i < 7) {
    //         printf(",");
    //     }
    //     else {
    //         printf("\n");
    //     }
    // }
    int sum = 0;
    for (int i = 0; i < 8; i++) {
        sum = sum + x[i] + y[i];
        // printf("%d\n", sum);
    }
    if (sum % 10 == 0) {
        // printf("%llu is VALID\n", number);
        return 0;
    }
    else {
        // printf("%llu is INVALID\n", number);
        return 1;
    }

    return 1;
}

void name(unsigned long long card, int* add_count, int* add_digits) {
    int count = 0;
    while (card >= 100) {
        card /= 10;
        count += 1;
    }
    count += 2;
    *add_count = count;
    *add_digits = card;
}