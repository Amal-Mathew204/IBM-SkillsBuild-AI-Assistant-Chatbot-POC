"""Module contains Configurations for the api app"""
import os
import json
from django.apps import AppConfig #pylint: disable=import-error
from pymongo import MongoClient

class ApiConfig(AppConfig):
    """
    Configuration class for api App
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"
    def ready(self) -> None:
        """
        Method executes during the StartUp of the Django server
        Executed functions aim apply and maintain the default configuration
         of the applications Database server

        Methods Executed 
            ApiConfig.database_setup_courses

        """
        with open('api/database_config/default_courses_collection.json',
                   encoding="UTF-8") as file_data:
            courses_data = json.load(file_data)
        url: str = f"mongodb://{os.getenv('MONGO_CONTAINER')}:{os.getenv('MONGO_PORT')}/"
        self.database_setup_courses(
            database_url=url,
            username=os.getenv('MONGO_USER'),
            password=os.getenv('MONGO_PASSWORD'),
            database_auth_mechanism=os.getenv('MONGO_AUTH_MECHANISM'),
            database_name=os.getenv('MONGO_CHATBOT_DATABASE'),
            courses_collection_name=os.getenv('MONGO_COURSE_COLLECTION'),
            course_data=courses_data
        )


    def database_setup_courses(self, database_url: str, username: str, password: str,
                               database_auth_mechanism: str, database_name: str,
                               courses_collection_name: str, course_data: list[dict]) -> None:
        """
        This method sets up the database by adding the course data to the database

        Args:
            database_url (str): URL of the database
            username (str): Username of the database
            password (str): Password of the database
            database_auth_mechanism (str): Authentication mechanism of the database
            database_name (str): Name of the database
            courses_collection_name (str): Name of the collection to store the course data
            course_data (list[dict]): List of dictionaries containing the course data
            
        Returns:
            bool: True if documents were uploaded to the database, False if not
        """
        server_client = MongoClient(database_url,
                                    username=username,
                                    password=password,
                                    authMechanism=database_auth_mechanism)
        server_client.server_info()
        database = server_client[database_name]
        collection = database[courses_collection_name]
        if collection.count_documents({}) > 0:
            return False
        collection.insert_many(course_data)
        server_client.close()
        return True
    