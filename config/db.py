from pymongo import MongoClient
from pymongo.server_api import ServerApi
from decouple import config

def get_mongo_uri():
    host = config('MONGODB_HOST', default='localhost')
    port = int(config('MONGODB_PORT', default=27017))
    db_name = config('MONGODB_DB_NAME', default='educarural')
    username = config('MONGODB_USERNAME', default='')
    password = config('MONGODB_PASSWORD', default='')

    if username and password:
        if "mongodb.net" in host:
            print("Conectando a MongoDB Atlas")
            return f"mongodb+srv://{username}:{password}@{host}/?retryWrites=true&w=majority"
        else:
            print("Conectando a MongoDB remoto/autenticado")
            return f"mongodb://{username}:{password}@{host}:{port}/{db_name}?authSource=admin"
    else:
        print("Conectando a MongoDB local")
        return f"mongodb://{host}:{port}"

def get_mongodb_connection():
    uri = get_mongo_uri()
    try:
        client = MongoClient(
            uri,
            server_api=ServerApi('1'),
            connectTimeoutMS=5000,
            socketTimeoutMS=30000,
            retryWrites=True
        )
        client.admin.command('ping')
        print("Conectado correctamente a MongoDB")
        db_name = config('MONGODB_DB_NAME', default='educarural')
        return client[db_name]
    except Exception as e:
        print(f"Error al conectar a MongoDB: {e}")
        return None

mongodb = get_mongodb_connection()