from dao.userDAO import UserDAO
from models.User import User
import sqlite3

class UserService:
    def __init__(self, conn):
        self.userDAO = UserDAO(conn)

    def verify_user(self, email, password):
        users = self.userDAO.get_all_users()
        for user in users:
            if user.userEmail == email and user.userPassword == password:
                return user
        return None

    def create_user(self, firstName, lastName, userEmail, userPassword, isManager):
        user = User(firstName=firstName, lastName=lastName, userEmail=userEmail, userPassword=userPassword, isManager=isManager)
        return self.userDAO.create_user(user)

    def get_user_by_id(self, userID):
        return self.userDAO.get_user_by_id(userID)

    def get_all_users(self):
        return self.userDAO.get_all_users()

    def update_user(self, userID, firstName, lastName, userEmail, userPassword, isManager):
        user = User(userID=userID, firstName=firstName, lastName=lastName, userEmail=userEmail, userPassword=userPassword, isManager=isManager)
        return self.userDAO.update_user(user)

    def delete_user(self, userID):
        return self.userDAO.delete_user(userID)



