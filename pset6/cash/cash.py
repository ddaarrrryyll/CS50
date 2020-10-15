from cs50 import get_float

# initialise number of coins to 0
coins = 0

while True:
    # get change owed by customer
    change = get_float("Change owed:")
    if change > 0:
        break

# round change to cents
change = round(change * 100)

# number of quarters
while change >= 25:
    coins += 1
    change -= 25

# number of dimes
while change >= 10:
    coins += 1
    change -= 10

# number of nickels
while change >= 5:
    coins += 1
    change -= 5

# number of pennies
while change >= 1:
    coins += 1
    change -= 1

# prints minimum number of coins given back
print(coins)