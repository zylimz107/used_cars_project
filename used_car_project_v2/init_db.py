import sqlite3

# Connect to the database
connection = sqlite3.connect('used_car.db')
cursor = connection.cursor()

# Create the user profiles table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_profiles (
        profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL UNIQUE,
        description TEXT NOT NULL,
        status TEXT NOT NULL CHECK(status IN ('active', 'suspended'))
    )
''')

# Create the user accounts table, linking each user to a profile role
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_accounts (
        id TEXT PRIMARY KEY,  -- Username
        name TEXT NOT NULL,
        password TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        profile_id INTEGER,
        status TEXT NOT NULL CHECK(status IN ('active', 'suspended')),
        FOREIGN KEY (profile_id) REFERENCES user_profiles (profile_id)
    )
''')

cursor.execute('''CREATE TABLE IF NOT EXISTS used_cars (
    car_id INTEGER PRIMARY KEY AUTOINCREMENT,
    make TEXT NOT NULL,
    model TEXT NOT NULL,
    year INTEGER NOT NULL,
    price REAL NOT NULL,
    description TEXT,
    view_count INTEGER DEFAULT 0,
    seller_id TEXT,
    agent_id TEXT NOT NULL,
    FOREIGN KEY (agent_id) REFERENCES user_accounts (id)
)
               ''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS shortlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    buyer_id TEXT,
    car_id INTEGER,
    FOREIGN KEY (buyer_id) REFERENCES user_accounts (id),
    FOREIGN KEY (car_id) REFERENCES cars (id),
    UNIQUE (buyer_id, car_id)  -- Composite unique constraint
)
''')


cursor.execute('''
CREATE TABLE IF NOT EXISTS reviews (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
    review TEXT,
    FOREIGN KEY (agent_id) REFERENCES user_accounts(id),
    FOREIGN KEY (user_id) REFERENCES user_accounts(id)
)
''')

# Optional: Insert default roles
cursor.executemany(
    'INSERT OR IGNORE INTO user_profiles (role, status, description) VALUES (?, ?, ?)',
    [
        ('admin', 'active', 'Administrator with full privileges'),
        ('agent', 'active', 'Agent responsible for managing car listings'),
        ('buyer', 'active', 'Buyer interested in purchasing used cars'),
        ('seller', 'active', 'Seller listing cars for sale')
    ]
)

cursor.execute('''
        INSERT INTO user_accounts (id, name, password, email, profile_id, status)
        VALUES (?, ?, ?, ?, 
                (SELECT profile_id FROM user_profiles WHERE role = 'admin' LIMIT 1), 
                ?)
    ''', ('admin1', 'Admin User', 'admin123', 'admin@example.com', 'active'))

# Commit and close
connection.commit()
connection.close()

