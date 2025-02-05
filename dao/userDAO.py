from models.User import User
import sqlite3

class UserDAO:
    def __init__(self, conn):
        self.conn = conn
        self.c = conn.cursor()

    # Create a new user
    def create_user(self, user):
        query = '''
        INSERT INTO users (firstName, lastName, userEmail, userPassword, isManager)
        VALUES (?, ?, ?, ?, ?)
        '''
        self.c.execute(query, (user.firstName, user.lastName, user.userEmail, user.userPassword, user.isManager))
        self.conn.commit()
        user.userID = self.c.lastrowid  # Set the userID after insertion
        return user

    # Retrieve a user by userID
    def get_user_by_id(self, userID):
        query = 'SELECT * FROM users WHERE userID = ?'
        self.c.execute(query, (userID,))
        row = self.c.fetchone()
        if row:
            return User(userID=row[0], firstName=row[1], lastName=row[2], userEmail=row[3], userPassword=row[4], isManager=row[5])
        return None

    # Retrieve all users
    def get_all_users(self):
        query = 'SELECT * FROM users'
        self.c.execute(query)
        rows = self.c.fetchall()
        users = []
        for row in rows:
            user = User(userID=row[0], firstName=row[1], lastName=row[2], userEmail=row[3], userPassword=row[4], isManager=row[5])
            users.append(user)
        return users

    # Update a user
    def update_user(self, user):
        query = '''
        UPDATE users
        SET firstName = ?, lastName = ?, userEmail = ?, userPassword = ?, isManager = ?
        WHERE userID = ?
        '''
        self.c.execute(query, (user.firstName, user.lastName, user.userEmail, user.userPassword, user.isManager, user.userID))
        self.conn.commit()
        return user

    # Delete a user by userID
    def delete_user(self, userID):
        query = 'DELETE FROM users WHERE userID = ?'
        self.c.execute(query, (userID,))
        self.conn.commit()
        return userID

    # Close the database connection (optional, but recommended)
    def close(self):
        self.conn.close()
