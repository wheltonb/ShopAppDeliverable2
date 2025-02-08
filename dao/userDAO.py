from models.User import User
import sqlite3
class UserDAO:
    def __init__(self):
        db_file = 'shop.db'
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def verify_user(self, email, password):
        print(f"Querying for Email: {email}, Password: {password}") # debug statement for query data
        # Modify the query to fetch a user by email and password
        sql = "SELECT * FROM users WHERE userEmail = ? AND userPassword = ?"
        self.cursor.execute(sql, (email, password))
        row = self.cursor.fetchone()  # Fetch one user matching the email and password
        if row:
            print(f"User found in database: {row}")
            self.conn.close()
            return User(userID=row[0], firstName=row[1], lastName=row[2], userEmail=row[3], userPassword=row[4], isManager=row[5])

        else:
            print("No matching user found in database")
            self.conn.close()
            return None



    # Create a new user
    def create_user(self, user):
        sql = '''
        INSERT INTO users (firstName, lastName, userEmail, userPassword, isManager)
        VALUES (?, ?, ?, ?, ?)
        '''
        self.cursor.execute(sql, (user.firstName, user.lastName, user.userEmail, user.userPassword, user.isManager))
        self.conn.commit()
        self.conn.close()
        return user

    # Retrieve a user by userID
    def get_user_by_id(self, userID):
        sql = 'SELECT * FROM users WHERE userID = ?'
        self.cursor.execute(sql, (userID,))
        row = self.cursor.fetchone()
        if row:
            return User(userID=row[0], firstName=row[1], lastName=row[2], userEmail=row[3], userPassword=row[4], isManager=row[5])
        self.conn.close()
        return None

    # Retrieve all users
    def get_all_users(self):
        sql = 'SELECT * FROM users'
        self.cursor.execute(sql)
        row = self.cursor.fetchall()
        if row:
            return User(*row)
        self.conn.close()
        return None

    # Update a user
    def update_user(self, user):
        sql = '''
        UPDATE users
        SET firstName = ?, lastName = ?, userEmail = ?, userPassword = ?, isManager = ?
        WHERE userID = ?
        '''
        self.cursor.execute(sql, (user.firstName, user.lastName, user.userEmail, user.userPassword, user.isManager, user.userID))
        self.conn.commit()
        self.conn.close()


    # Delete a user by userID
    def delete_user(self, userID):
        sql = 'DELETE FROM users WHERE userID = ?'
        self.cursor.execute(sql, (userID,))
        self.conn.commit()
        self.conn.close()