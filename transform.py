from extract import Extract
from load import MongoDB
import urllib
import pandas as pd
import numpy as np


class Transformation:

    def __init__(self, data_source, data_set):

        extract_obj = Extract()
        func_name = f"{data_source}_{data_set}"

        if data_source == 'api':
            self.data = extract_obj.get_api_data(data_set)

        elif data_source == 'csv':
            self.data = extract_obj.get_csv_data(data_set)

        else:
            print('Unkown Data Source')
            return

        # getattr function takes in function name of class and calls it.
        getattr(self, func_name)()

    # Economy Data Transformation
    def api_economy(self):
        gdp_india = {}
        for record in self.data['records']:
            gdp = {}

            # taking out yearly GDP value from records
            gdp['GDP_in_rs_cr'] = int(record['gross_domestic_product_in_rs_cr_at_2004_05_prices'])
            gdp_india[record['financial_year']] = gdp
            gdp_india_yrs = list(gdp_india)

        for i in range(len(gdp_india_yrs)):
            if i == 0:
                pass
            else:
                key = 'GDP_Growth_' + gdp_india_yrs[i]
                # calculating GDP growth on yearly basis
                gdp_india[gdp_india_yrs[i]][key] = round(((gdp_india[gdp_india_yrs[i]]['GDP_in_rs_cr'] -
                                                           gdp_india[gdp_india_yrs[i - 1]]['GDP_in_rs_cr']) /
                                                          gdp_india[gdp_india_yrs[i - 1]]['GDP_in_rs_cr']) * 100, 2)

        # connection to mongo db
        mongo_obj = MongoDB(urllib.parse.quote_plus('root'), urllib.parse.quote_plus('password'), 'host', 'GDP')
        # Insert Data into MongoDB
        mongo_obj.insert_into_db(gdp_india, 'India_GDP')

    # Pollution Data Transformation
    def api_pollution(self):
        air_data = self.data['results']

        # Converting nested data into linear structure
        air_list = []
        for data in air_data:
            for measurement in data['measurements']:
                air_dict = {}
                air_dict['city'] = data['city']
                air_dict['country'] = data['country']
                air_dict['parameter'] = measurement['parameter']
                air_dict['value'] = measurement['value']
                air_dict['unit'] = measurement['unit']
                air_list.append(air_dict)

        # Convert list of dict into pandas df
        df = pd.DataFrame(air_list, columns=air_dict.keys())

        # connection to mongo db
        mongo_obj = MongoDB(urllib.parse.quote_plus('root'), urllib.parse.quote_plus('password'), 'host',
                              'Pollution_Data')
        # Insert Data into MongoDB
        mongo_obj.insert_into_db(df, 'Air_Quality_India')

    # Crypto Market Data Transformation
    def csv_cryptomarkets(self):
        assets_code = ['BTC', 'ETH', 'XRP', 'LTC']

        # coverting open, close, high and low price of crypto currencies into GBP values since current price is in Dollars
        # if currency belong to this list ['BTC','ETH','XRP','LTC']
        self.csv_df['open'] = self.csv_df[['open', 'asset']].apply(
            lambda x: (float(x[0]) * 0.75) if x[1] in assets_code else np.nan, axis=1)
        self.csv_df['close'] = self.csv_df[['close', 'asset']].apply(
            lambda x: (float(x[0]) * 0.75) if x[1] in assets_code else np.nan, axis=1)
        self.csv_df['high'] = self.csv_df[['high', 'asset']].apply(
            lambda x: (float(x[0]) * 0.75) if x[1] in assets_code else np.nan, axis=1)
        self.csv_df['low'] = self.csv_df[['low', 'asset']].apply(
            lambda x: (float(x[0]) * 0.75) if x[1] in assets_code else np.nan, axis=1)

        # dropping rows with null values by asset column
        self.csv_df.dropna(inplace=True)

        # saving new csv file
        self.csv_df.to_csv('crypto-market-GBP.csv')