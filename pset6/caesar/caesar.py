from cs50 import get_int
from cs50 import get_string
import sys


def main():
    if len(sys.argv) != 2:
        print("Usage: python caesar.py key")
        exit(1)


# getting key from argument
key = int(sys.argv[1])

# ask user for message to be encrypted
message = get_string("plaintext:")
print("ciphertext:", end='')

for i in range(len(message)):

    # converting uppercase letters
    if message[i].isupper():
        x = chr((ord(message[i]) - ord('A') + key) % 26 + ord('A'))
        print(x, end='')

    # converting lowercase letters
    elif message[i].islower():
        x = chr((ord(message[i]) - ord('a') + key) % 26 + ord('a'))
        print(x, end='')

    # special characters
    else:
        print(message[i], end='')

print('\n')

if __name__ == "__main__":
    main()