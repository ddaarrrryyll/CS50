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
    print(x, y)
    if (sum(x) + sum(y)) % 10 == 0:
        return print(f"{num} is VALID")
    else:
        return print(f"{num} is INVALID")

valid(4003600000000014)
