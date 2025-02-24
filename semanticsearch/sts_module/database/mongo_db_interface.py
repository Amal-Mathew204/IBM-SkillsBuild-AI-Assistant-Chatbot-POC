"""
This script contains the code used to communicate with the MongoDB Sever 
Used to SetUp and Interact With the Databases on the Server
"""
import os
import json
from bson.json_util import dumps
import pandas
from pymongo import MongoClient
from pymongo import errors
from . import exceptions


class MongoDBDatabase:
    """
     A Class for communication with the Mongo DB Server
    
    Attributes:
        url (str): URL of the  Mongo DB server
        database (str): Target Database inside Server
        collection (str): Target Collection inside Database
    """
    def __init__(self, url: str, database: str, collection: str,
                 username: str, password: str, auth_mechanism: str):
        """
        Initalising method for the MongoDBDatabase Class

        Args:
            url (str): URL of the  Mongo DB server
            database (str): Target Database inside Server
            collection (str): Target Collection inside Database
            username (str): Username of the Database User
            password (str): Password of the Database User
            auth_mechanism (str): Authentication Mechanism used by the database
        """
        self.__url_name: str = url
        self.__database_name: str = database
        self.__collection_name: str = collection
        self.__collection = None
        self.__client: MongoClient = None
        self.__username: str = username
        self.__password: str = password
        self.__auth_mechanism = auth_mechanism


    @property
    def server_url(self) -> str:
        """str: URL of of the Mongo DB server"""
        return self.__url_name

    @property
    def database(self) -> str:
        """str: Target Database inside Server"""
        return self.__database_name

    @property
    def collection(self) -> str:
        """str: Target Collection inside Database"""
        return self.__collection_name


    def connect(self, create = False) -> None:
        """
        Connects to the Mongo DB Server

        Raises:
            ConnectionFailure: If Failure to Connect the MongoDB server with given URL
            DoesNotExist: If Database or Collection does not exist in MongoDB Server
        """
        try:
            self.__client = MongoClient(self.server_url,
                                        username=self.__username,
                                        password=self.__password,
                                        authMechanism=self.__auth_mechanism)
            self.__client.server_info()
        except errors.ServerSelectionTimeoutError as exception:
            self.__client = None
            raise exceptions.ConnectionFailure() from exception
        except errors.ConnectionFailure as exception:
            self.__client = None
            raise exceptions.ConnectionFailure() from exception

        if not create :
            database_list = self.__client.list_database_names()
            if self.database not in database_list:
                self.__client = None
                raise exceptions.DoesNotExist(field="Database", field_name=self.database)
        database = self.__client[self.database]
        if not create :
            collection_list = database.list_collection_names()
            if self.collection not in collection_list:
                self.__client = None
                raise exceptions.DoesNotExist(field="Collection", field_name=self.collection)
        self.__collection = database[self.collection]

    def is_connected(self) -> bool:
        """
        Method checks if there is a connection active to the Database

        Returns:
            boolean value
        """
        return self.__client is not None

    def close(self) -> None:
        """
        Method closes the Connection with the MongoDB Server
        """
        self.__client.close()
        self.__client = None

    def load_csvs_to_database(self, csv_folder_path: str, encoding: str) -> None:
        """
        Takes a folder path of CSVS to read and store into the database
            (location specified in connection string)
        Args:
            csv_folder_path (str): Folder Path of CSV files
            encoding (str): encoding of csv file
        Raises:
            NoConnection: Connection to database has not been established
            CSVsNotFound: No CSVs found in the path directory
            DoesNotExist: Directory does not exist
        """
        if os.path.isdir(csv_folder_path) is False:
            raise exceptions.DoesNotExist(field="Directory", field_name=csv_folder_path)

        if self.__client is None:
            raise exceptions.NoConnection

        csvs_count = 0
        for file in os.listdir(csv_folder_path):
            if file.endswith(".csv"):
                dataframe = pandas.read_csv(f"{csv_folder_path}/{file}", encoding=encoding)
                # return dataframe as a list of dictionaries
                data = dataframe.to_dict(orient='records')
                self.__collection.insert_many(data)
                csvs_count+=1
        if csvs_count == 0:
            raise exceptions.CSVsNotFound(path=csv_folder_path)

    def load_dataframe_to_database(self, dataframe: pandas.DataFrame,
                                            replace: bool = False) -> None:
        """
        Takes a Pandas Dataframe store into the database 
            (location specified in connection string)

        Args:
            dataframe (pandas.Dataframe): Dataframe consisting of data to store into the db
            replace (bool): Decides if method should delete all files currently in the 
            collection before inserting data
        """
        data: dict = json.loads(dataframe.to_json(orient="records"))
        if replace:
            #delete existing files in collection
            self.__collection.delete_many({})
        self.__collection.insert_many(data)

    def collection_to_dataframe(self) -> pandas.DataFrame:
        """
        The method takes the data stored in the pointed MongoDB collection and returns it
        in pandas.Dataframe format

        Returns:
            pandas.Dataframe

        Raises:
            NoConnection: Connection to database has not been established
            FilesNotFound: When data returned from collection is empty
        """
        if self.__client is None:
            raise exceptions.NoConnection
        data: list = list(self.__collection.find())
        if len(data) == 0:
            raise exceptions.EmptyCollection(self.database, self.collection)
        return pandas.DataFrame(data)
    def collection_to_json(self) -> list[dict]:
        """
        The method takes the data stored in the pointed MongoDB collection and returns it as
        a list of json (dict) form objects

        Returns:
            List[dict]
        Raises:
            NoConnection: Connection to database has not been established
            FilesNotFound: When data returned from collection is empty
        """
        if self.__client is None:
            raise exceptions.NoConnection
        data: list = list(self.__collection.find())
        if len(data) == 0:
            raise exceptions.EmptyCollection(self.database, self.collection)
        return json.loads(dumps(data))
