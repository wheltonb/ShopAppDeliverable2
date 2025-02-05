from models.User import User
import sqlite3

# class to hold all users in memory, using this instead of database
class UserDAO:

    def __init__(self, user_list=None):
        # Initialize user_list as an empty list if None is provided
        self.user_list = user_list if user_list is not None else []

    # This method grabs all users, and creates some if the list is empty
    def getAllUsers(self):
        if not self.user_list:  # Check if the list is empty
            # Create default users if list is empty
            user_manager = User("John", "Doe", "John@gmail.com", "123", True)
            user_employee = User("Jane", "Doe", "Jane@gmail.com", "123", False)

            self.user_list.append(user_manager)
            self.user_list.append(user_employee)

        return self.user_list

    def getUserByEmail(self, email):
        for user in self.user_list:
            if user.userEmail == email:
                return user
        return None
    # Add a new model to the list
