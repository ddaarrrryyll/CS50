# Get credit card number
card = int(input("Number: "))
number = card
# Validity check
def valid(num):
    # Reversed num
    rev_num = str(num)[::-1]
    # x is first digit of reversed num, y is second, x is third (...)
    x = []
    y = []
    for idx, val in enumerate(rev_num):
        # if x (idx=0/2/4/6 etc), don't do anything
        # if y (idx=1/3/5/7 etc), multiply by 2
        if idx % 2 == 1:
            multiplied = int(val) * 2
            if multiplied >= 10:
                y.append(1 + multiplied - 10)
            else:
                y.append(multiplied)
        else:
            x.append(int(val))
    if (sum(x) + sum(y)) % 10 == 0:
        return True
    else:
        return False

# Check card digits
count = 0
while card > 0:
    card = card//10
    count += 1

# Validity check 
# Count 15 = AmEx
if count == 15 and valid(number) and (str(number)[:2] == "34" or str(number)[:2] == "37"):
    print("AMEX")
# Count 16 = MasterCard
elif count == 16 and valid(number) and (str(number)[:2] == "51" or str(number)[:2] == "52" or str(number)[:2] == "53" or str(number)[:2] == "54" or str(number)[:2] == "55"):
    print("MASTERCARD")
# Count 13, 16 = Visa
elif (count == 16 or count == 13) and valid(number) and (str(number)[:1] == "4"):
    print("VISA")
else:
    print("INVALID")
