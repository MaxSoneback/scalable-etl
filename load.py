from pymongo import MongoClient
import pandas as pd


class MongoDB:

    def __init__(self, user, password, host, db_name, port='27017', auth_source='admin'):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.db_name = db_name
        self.auth_source = auth_source
        self.uri = f"/mongodb://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}?authSource={self.auth_source}"

        try:
            self.client = MongoClient(self.uri)
            print('Connection to MongoDB established')

        except Exception as e:
            print(e)

    def insert_into_db(self, data, collection):
        if isinstance(data, pd.DataFrame):
            try:
                self.db[collection].insert_many(data.to_dict('records'))
                print("Data inserted")
            except Exception as e:
                print(e)

        else:
            try:
                self.db[collection].insert_many(data)
                print("Data inserted")
            except Exception as e:
                print(e)

    def read_from_db(self, collection):
        try:
            data = pd.DataFrame(list(self.db[collection].find()))
            return data
        except Exception as e:
            print(e)
