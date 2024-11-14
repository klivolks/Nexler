import csv
import json
import random

from faker import Faker
from datetime import datetime

fake = Faker()


def fake_users(count=10):
    users = []
    for _ in range(count):
        user = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "date_of_birth": datetime(2000, 12, 30).strftime("%Y-%m-%d"),
            "phone": str(random.randint(1000000000, 9999999999)),
            "email": fake.email(),
            "password": fake.password(length=10)
        }
        users.append(user)
    return users


def write_csv():
    users = fake_users()
    # Write to a CSV file
    with open('users.csv', 'w', newline='') as csvfile:
        fieldnames = users[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(users)


def write_json():
    users = fake_users()
    # Write to a JSON file
    with open('users.json', 'w') as jsonfile:
        json.dump(users, jsonfile, indent=4)

