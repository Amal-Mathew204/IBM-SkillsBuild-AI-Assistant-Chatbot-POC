import os

CONFIG = {
    # 'mongo_uri': f"mongodb://{os.getenv('MONGO_ROOT_USERNAME', 'admin')}:{os.getenv('MONGO_ROOT_PASSWORD', 'adminpassword')}@localhost:27017/ibm_chatbot?authSource=admin",
    'es_host': 'elasticsearch',
    'es_port': 9200,
    'es_user': os.getenv('ELASTICSEARCH_USERNAME', 'elastic'),
    'es_password': os.getenv('ELASTICSEARCH_PASSWORD', 'yourpassword')
}
