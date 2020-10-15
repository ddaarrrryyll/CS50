from cs50 import get_int

while True:
    # get pyramid height from user
    height = get_int("Height: ")
    if height >= 1 and height <= 8:
        break

for i in range(0, height):
    number_of_spaces = height - i
    number_of_hashes = i

    # print spaces
    for j in range(1, number_of_spaces):
        print(" ", end='')
        j += 1

    # print hashes
    for j in range(0, number_of_hashes + 1):
        print("#", end='')
        j += 1
    print()