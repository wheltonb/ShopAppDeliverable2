class User:

    # Constructor to initalise the model class needs these parameters
    def __init__(self, firstName, lastName, userEmail, userPassword, isManager=None):

        self.firstName = firstName
        self.lastName = lastName
        self.userEmail = userEmail
        self.userPassword = userPassword
        # conditional statement for setting admin role
        if isManager is not None:
            self.isManager = isManager
        else:
            self.isManager = False

    def __str__(self):
        return f" I am  {self.firstName} {self.lastName} my email is {self.userEmail}"
