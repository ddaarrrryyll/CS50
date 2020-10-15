from cs50 import get_string
import sys


def main():
    # 2 arguments check
    if len(sys.argv) != 2:
        print("Usage: python bleep.py dictionary")
        exit(1)

    # opening dictionary
    with open(sys.argv[1], "r") as dictionary:
        banned_words = [text.strip() for text in dictionary]

    # prompt user for message
    message = get_string("What message would you like to censor?\n")
    words = message.split()

    for word in words:
        # convert words to lowercase for easier detection
        lowercase_word = word.lower()
        length = len(word)

        # print '*' for each character in banned words
        if lowercase_word in banned_words:
            print(length * "*" + " ", end='')
        else:
            print(word + " ", end='')

    print("")


if __name__ == "__main__":
    main()
