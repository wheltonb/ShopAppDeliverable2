import sqlite3

def initialize_database():
    # establishes connection to shop.db
    conn = sqlite3.connect('shop.db')
    c = conn.cursor()

    # Create the products table if it doesn't already exist
    c.execute('''
    CREATE TABLE IF NOT EXISTS products (
        productID INTEGER PRIMARY KEY AUTOINCREMENT,
        productName TEXT NOT NULL,
        price REAL NOT NULL,
        type TEXT,
        gender TEXT,
        movable BOOLEAN,
        isMirror BOOLEAN,
        character TEXT,
        hasColour BOOLEAN,
        dimensions TEXT,
        material TEXT,
        scale TEXT,
        isLimited BOOLEAN,
        description TEXT,
        image_blob BLOB
    )
    ''')

    # Create the users table if it doesn't already exist
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        userID INTEGER PRIMARY KEY AUTOINCREMENT,
        firstName TEXT NOT NULL,
        lastName TEXT NOT NULL,
        userEmail TEXT NOT NULL,
        userPassword TEXT NOT NULL,
        isManager BOOLEAN
    )
    ''')

    conn.commit()
    conn.close()
    print('Database initialized.')
# debug statement on function call to initialize the database
if __name__ == '__main__':
    initialize_database()
