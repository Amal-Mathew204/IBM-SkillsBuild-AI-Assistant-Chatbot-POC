"""
Script contains all unit tests for the Semantic Search Module Core Interactions
Note: Tests require an active Test MongoDB Server instance
"""
import unittest
from jsonschema import ValidationError, validate
import numpy
from pymongo import MongoClient
from sts_module.database.database_helper import DatabaseHelper
from sts_module.database.mongo_db_interface import MongoDBDatabase
from sts_module.embedding_module.controller import EmbeddingController


class EmbeddingControllerTests(unittest.TestCase):
    """
    Class for testing the EmbeddingController Class Semantic Search Module. 
    The Tests will test both database interactions and embedding tasks

    Fields:
        course_database (MongoDBDatabase): The database instance to connected with the course 
                                           collection stored in the database server
        course_database (MongoDBDatabase): The database instance to connected with the course 
                                           collection stored in the database server
        
    """
    #Database Object connecting to the Courses Collection
    courses_database = MongoDBDatabase(
                url="mongodb://localhost:27017/",
                username="chatbot",
                password="chatbotpassword",
                auth_mechanism="SCRAM-SHA-1",
                database="ibm_chatbot",
                collection="courses")
    #Database Object connecting to the Embedded Dataset Collection
    embedded_database = MongoDBDatabase(
                    url="mongodb://localhost:27017/",
                    username="chatbot",
                    password="chatbotpassword",
                    auth_mechanism="SCRAM-SHA-1",
                    database="ibm_chatbot",
                    collection="embedded_dataset")
    course_schema_udemy = {
        "type" : "object",
        "properties" : {
            "name": {"type": "string"},
            "price": {"type": "string"},
            "description": {"type": "string"},
            "host": {"type": "string"},
            "rating": {"type": "number"},
            "duration": {"type": "string"},
            "lectures": {"type": "string"},
            "level": {"type": "string"},
            "url": {"type": "string"}
    }}
    course_schema_ibm = {
        "type" : "object",
        "properties" : {
            "title": {"type": "string"},
            "description": {"type": "string"},
            "learning_hours": {"type": "string"},
            "course_type": {"type": "string"},
            "tags": {"type": "array"},
            "url": {"type": "string"}
    }}


    def test_create_embeddings(self) -> None:
        """
        This method tests the Embedding Controller can successfully create embeddings. 
        There are two types of embeddings that are created by the EmbeddingController 
        Class (that will be tested):
        - Test creating query embedding: returning a single numpy ndarray
        - Test creating embedded dataset: returning the set of values as a nested numpy ndarray

        Assert Conditions:
        -  Check the number of rows of the retrieved embedded dataset matches the number 
           of courses stored on the database
        - Check that the dimensions of the embedded query (numpy obj) is equal to 1
        """
        controller = EmbeddingController(self.courses_database, self.embedded_database)
        #load list of courses from the database
        courses: list = DatabaseHelper.load_collection_data_json(self.courses_database)
        # create embedded dataset
        embedded_dataset: numpy.ndarray = controller.create_embedding(courses)
        self.assertEqual(len(embedded_dataset), len(courses))
        #create embedded query
        query: str = "Introduction to datascience"
        embedded_query: numpy.ndarray =  controller.create_embedding(query)
        correct_array_dimension: int = 1
        self.assertEqual(embedded_query.ndim, correct_array_dimension)

    def test_create_embedded_dataset(self) -> None:
        """
        Method tests the creation and storage (to the MongoDB Server Instance) of 
        an embedded_dataset.

        This is comprised of two tests:
        - Test creation of embedded dataset and store on DB
        - Test replacement of embedded dataset and store onto DB

        Assert Condition:
            Check the number of rows of the retrieved embedded dataset matches the 
            number of courses stored on the database
        """
        #load list of courses from the database
        courses: list = DatabaseHelper.load_collection_data_json(self.courses_database)
        #reset EmbeddedDataset > Courses collection
        server_client = MongoClient(self.embedded_database.server_url,
                                    username="chatbot",
                                    password="chatbotpassword",
                                    authMechanism="SCRAM-SHA-1")
        database = server_client[self.embedded_database.database]
        collection = database[self.embedded_database.collection]
        collection.drop()
        server_client.close()

        #create embedded dataset
        controller = EmbeddingController(self.courses_database, self.embedded_database)
        controller.create_embedded_dataset()
        embedded_dataset = controller.retrieve_embedded_dataset()
        self.assertEqual(len(embedded_dataset), len(courses))

        #check embedded dataset replacement
        controller = EmbeddingController(self.courses_database, self.embedded_database)
        controller.create_embedded_dataset()
        embedded_dataset = controller.retrieve_embedded_dataset()
        self.assertEqual(len(embedded_dataset), len(courses))

    def test_recieve_embedded_dataset(self) -> None:
        """
        Method tests to see that the EmbeddedController can successfully retrieve the
        embedded dataset from the database

        Assert Condition:
            Check the number of rows of the retrieved embedded dataset matches the number of
              courses stored on the database
        """
        #load list of courses from the database
        courses: list = DatabaseHelper.load_collection_data_json(self.courses_database)
        controller = EmbeddingController(self.courses_database, self.embedded_database)
        embedded_dataset = controller.retrieve_embedded_dataset()
        self.assertEqual(len(embedded_dataset), len(courses))

    def test_semantic_search(self) -> None:
        """
        Method tests the semantic search method inside the Embedded Controller

        Assert Conditions;
            - Check the correct ammount of courses is returned by the method
            - Check that the schema of the course data objects is valid
        """
        #load list of courses from the database
        controller = EmbeddingController(self.courses_database, self.embedded_database)
        top_k: int = 10
        top_k_courses: list[dict] = controller.courses_semantic_search(
                                                       "Introduction to DataScience", top_k)
        self.assertEqual(len(top_k_courses), top_k)
        try:
            for course in top_k_courses:
                validate(course, self.course_schema_ibm)
        except ValidationError as e:
            self.fail(f"Invalid Course Schema: {e.message}")

if __name__ == "__main__":
    unittest.main()
