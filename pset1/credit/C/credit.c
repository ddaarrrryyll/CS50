#include <stdio.h>

int valid(unsigned long long card);
void name(unsigned long long card, int* add_count, int* add_digits);

int main(void){
    // unsigned long long card = 4003600000000014ULL;
    // get card number
    unsigned long long card;
    // LACKING ERROR CHECKING
    printf("Number: ");
    scanf("%llu", &card);

    int count, digits;
    name(card, &count, &digits);
    if (valid(card) == 0) {
        // count 15 = AMEX
        if (count == 15 && (digits == 34 || digits == 37)){
            printf("AMEX\n");
        }
        // count 16 = MASTERCARD
        else if (count == 16 && (digits == 51 || digits == 52 || digits == 53 || digits == 54 || digits == 55)) {
            printf("MASTERCARD\n");
        }
        // count 13, 16 = VISA
        else if ((count == 16 || count == 13) && digits >= 40 && digits < 50) {
            printf("VISA\n");
        }
        else {
            printf("INVALID\n");
        }
    }
    else {
        printf("INVALID\n");
    }
    return 0;
}

// VALIDITY CHECK
int valid(unsigned long long card) {

    const unsigned long long number = card;
    int counter = 0;
    int x[8] = {};
    int y[8] = {};
    while (card > 0) {
        int digit = card % 10;
        // if x , don't do anything
        // if y , multiply by 2
        if (counter % 2 == 0) {
            x[counter / 2] = digit;
            counter += 1;
        }
        else {
            int multiplied = digit * 2;
            // if > 10, split digits and add
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

    int sum = 0;
    for (int i = 0; i < 8; i++) {
        sum = sum + x[i] + y[i];
    }
    if (sum % 10 == 0) {
        // VALID if sum ends with 0
        return 0;
    }
    else {
        // else INVALID
        return 1;
    }

    return 1;
}

// CHECK FOR CARD COMPANY NAME
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
