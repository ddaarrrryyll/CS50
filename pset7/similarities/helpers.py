from nltk.tokenize import sent_tokenize


# list(set(x).intersection(y)) to find the intersects between both inputs
# check for line similarity
def lines(a, b):
    """Return lines in both a and b"""

    # split a into lines using .split(\n)
    x = a.split('\n')
    # split b into lines using .split(\n)
    y = b.split('\n')
    # return a list of lines
    return list(set(x).intersection(y))


# check for sentence similarity
def sentences(a, b):
    """Return sentences in both a and b"""
    # split a into sentences using sent_tokenize
    x = sent_tokenize(a)
    # split b into sentences using sent_tokenize
    y = sent_tokenize(b)
    # return a list of sentence
    return list(set(x).intersection(y))


# check for substring similarity
def substrings(a, b, n):
    """Return substrings of length n in both a and b"""
    # split a into substrings
    x = [a[i:i+n] for i in range(len(a) - (n-1))]
    # split b into substrings
    y = [b[i:i+n] for i in range(len(b) - (n-1))]
    # return a list of substrings of length n
    return list(set(x).intersection(y))
