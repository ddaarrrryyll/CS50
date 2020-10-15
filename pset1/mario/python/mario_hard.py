# Get height
height = 0
while height < 1 or height > 8:
    height = int(input("Height: "))

for i in range(height):
    spaces = height - i - 1
    hashes = i + 1

    # Left side
    for j in range(spaces):
        print(" ", end = "")
    
    for j in range(hashes):
        print("#", end = "")
    
    # Middle
    print("  ", end = "")

    # Right side
    for j in range(hashes):
        print("#", end = "")
    print("")