# Imports
import itertools
import time


# Brute force function
def tryPassword(passwordSet, stringTypeSet):
    start = time.time()
    chars = stringTypeSet
    attempts = 0
    for i in range(1, 9):
        for letter in itertools.product(chars, repeat=i):
            attempts += 1
            letter = ''.join(letter)
            if letter == passwordSet:
                end = time.time()
                distance = end - start
                return (attempts, distance)


while True:

    password = input("Password:  ")
    if not password: break

    # Allowed characters
    # stringType = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ`~!@#$%^&*()_-+=[{]}|:;'\",<.>/?"
    stringType = "1234567890"
    # stringType = "abcdefghijklmnopqrstuvwxyz"
    tries, timeAmount = tryPassword(password, stringType)
    print("CyanCoding's BFPC cracked the password %s in %s tries and %s seconds!" % (password, tries, timeAmount))