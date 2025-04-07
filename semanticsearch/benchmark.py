"""
Benchmark Module Observes the Memory Usage and Process Time for the Semantic Search Module
"""
import os
from pandas import DataFrame
import time
import psutil
import gc
from sts_module.database.database_helper import DatabaseHelper
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

def get_virtual_memory() -> int:
    """
    Method returns the virtual memory usage of the system

    Returns:
    int: Virtual Memory Usage in MB
    """
    return psutil.virtual_memory().total / 1024 / 1024

def get_swap_memory() -> int:
    """
    Method returns the total swap memory usage of the system

    Returns:
    int: Swap Memory Usage in MB
    """
    return psutil.swap_memory().total / 1024 / 1024

#region Embedded Dataset Creation
def observe_memory_embedded_dataset_setup(courses) -> tuple:
    """
    This method observes the memory usage and process time (CPU execution time) for 
    creating an embedded dataset and storing it into the projects database

    Returns:
       tuple (int, int): (Memory Usage (MB), Process Time (s))
    """
    # invoke garbage collection
    gc.collect()
    prev_memory = get_process_memory()
    prev_virtual_memory = get_virtual_memory()
    prev_swap_memory = get_swap_memory()
    prev_time = time.time()

    controller = EmbeddingController(courses_database, embedded_database)
    embedded_dataset = controller.create_embedding(courses)
    current_time = time.time()
    del controller
    del embedded_dataset
    # invoke garbage collection
    gc.collect()
    total_memory_usage =  abs(get_process_memory() - prev_memory)
    total_virutal_memory_change = abs(get_virtual_memory() - prev_virtual_memory)
    total_swap_memory_change = abs(get_swap_memory() - prev_swap_memory)
    total_time = current_time - prev_time
    return (total_memory_usage, total_virutal_memory_change, total_swap_memory_change, total_time)
#endregion

if __name__ == "__main__":
    courses = DatabaseHelper.load_collection_data_json(courses_database)
    memory_usage, virtual_memory_change, swap_memory_change, process_time = observe_memory_embedded_dataset_setup(courses)

    print("Embedded Dataset Creation Memory Usage (MB): ", memory_usage)
    print("Embedded Dataset Creation Virtual Memory Change (MB): ", virtual_memory_change)
    print("Embedded Dataset Creation Swap Memory Change (MB): ", swap_memory_change)
    print("Embedded Dataset Creation Execution Time (Seconds): ", process_time)
