from src.models.baseModel import BaseModel
from src.db.strategies import DatabaseStrategy

class UserModel(BaseModel):
    """
    Model for user operations using the database context (strategy pattern).
    """
    def __init__(self, db_strategy: DatabaseStrategy):
        """
        Initialize the UserModel with a database context.
        :param db_context: An instance of DatabaseContext.
        """
        self.db = db_strategy
        self.db.connect()
        self.placeholder = "%s" if self.db.type == "mysql" else "?"
        

    def create(self, username, password, full_name, faculty, class_, user_type):
        """
        Create a new user.
        """
        query = f"""
            INSERT INTO users (username, password, full_name, faculty, class, user_type)
            VALUES ({self.placeholder}, {self.placeholder}, {self.placeholder}, {self.placeholder}, {self.placeholder}, {self.placeholder})
        """
        params = (username, password, full_name,faculty, class_, user_type)
        self.db.execute(query, params)
        self.db.commit()

    def get_by_id(self, user_id):
        """
        Get a user by ID.
        """
        query = f"SELECT * FROM users WHERE id = {self.placeholder}"
        self.db.execute(query, (user_id,))
        return self.db.fetchone()

    def get_by_username(self, username):
        """
        Get a user by username.
        """
        query = f"SELECT id, username, password, full_name, user_type, faculty, class FROM users WHERE username = {self.placeholder}"
        self.db.execute(query, (username,))
        return self.db.fetchone()

    def get_all(self):
        """
        Get all users.
        """
        query = "SELECT * FROM users"
        self.db.execute(query)
        return self.db.fetchall()

    def update(self, user_id, data):
        """
        Update user information.
        """
        fields = []
        params = []
        for key, value in data.items():
            fields.append(f"{key} = {self.placeholder}")
            params.append(value)
        params.append(user_id)
        query = f"UPDATE users SET {', '.join(fields)} WHERE id = {self.placeholder}"
        self.db.execute(query, tuple(params))
        self.db.commit()

    def delete(self, user_id):
        """
        Delete a user by ID.
        """
        query = f"DELETE FROM users WHERE id = {self.placeholder}"
        self.db.execute(query, (user_id,))
        self.db.commit()