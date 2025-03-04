"""
Benchmark Module Observes the Memory Usage and Process Time for the Semantic Search Module
"""
import os
import time
import psutil
from sts_module.database.mongo_db_interface import MongoDBDatabase
from sts_module.embedding_module.controller import EmbeddingController



#region Database Connection Variables
url: str = "mongodb://localhost:27017/"
username: str = "chatbot"
password: str = "chatbotpassword"
database_auth_mechanism: str = "SCRAM-SHA-1"
database_name: str= "ibm_chatbot"
courses_collection_name: str = "courses"
embedded_dataset_collection_name: str = "embedded_dataset"


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
#endregion

#region utility functions
def get_process_memory() -> int:
    """
    Method returns the memory usage of the current process

    Returns:
    int: Memory Usage in MB
    """
    return psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
#endregion

#region Embedded Dataset Creation
def observe_memory_embedded_dataset_setup() -> tuple:
    """
    This method observes the memory usage and process time (CPU execution time) for 
    creating an embedded dataset and storing it into the projects database

    Returns:
       tuple (int, int): (Memory Usage (MB), Process Time (s))
    """

    prev_memory = get_process_memory()
    prev_time = time.process_time()
    controller = EmbeddingController(courses_database, embedded_database)
    controller.create_embedded_dataset()
    current_time = time.process_time()
    total_memory_usage =  abs(get_process_memory() - prev_memory)
    total_process_time = current_time - prev_time
    return (total_memory_usage, total_process_time)


#endregion

#region Semantic Search
#endregion
rounds: int = 10
total_mem_usage: int = 0
total_process_cpu_time: int = 0
for i in range(rounds):
    print("Round: ", i+1)
    memory_usage, process_time = observe_memory_embedded_dataset_setup()
    total_mem_usage+=memory_usage
    total_process_cpu_time+=process_time

print("Embedded Dataset Creation Average Memory Usage (MB): ", total_mem_usage/rounds)
print("Embedded Dataset Creation Average Process (CPU Execution) Time (Seconds): ",
                                                        total_process_cpu_time/rounds)
