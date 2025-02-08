from dao.userDAO import UserDAO
from models.User import User
import sqlite3

class UserService:
    def __init__(self):
        self.userDAO = UserDAO()

    def verify_user(self, email, password):
        user = self.userDAO.verify_user(email, password)  # Calls userDAO
        if user is not None:
            print(f"User found: {user.userEmail}")
            return user
        else:
            print("No matching user found")
            return None  # Return None if no matching user is found

    def create_user(self, user):
        return self.userDAO.create_user(user)

    def get_user_by_id(self, userID):
        return self.userDAO.get_user_by_id(userID)

    def get_all_users(self):
        return self.userDAO.get_all_users()

    def update_user(self, user):
        return self.userDAO.update_user(user)

    def delete_user(self, userID):
        return self.userDAO.delete_user(userID)



