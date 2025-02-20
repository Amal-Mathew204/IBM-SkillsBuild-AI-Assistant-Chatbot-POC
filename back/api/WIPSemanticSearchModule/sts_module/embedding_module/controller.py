"""Embedding Class is an interface for the jinaai/jina-embeddings-v3 embedding model"""
import json
import re
from typing import Union
import torch
import numpy
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import semantic_search
from pandas import DataFrame
from ..database.database_helper import DatabaseHelper
from ..database.mongo_db_interface import MongoDBDatabase


class EmbeddingController:
    """Class will perform both embedding and STS Comparisions between text type data"""
    model_name: str = "jinaai/jina-embeddings-v3"
    model = SentenceTransformer("jinaai/jina-embeddings-v3", trust_remote_code=True)

    def __init__(self, courses_database: MongoDBDatabase, embedded_database: MongoDBDatabase):
        """
        When initialising the Embedding Controller class, the class object must have access to both
        the courses and embedded dataset endpoints on the database server

        Args:
        courses_database (MongoDBDatabase): Database Object creating/connecting to the new 
                                            Database and Collection storing courses data inside
                                            the MongoDB Server.
        embedded_database (MongoDBDatabase): Database Object creating/connecting to the new 
                                            Database and Collection storing the embedded dataset 
                                            inside the MongoDB Server.
        """
        self.__courses_database: MongoDBDatabase = courses_database
        self.__embedded_database: MongoDBDatabase = embedded_database

    def create_embedded_dataset(self) -> None:
        """
        Method obtains the courses data from the database, creates and stores the embedded 
        dataset on a new database inside the MongoDB server 
        """
        #obtain courses from database as json format
        data: list = DatabaseHelper.load_collection_data_json(self.__courses_database)
        # create embedded dataset
        embedded_dataset = self.create_embedding(data)
        DatabaseHelper.store_embedded_dataset(database=self.__embedded_database,
                                                        dataset=embedded_dataset)

    def create_embedding(self, data: Union[str, list]) -> numpy.ndarray:
        """
        Method Creates embeddings using the HuggingFace API Framework through the 
            jinaai embedding model

        Note when embedding a list of dictionary data the method will convert the
        data into a "passage" string before embedding

        Args:
            data (list[dict] | str): data to be embedded
        Returns:
            numpy.ndarray: the embedded object of the parsed data
        """
        #for each dict data obj convert to string then clean data (remove special characters)
        if isinstance(data, list):
            data_to_embed = [re.sub('[^A-Za-z0-9 ]+', '', json.dumps(course)) for course in data]
            return self.model.encode(data_to_embed)

        return self.model.encode(data)

    def retrieve_embedded_dataset(self) -> numpy.ndarray:
        """
        Method returns the embedded dataset from the Database. 
        The method will convert retrieved data from a pandas Dataframe Object
        into numpy.ndarray form.

        Returns:
            numpy.ndarray: 
        """
        dataframe: DataFrame = DatabaseHelper.load_collection_data_dataframe(
                                                        self.__embedded_database)
        dataframe = dataframe.drop(columns=["_id"])
        return dataframe.to_numpy()

    def courses_semantic_search(self, query: str, top_k: int=5) -> list[dict]:
        """
        Method performs semantic search from a users query and the embedded dataset 
        returning the top "top_k" courses closest to the users query

        Args:
            query (str): The users query for a desired course
            top_k (int): Number of top related courses desired to be returned by the method
        Returns:
            list[dict]: list of top k courses (information stored as a dict object)
        """
        #load courses dataset
        courses: list = DatabaseHelper.load_collection_data_json(database=self.__courses_database)
        # get embedded dataset
        embedded_dataset: numpy.ndarray = self.retrieve_embedded_dataset()
        dataset_embeddings = torch.from_numpy(embedded_dataset).to(torch.float)
        embedded_query = torch.FloatTensor(self.create_embedding(query))
        hits = semantic_search(embedded_query, dataset_embeddings, top_k=top_k)
        print(hits)
        top_k_courses = [courses[hits[0][i]['corpus_id']] for i in range(len(hits[0]))]
        for course in top_k_courses:
            course.pop("_id")
        return top_k_courses
