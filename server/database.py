import os
import pymongo

# Connect to MongoDB


def connect_to_mongo():
    url_auth = f'{os.environ["MONGO_DB_USERNAME"]}:{os.environ["MONGO_DB_PASSWORD"]}@'
    ip_port = f'{os.environ["CLIENT_DB_HOST"]}:{os.environ["CLIENT_DB_PORT"]}'
    db = pymongo.MongoClient(f'mongodb://{url_auth}{ip_port}')
    return db


def get_clients_collection():
    db = connect_to_mongo()
    collection = db[os.environ["CLIENT_DB_NAME"]
                    ][os.environ["CLIENTS_COLLECTION_NAME"]]
    return collection


def get_items_collection():
    db = connect_to_mongo()
    collection = db[os.environ["CLIENT_DB_NAME"]
                    ][os.environ["ITEMS_COLLECTION_NAME"]]
    return collection


def get_transactions_collection():
    db = connect_to_mongo()
    collection = db[os.environ["CLIENT_DB_NAME"]
                    ][os.environ["TRANSACTIONS_COLLECTION_NAME"]]
    return collection
