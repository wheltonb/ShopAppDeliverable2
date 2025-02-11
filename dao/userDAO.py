from models.User import User
import sqlite3
class UserDAO:
    def __init__(self):
        db_file = 'shop.db'
        self.conn = sqlite3.connect(db_file)

    def verify_user(self, email, password):
        sql = '''SELECT * FROM users WHERE userEmail = ? AND userPassword = ?'''
        cursor = self.conn.execute(sql, (email, password))
        row = cursor.fetchone()
        if row:
            return User(userID=row[0], firstName=row[1], lastName=row[2], userEmail=row[3], userPassword=row[4], isManager=row[5])
        self.conn.close()
        return None

    # Create a new user
    def create_user(self, user):
        sql = '''INSERT INTO users (firstName, lastName, userEmail, userPassword, isManager)
                 VALUES (?, ?, ?, ?, ?)'''
        self.conn.execute(sql, (user.firstName,user.lastName,user.userEmail,user.userPassword,user.isManager))
        self.conn.commit()
        self.conn.close()



    # Retrieve a user by userID
    def get_user_by_id(self, userID):
        sql = 'SELECT * FROM users WHERE userID = ?'
        cursor = self.conn.execute(sql, (userID,))
        row = cursor.fetchone()
        if row:
            return User(userID=row[0], firstName=row[1], lastName=row[2], userEmail=row[3], userPassword=row[4], isManager=row[5])
        self.conn.close()
        return None

    def get_user_by_email(self, email):
        sql = 'SELECT * FROM users WHERE userEmail = ?'
        cursor = self.conn.execute(sql, (email,))
        row = cursor.fetchone()
        if row:
            return User(userID=row[0], firstName=row[1], lastName=row[2], userEmail=row[3], userPassword=row[4], isManager=row[5])
        return None



    def get_all_users(self):
        sql = '''SELECT * FROM users '''
        cursor = self.conn.execute(sql)
        row = cursor.fetchall()
        users = []
        if row:
            for row in row:
                user = User(*row)  # Assuming the Product constructor takes the values in the row
                users.append(user)
        return users



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