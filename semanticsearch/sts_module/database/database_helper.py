"""
Script contains DatabaseHelper Class used for accessing common functions to setup
and obtain information from the database.
"""
from typing import List
import numpy
from pandas import DataFrame
from .mongo_db_interface import MongoDBDatabase




class DatabaseHelper:
    """
    Static Class containing Static Methods for common interactions with the database
    """
    @classmethod
    def setup_database(cls, database: MongoDBDatabase, csv_folder_path: str,
                                                       csv_encoding: str) -> None:
        """
        Method sets up Inital data for Mongo DB Database by loading a CSV collection of 
        courses data. The method sources "The Best Data Science Courses - Udemy" dataset
        for the MongoDB Database Server.This will be used as the prop and test data for 
        building, testing and evaluating the Semantic Search Module.

        Args:
            database (MongoDBDatabase): Database Object creating/connecting to the new 
                                        Database and Collection inside the MongoDB Server.
            csv_folder_path (str): Folder Path of CSV files
            csv_encoding (str): encoding of csv file
        """
        # establish connection to database
        database.connect(create=True)

        #load csv data to collection
        database.load_csvs_to_database(csv_folder_path=csv_folder_path, encoding=csv_encoding)
        database.close()

    @classmethod
    def load_collection_data_dataframe(cls, database: MongoDBDatabase) -> DataFrame:
        """
        Method returns collection data in database as a pandas.Dataframe
        Args:
            database (MongoDBDatabase): Database Object connecting to a Database and
                                        Collection inside the MongoDB Server.
        Returns:
            pandas.Dataframe: Dataframe Object containing all data from the pointed collection
                (in the connection string)
        """
        # establish connection to database
        database.connect()
        # print a dataframe representing the data stored in a collection
        data: DataFrame = database.collection_to_dataframe()
        database.close()
        return data
    @classmethod
    def load_collection_data_json(cls, database: MongoDBDatabase) -> list:
        """
        Method returns collection data in database as a list of json (dict)
        Args:
            database (MongoDBDatabase): Database Object connecting to a Database and
                                        Collection inside the MongoDB Server.
        Returns:
            List[dict]: List of Json Objects containing all data from the pointed collection
                    (in the connection string)
        """
        # establish connection to database
        database.connect()
        # print a dataframe representing the data stored in a collection
        data: List[dict] =  database.collection_to_json()
        database.close()
        return data

    @classmethod
    def store_embedded_dataset(cls, database: MongoDBDatabase, dataset: numpy.ndarray) -> None:
        """
        Method stores the embedded dataset into the database.

        Args:
            database (MongoDBDatabase): Database Object creating/connecting to the new 
                                        Database and Collection inside the MongoDB Server.
            dataset (numpy.ndarray): Ndarray Object containing the embedded dataset data
        """
        # establish connection to database
        database.connect(create=True)
        #convert ndarray to dataframe (in a format to be able to store in MongoDB)
        dataframe = DataFrame(dataset)
        #load dataframe to database
        database.load_dataframe_to_database(dataframe, replace=True)
        database.close()
