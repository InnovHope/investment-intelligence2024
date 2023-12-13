#!/usr/bin/env python3

# import sys
# sys.path.append("/home/cm/innovhope_projects/dashboard_latest/utils/")

import os
import pandas as pd
import pickle
import joblib
from utils.columns import *
from utils.transformers import *

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

def get_path():
    return os.getcwd() + '/data/'
    
def get_all_files():
    path = get_path()
    file_names =[
        x for x in os.listdir(path + 'csv/') 
        if x.endswith('.csv')
        and not x.startswith('check')
    ]
    return file_names

def sql2df(table_name, conn):
    if not table_name or not conn:
        print('please check the input.')

    query = f'select * from {table_name};'
    res = pd.read_sql_query(query, conn)
    if 'index' in res.columns:
        return res.drop('index', axis=1)
    return res

# make options for dropdown input
def make_options(vars):
    options = [
        {'label':str(vars[var]), 'value': str(var)} 
        for var in vars
    ]
    return options

def get_gps_coords(address):
    geo_locator = Nominatim(user_agent='geopy_locator')
    geoLoc = geo_locator.geocode(address)
    return [geoLoc.latitude, geoLoc.longitude]

def df2sql(df, con):
    if not df or not con:
        print('please check the input.')
    df.to_sql(f'{df}_useful', con=con, if_exists='replace')


class DataLoader:
    
    data_path = get_path()

    def load_data_ml(self):
        ans = pd.read_csv(
            DataLoader.data_path + 'df_ml.csv', 
            lineterminator='\n', 
            low_memory=False
        )
        ans = select_categories(ans, focus_categories)
        return ans.drop('Unnamed: 0', axis=1)

    def load_data_all(self):
        ans = pd.read_csv(
            DataLoader.data_path + 'df_all.csv', 
            lineterminator='\n', 
            low_memory=False
        )
        return ans.drop('Unnamed: 0', axis=1)

    def load_search_results(self):
        ans = pd.read_csv(
            DataLoader.data_path + 'search_results.csv', 
            lineterminator='\n', 
            low_memory=False
        )
        return ans.drop('Unnamed: 0', axis=1)

    def load_ranked_search_results(self):
        ans = pd.read_csv(
            DataLoader.data_path + 'ranked_search_results.csv', 
            lineterminator='\n', 
            low_memory=False
        )
        return ans


class ModelLoader:
    
    model_path = get_path() + 'model/'

    def load_best_model(self):
        return joblib.load(ModelLoader.model_path + 'model_gbc.joblib')

    def load_matcher(self):
        return pickle.load(
            open(ModelLoader.model_path + 'matcher.sav', 'rb')
        )

class DataFormatter:

    def __init__(self):
        self.columns_string = columns_string
        self.columns_numeric = columns_numeric
        self.columns_date = columns_date
        self.all_features_ml = ['uuid'] \
            + ['name'] \
            + all_features_ml \
            + ['address'] \
            + ['postal_code'] \
            + ['short_description'] \
            + ['description'] \
            + ['category_groups_list'] \
            + ['status']

    def fit(self, X, y=None):
        pass

    def transform(self, X, y=None):
        for column in self.columns_numeric:
            X[column] = pd.to_numeric(X[column], errors='coerce')
        for column in self.columns_date:
            X[column] = pd.to_datetime(X[column], errors='coerce')
        X[columns_string] = X[columns_string].astype('str')
        return X, X[self.all_features_ml]

    def fit_transform(self, X, y=None):
        self.fit(X)
        return self.transform(X)

def get_coords(df):
    geolocator = Nominatim(user_agent="organization_coords_identifier")
    #geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    columns_location = [
        'name', 'address', 'city', 'state_code', 'postal_code', 
        'country_code'
    ]
    df = df[columns_location]
    ans = {}
    for _, row in df.iterrows():
        address = ', '.join([x for x in row[1:] if x != 'None'])
        print(address)
        loc = geolocator.geocode(address)
        if loc is None:
            ans.update({row[0]: [0, 0]})
        else:
            ans.update({row[0]: [loc.latitude, loc.longitude]})
    print(ans)
    return ans
    # addresses = []
    # for _, row in df[columns_location].iterrows():
    #     addresses.append(', '.join([x for x in row[1:] if x != 'None']))
    # df['loc'] = addresses
    # print(df['loc'])
    # df['coords'] = df['loc'].apply(geolocator.geocode)
    # print(df['coords'])
    # return df[['name', ['coords']]]