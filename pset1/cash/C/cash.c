#include <stdio.h>
#include <math.h>
int main(void)
{
    int coins = 0;
    //prompts user for change owed as x and makes sure it is positive
    float x;
    do
    {
        printf("Change Owed: ");
        scanf("%f", &x);
    }
    while(x < 0.00);

    //amounts x to cents by multiplying by 100
    x = round(x * 100);
    //quarters
    while(x >= 25)
    {
        coins += 1;
        x -= 25;
    }
    //dimes
    while(x >= 10)
    {
        coins += 1;
        x -= 10;
    }
    //nickels
    while(x >= 5)
    {
        coins += 1;
        x -= 5;
    }
    //pennies
    while(x >= 1)
    {
        coins += 1;
        x -= 1;
    }
    //prints minimum number of coins given back
    printf("%d\n", coins);
    return 0;
}
