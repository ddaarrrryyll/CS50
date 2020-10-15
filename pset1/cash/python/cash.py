# Get change owed
while True:
    x = float(input("Change Owed: "))
    if x == 0:
        print(0)
    elif x < 0:
        continue
    else:
        break
# Convert x to cents
change = round(x * 100)
coins = 0

# Quarters
while change >= 25:
    coins += 1
    change -= 25

# Dimes
while change >= 10:
    coins += 1
    change -= 10

# Nickles
while change >= 5:
    coins += 1
    change -= 5

# Pennies
while change >= 1:
    coins += 1
    change -= 1

print(coins)