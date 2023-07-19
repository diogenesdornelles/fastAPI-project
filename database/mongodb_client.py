"""
Create mongoDB Atlas client
"""
from typing import Union
from pymongo.mongo_client import MongoClient


class DatabaseConnectionError(Exception):
    """
    Exception to be raised if the connection fails
    :param: message - str
    """

    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)


class MongoDBClient:
    """
    Initialize connection with mongodb database.
    :param:  conn_string: str - database param to connection.
    :return: None.
    :rtype: none.
    """

    def __init__(self, conn_string: str) -> None:
        self.__conn_string: str = conn_string
        self.__client: Union[MongoClient, None] = self.__create_conn()
        if self.__client is None:
            raise DatabaseConnectionError("Failed to connect to the database.")

    @property
    def client(self):
        """Getter method for accessing the MongoClient instance.
        Returns:
            The current value of the client attribute.
        """
        return self.__client

    def __create_conn(self) -> Union[MongoClient, None]:
        """
        Return a MongoClient instance to initialize the database connection.
        :return: MongoClient instance or None.
        :rtype: MongoClient or None
        """
        client: MongoClient = MongoClient(self.__conn_string)
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
            return client
        except Exception as error:
            print(error)
            return None
