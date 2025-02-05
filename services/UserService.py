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


# below is code from a previously scrapped userValidation Module however this caused significant issues in the late
# stages of project development, not removed as contains logic relating to signup so may be useful in later
# iteration of the project
"""
    def __init__(self, userValidation):
        # Create an instance of UserDAO to handle model data
        self.userDAO = userDAO([])  # Passing an empty list to UserDAO constructor
        self.userValidation = userValidation

    # Creating the login function
    def login(self):

        # Retrieve the list of all users from UserDAO
        userListToCheckAgainst = self.userDAO.getAllUsers()

        # Prompt the model for email and password input
        email = input("Enter your Email: ")
        password = input("Enter your password: ")

        # Flag to check if the model is found
        user_found = False

        # Iterate through the list of users to find a matching model
        for user in userListToCheckAgainst:
            if user.userEmail == email and user.userPassword == password:
                user_found = True
                if user.isManager:
                    print("Hello Manager, Welcome Back")
                else:
                    print("Hello Employee, Welcome Back")
                break  # Exit the loop once a model is found

        # If no matching model is found, display an error message
        if not user_found:
            print("Invalid username or password. Try again.")
            self.login()

    def signUp(self):
        firstName = input("Enter First Name: ")
        lastName = input("Enter Last Name: ")
        email = input("Enter Email: ")
        password = input("Enter Password: ")

        if self.userValidation.checkEmail(self.userDAO.getAllUsers(), email) and self.userValidation.checkPassword(password):
            userToCreate = User(firstName,lastName, email, pasword)
            self.userDAO.createUser(userToCreate)
            print(f"Hello {firstName} {lastName}, your account has been created successfully!")
            for user in self.userDAO.getAllUsers():
                print(user)
        else:
            print("Sign up failed. Please try again.")
            self.signUp()  # Recursive call if validation fails

"""
