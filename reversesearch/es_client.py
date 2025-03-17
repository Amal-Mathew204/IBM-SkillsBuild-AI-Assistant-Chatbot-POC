from elasticsearch import Elasticsearch
from config import CONFIG

def get_es_client():
    return Elasticsearch(
        [{"host": CONFIG['es_host'], "port": CONFIG['es_port'], "scheme": "http"}],
        basic_auth=(CONFIG['es_user'], CONFIG['es_password'])  # Authenticate with username & password
    )
def create_index(es_client, index_name):
    

    settings = {
        "settings": {
            "analysis": {
                "analyzer": {
                    "custom_analyzer": {
                        "type": "standard",
                        "stopwords": "_english_"
                    }
                }
            }
        }
    }
    es_client.indices.create(index=index_name, body=settings, ignore=400)
    print(f"Created index: {index_name} with custom settings")

def index_documents(es_client, index_name, documents):
    for doc in documents:
        doc_id = str(doc["_id"])
        del doc["_id"]
        es_client.index(index=index_name, id=doc_id, document=doc)

def search_similar_courses(es_client, index_name, course_input):
    search_query = {
        "query": {
            "bool": {
                "should": [
                    {
                        "more_like_this": {
                            "fields": ["title"],
                            "like": course_input["title"],
                            "min_term_freq": 1,
                            "max_query_terms": 12,
                            "boost": 3  # Higher boost for title
                        }
                    },
                    {
                        "more_like_this": {
                            "fields": ["description"],
                            "like": course_input["description"],
                            "min_term_freq": 1,
                            "max_query_terms": 25,  # Allowing more terms for description
                            "boost": 1  # Moderate boost for description
                        }
                    },
                    {
                        "more_like_this": {
                            "fields": ["tags"],
                            "like": course_input["tags"],
                            "min_term_freq": 1,
                            "max_query_terms": 12,
                            "boost": 2  # Boost for tags
                        }
                    }
                ],
                "must_not": [
                    {
                        "term": {
                            "title.keyword": course_input["title"]  # Exclude courses with the same title
                        }
                    }
                ]
            }
        }
    }
    return es_client.search(index=index_name, body=search_query)




