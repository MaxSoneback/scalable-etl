import json
import requests
import pandas as pd


class Extract:

    def __init__(self):
        self.data_sources = json.load(open('config.json'))
        self.api = self.data_sources['data_sources']['api']
        self.csv_path = self.data_sources['data_sources']['csv']

    def get_api_data(self, api_name):
        api_url = self.api[api_name]
        response = requests.get(api_url)

    def get_csv_data(self, csv_name):
        df = pd.read_csv(self.csv_path[csv_name])
