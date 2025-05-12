class BaseModel:
    """
    Interface for models to interact with the database using a strategy pattern.
    """
    def __init__(self, db_context):
        self.db = db_context

    def create(self, data):
        """
        Insert a new record.
        """
        raise NotImplementedError

    def get_by_id(self, record_id):
        """
        Retrieve a record by its ID.
        """
        raise NotImplementedError

    def get_all(self):
        """
        Retrieve all records.
        """
        raise NotImplementedError

    def update(self, record_id, data):
        """
        Update a record by its ID.
        """
        raise NotImplementedError

    def delete(self, record_id):
        """
        Delete a record by its ID.
        """
        raise NotImplementedError