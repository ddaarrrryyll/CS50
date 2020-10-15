# Get height
height = 0
while height < 1 or height > 8:
    height = int(input("Height:"))

for i in range(height):

    # first row if heigh = 4, "xxx#"
    # spaces = 4 - 0 - 1
    spaces = height - i - 1
    # hashes = 0 + 1
    hashes = i + 1

    # Print spaces
    for j in range(spaces):
        print(" ", end = "")
    
    # Print hashes
    for j in range(hashes):
        print("#", end = "")
    i += 1
    print("")