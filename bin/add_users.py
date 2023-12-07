"""script for import users to database"""
import csv
import sys

from repositories.sqlite_repo import SQLiteRepository

if len(sys.argv) != 3:
    print("usage: python -m bin.add_users CSV_FILE DB_FILE")

    raise Exception(f"Expected 2 argument but found {len(sys.argv)}")

repo = SQLiteRepository({"DB_NAME": sys.argv[2]})
repo.connect()

with open(sys.argv[1], encoding="utf8") as input_file:
    reader = csv.reader(input_file)

    for row in reader:
        user_id = repo.create_user(row[0], row[1])
        print(f"User with name {row[0]} surname {row[1]} created with ID {user_id}")
