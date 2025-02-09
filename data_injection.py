from dao.productDAO import ProductDAO
from dao.userDAO import UserDAO



def inject_sample_products():
    productDAO = ProductDAO()

    # Sample data for products (excluding image paths, which will be read as BLOBs)
    sample_products = [
        ("Next Gen Phaser", 80, "replica", None, None, None, None, None, None, "aluminum", "1/1", True, "Replica of the phaser blaster used on the set of Star Trek the Next Generation", "static/images/NextGenPhaser.jpg"),
        ("Original Series Sulu Model", 30, "Figurine", "Male", "No moving pieces", "not from Mirror-verse", None, None, None, None, None, None, "1/6 scale figurine of Lt. Sulu from Star Trek the original series", "static/images/OriginalSeriesSuluFigurine.jpg"),
        ("Live Long and Prosper tv series Spock Poster", 20, "Poster", None, None, None, "Spock", True, "18x24-inch", None, None, None, "18x24-inch Poster of widely beloved Star Trek character Spock", "static/images/Spock_Poster.png")
    ]

    conn = productDAO.conn
    c = conn.cursor()

    # Insert each sample product into the products table
    for product in sample_products:
        try:
            with open(product[13], 'rb') as img_file:
                img_blob = img_file.read()
            # Insert the product data into the table
            c.execute('''
                INSERT INTO products (productName, price, type, gender, movable, isMirror, character, hasColour, dimensions, material, scale, isLimited, description, image_blob)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (*product[:13], img_blob))  # product[:13] gives you the first 13 values

        except FileNotFoundError: # debugging statement for file not found error
            print(f"Error:  {product[13]} not found.")

    conn.commit()  # commit injection + print debugging statement
    print("Sample product data injected successfully.")


def inject_sample_users():
    userDAO = UserDAO()
    sample_users = [("John", "Doe", "John@gmail.com", "123", True),
                    ("Jane", "Doe", "Jane@gmail.com", "123", False),
    ]
    conn = userDAO.conn
    c = conn.cursor()
    for user in sample_users:
        c.execute('''
                INSERT INTO users (firstName, lastName, userEmail, userPassword, isManager)
                VALUES (?, ?, ?, ?, ?)
            ''', user)

    conn.commit() # debugging user injection statement
    print("Sample user data injected successfully.")

inject_sample_products()
inject_sample_users()