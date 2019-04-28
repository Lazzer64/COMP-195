from .database_storage import *


def store_data(type, data_list):
    database_store(type, data_list)


def read_data(type):
    query_data(type)


def create_storage():
    create_db()
