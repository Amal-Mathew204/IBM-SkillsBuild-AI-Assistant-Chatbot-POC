"""Files contains all exceptions for the database_server module"""

class ConnectionFailure(Exception):
    """Exception for failing to connect to the MongoDB Server"""
    def __init__(self):
        super(ConnectionFailure, self).__init__("Failed to Connect To MongoDB Server")

class NoConnection(Exception):
    """Exception for failing to connect to the MongoDB Server"""
    def __init__(self):
        super().__init__("Not Connected To The MongoDB Server")

class DoesNotExist(Exception):
    """Exception for reference items (any) not found"""
    def __init__(self, field: str, field_name: str):
        """
        Args:
            field (str): The type item that does not exist
            field_anem (str): The name of item (given) that does not exist
        """
        super(DoesNotExist, self).__init__(f"{field}: {field_name} does not exist")

class CSVsNotFound(Exception):
    """Exception for no csv files found in a given folder/file path"""
    def __init__(self, path: str):
        """
        Args:
            path (str): Folder/File path given to locate CSV
        """
        super(CSVsNotFound, self).__init__(f"No CSV Files Found in given path: {path}")

class EmptyCollection(Exception):
    """Exception when a collection is empty"""
    def __init__(self, database: str, collection: str):
        """
        Args:
            database (str): Database name of collection
            collection (str): Name of Empty Collection
        """
        super().__init__(f"{collection} Collection inside of {database} database is empty")
