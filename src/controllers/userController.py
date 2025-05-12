from src.models.userModel import UserModel

class UserController:
    """
    Controller for user-related operations.
    """
    def __init__(self, user_model: UserModel):
        """
        Initialize the UserController with a user model.
        :param user_model: An instance of UserModel.
        """
        self.user_model = user_model

    def create_user(self, username, password, full_name, user_type):
        """
        Create a new user.
        """
        self.user_model.create(username, password, full_name, user_type)

    def get_user_by_id(self, user_id):
        """
        Retrieve a user by ID.
        """
        return self.user_model.get_by_id(user_id)

    def get_user_by_username(self, username):
        """
        Retrieve a user by username.
        """
        return self.user_model.get_by_username(username)

    def get_all_users(self):
        """
        Retrieve all users.
        """
        return self.user_model.get_all()

    def update_user(self, user_id, data):
        """
        Update user information.
        """
        self.user_model.update(user_id, data)

    def delete_user(self, user_id):
        """
        Delete a user by ID.
        """
        self.user_model.delete(user_id)

    def signup(self, username, password, full_name, user_type):
        """
        Register a new user if the username does not already exist.
        Returns True if successful, False if username exists.
        """
        if self.user_model.get_by_username(username):
            return False
        self.create_user(username, password, full_name, user_type)
        return True

    def signin(self, username, password):
        """
        Authenticate a user by username and password.
        Returns the user record if credentials are correct, else None.
        """
        user = self.user_model.get_by_username(username)
        if user and user[2] == password:  # Assuming password is at index 2
            return user
        return None