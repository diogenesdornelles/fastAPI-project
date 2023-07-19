"""
Initialize mongodb database collections.
"""
from typing import List
from pymongo.collection import Collection
from pymongo.database import Database
from schemas import \
    create_clients_collection,\
    create_products_collection,\
    create_orders_collection,\
    create_users_collection


class MongoDBCollections:
    """
    Initialize mongodb database collections.
    :param:  conn_string: str - database param to connection.
    :param:  database_name: List - collections names.
    :return: None.
    :rtype: none.
    """

    def __init__(self, database: Database) -> None:
        self.__database = database
        self.__collections_names_created: List[str] = self.__database.list_collection_names()
        self.__clients_collection = self.__set_collection_clients()
        self.__products_collection = self.__set_collection_products()
        self.__orders_collection = self.__set_collection_orders()
        self.__users_collection = self.__set_collection_users()

    @property
    def clients(self):
        """Getter method for accessing the clients' collection.
        Returns:
            The current value of the clients collection attribute.
        """
        return self.__clients_collection

    @property
    def products(self):
        """Getter method for accessing the products' collection.
        Returns:
            The current value of the products collection attribute.
        """
        return self.__products_collection

    @property
    def orders(self):
        """Getter method for accessing the orders' collection.
        Returns:
            The current value of the orders collection attribute.
        """
        return self.__orders_collection

    @property
    def users(self):
        """Getter method for accessing the users' collection.
        Returns:
            The current value of the users collection attribute.
        """
        return self.__users_collection

    def __set_collection_clients(self) -> Collection:
        """Private method for setting collections.
            Returns: None
        """
        if 'clients' not in self.__collections_names_created:
            try:
                clients = create_clients_collection(self.__database)
                return clients
            except Exception as error:
                print(error)
        else:
            return self.__database['clients']

    def __set_collection_products(self) -> Collection:
        """Private method for setting collections.
        Returns: None
        """
        if 'products' not in self.__collections_names_created:
            try:
                products = create_products_collection(self.__database)
                return products
            except Exception as error:
                print(error)
        else:
            return self.__database['products']

    def __set_collection_orders(self) -> Collection:
        """Private method for setting collections.
        Returns: None
        """
        if 'orders' not in self.__collections_names_created:
            try:
                orders = create_orders_collection(self.__database)
                return orders
            except Exception as error:
                print(error)
        else:
            return self.__database['orders']

    def __set_collection_users(self) -> Collection:
        """Private method for setting collections.
            Returns: None
        """
        if 'users' not in self.__collections_names_created:
            try:
                users = create_users_collection(self.__database)
                return users
            except Exception as error:
                print(error)
        else:
            return self.__database['users']
