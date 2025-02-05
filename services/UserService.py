from dao import userDAO
from models import User
# Creating a service layer for the model class this will handle business logic related to model

from dao.userDAO import UserDAO
from models.User import User


class UserService:
    def __init__(self):
        self.userDAO = UserDAO()
        self.users = self.userDAO.getAllUsers()

    def verifyUser(self, email, password):
        # Fetch user by email
        for user in self.users:
            if user.userEmail == email and user.userPassword == password:
                return user
        return None

