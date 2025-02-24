"""
Python Script for Setting Up the Semantic Search Module
- The Script will create and store (on the applications DB) the courses embedded dataset
"""
from logger import ModuleLogger #pylint: disable=relative-beyond-top-level
from sts_module.database.mongo_db_interface import MongoDBDatabase
from sts_module.embedding_module.controller import EmbeddingController


def database_setup_embedded_database(url: str, username: str, password: str,
                                     database_auth_mechanism: str, database_name: str,
                                     courses_collection_name: str,
                                     embedded_dataset_collection_name: str):
    """
    Method creates an embedded dataset and store the embedded dataset onto the applications database

    Args:
        url (str): URL of the  Mongo DB server
        username (str): Username of the Database User
        password (str): Password of the Database User
        database_auth_mechanism (str): Authentication Mechanism used by the database
        database_name (str): Application Database inside Server
        courses_collection_name (str): Courses Collection inside Database
        embedded_dataset_collection_name (str): Embedded Dataset Collection inside Database

    """
    #intialise logger
    logger = ModuleLogger.get_logger()

    #Database Object connecting to the Courses Collection
    courses_database = MongoDBDatabase(
                url=url,
                username=username,
                password=password,
                auth_mechanism=database_auth_mechanism,
                database=database_name,
                collection=courses_collection_name)
    #Database Object connecting to the Embedded Dataset Collection
    embedded_database = MongoDBDatabase(
                url=url,
                username=username,
                password=password,
                auth_mechanism=database_auth_mechanism,
                database=database_name,
                collection=embedded_dataset_collection_name)

    try:
        logger.info("(Set Up) Setting Up Embedded Dataset")
        #store embedded dataset
        controller = EmbeddingController(courses_database, embedded_database)
        controller.create_embedded_dataset()
        logger.info("(Set Up) Embedded Dataset Stored Successfully")
        controller.retrieve_embedded_dataset()
        logger.info("(Set Up) Embedded Dataset Retrieved Successfully")
    except Exception as e: #pylint:disable=broad-exception-caught
        logger.error("(Set Up) Exception Encountered: " + str(e))
        