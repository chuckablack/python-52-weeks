from datetime import datetime
import hashlib
import sys

# search for password by reading file one password at a time
print("\n----- FINDING PASSWORDS: File read option")
while True:

    in_password = input("Input the password to search for: ")
    if not in_password:
        break

    start_time = datetime.now()
    with open("../../rockyou.conv.txt") as passwords_file:

        for index, password in enumerate(passwords_file):
            # print(f"checking: {index} {password.strip()} {in_password}")
            if in_password == password.strip():
                print(f"---> found it! password index: {index} in {(datetime.now()-start_time)}")
                break
        else:
            print(f"---> did not find password '{in_password}' in {(datetime.now()-start_time)}")

# search for password by reading file into dictionary, using that to match password
print("\n----- FINDING PASSWORDS: Dictionary option")

DEFAULT_NUM_PASSWORDS = 4000000
num_passwords_in = input(f"Number of passwords to add to dict ({DEFAULT_NUM_PASSWORDS})?  ")
if   not num_passwords_in:             num_passwords = DEFAULT_NUM_PASSWORDS
elif not num_passwords_in.isnumeric(): num_passwords = DEFAULT_NUM_PASSWORDS
else:                                  num_passwords = int(num_passwords_in)

passwords = dict()
with open("../../rockyou.conv.txt") as passwords_file:
    for index, password in enumerate(passwords_file):
        if index > num_passwords: break  # only do 4 million because of memory limitations on my VM

        sys.stdout.write("\r")
        sys.stdout.write(f" --- writing out entry: {index}")
        passwords[password.strip()] = {"index": index, "hash": hashlib.md5(password.strip().encode("utf-8"))}
print()

while True:

    in_password = input("Input the password to search for: ")
    if not in_password:
        break

    start_time = datetime.now()
    if in_password in passwords:
        print(f"---> found it! in {(datetime.now()-start_time)}")
        continue
    else:
        print(f"---> did not find password '{in_password}' in {(datetime.now()-start_time)}")


# search for password by matching with passwords in database
print("\n----- FINDING PASSWORDS: Database option")
from pymongo import MongoClient
client = MongoClient()
db = client.passdb

if not db.passwords.find_one({"clear": "fred"}):
    with open("../../rockyou.conv.txt") as passwords_file:
        for index, password in enumerate(passwords_file):
            sys.stdout.write("\r")
            sys.stdout.write(f" --- writing out entry: {index}, password: {password.strip()}")
            password_doc = {"clear": password.strip(), "hash": hashlib.md5(password.strip().encode("utf-8")).hexdigest()}
            db.passwords.insert_one(password_doc)
    print("\n--> indexing the collection")
    db.passwords.create_index("clear")

while True:

    in_password = input("Input the password to search for: ")
    if not in_password:
        break

    start_time = datetime.now()
    pw = db.passwords.find_one({"clear": in_password})
    if pw:
        print(f"---> found it! in {(datetime.now()-start_time)}")
        continue
    else:
        print(f"---> did not find password '{in_password}' in {(datetime.now()-start_time)}")

print()
