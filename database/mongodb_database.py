"""
Gives a mongoDB Atlas database
"""

from pymongo.database import Database
from pymongo.mongo_client import MongoClient


class MongoDBDatabase:
    """
    Initialize a mongodb database.
    :param:  client: MongoClient - mongodb client.
    :param:  database_name: str - database name.
    :return: None.
    :rtype: none.
    """

    def __init__(self, client: MongoClient, database_name: str) -> None:
        self.__client: MongoClient = client
        self.__database_name: str = database_name
        self.__database: Database = self.__client[self.__database_name]

    @property
    def database(self) -> Database:
        """Getter method for accessing the database attribute.
        Returns:
            The current value of the database attribute.
        """
        return self.__database
