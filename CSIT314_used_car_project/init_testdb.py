import sqlite3
from faker import Faker
import random

# Initialize Faker and connect to the database
faker = Faker()
connection = sqlite3.connect('used_car.db')
cursor = connection.cursor()

# Generate 100 users across roles
user_roles = ['admin', 'agent', 'buyer', 'seller']
for role in user_roles:
    profile_id = cursor.execute('SELECT profile_id FROM user_profiles WHERE role = ?', (role,)).fetchone()[0]
    for _ in range(25):  # 25 users per role to total 100 users
        cursor.execute('''
            INSERT INTO user_accounts (id, name, password, email, profile_id, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            faker.user_name(),
            faker.name(),
            'password',
            faker.email(),
            profile_id,
            random.choice(['active', 'suspended'])
        ))

car_brands = [
    "Toyota", "Honda", "Ford", "Chevrolet", "Nissan",
    "BMW", "Mercedes-Benz", "Volkswagen", "Hyundai", "Audi",
    "Kia", "Mazda", "Subaru", "Jeep", "Porsche",
    "Lexus", "Buick", "Chrysler", "Dodge", "Ram"
]
# Generate 100 used car records linked to agents
agent_ids = [row[0] for row in cursor.execute("SELECT id FROM user_accounts WHERE profile_id = (SELECT profile_id FROM user_profiles WHERE role = 'agent')").fetchall()]
seller_ids = [row[0] for row in cursor.execute("SELECT id FROM user_accounts WHERE profile_id = (SELECT profile_id FROM user_profiles WHERE role = 'seller')").fetchall()]
for _ in range(100):
    cursor.execute('''
        INSERT INTO used_cars (make, model, year, price, description, view_count, seller_id, agent_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        random.choice(car_brands),  # make
        faker.word().capitalize(),  # model
        random.randint(1990, 2023),  # year
        round(random.uniform(5000, 30000), 2),  # price
        faker.text(max_nb_chars=100),  # description
        random.randint(0, 50),  # view count
        random.choice(seller_ids),  # seller_id (could be improved by adding seller accounts)
        random.choice(agent_ids)  # agent_id
    ))

# Generate 100 reviews with random ratings and text for agents
for _ in range(100):
    cursor.execute('''
        INSERT INTO reviews (agent_id, user_id, rating, review)
        VALUES (?, ?, ?, ?)
    ''', (
        random.choice(agent_ids),  # agent_id
        random.choice(buyer_ids + agent_ids),  # user_id (buyers and sellers can leave reviews)
        random.randint(1, 5),  # rating
        faker.sentence(nb_words=20)  # review text
    ))

# Commit and close
connection.commit()
connection.close()
print("Test data generated successfully.")
