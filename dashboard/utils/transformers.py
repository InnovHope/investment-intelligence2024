#!/usr/bin/env python3

# import sys
# sys.path.append("/home/cm/innovhope_projects/dashboard_latest/utils/")

import numpy as np
import pandas as pd

from utils.columns import *

def select_categories(df, categories):

    def screen_category(df, category):
        category = category[0].upper() + category[1:]
        res = df[
            df['category_groups_list'].map(
                lambda x: True 
                if x and category in str(x) 
                else False
            )
        ]
        return res

    ans = pd.DataFrame()
    for category in categories:
        selection = screen_category(df, category)
        ans = pd.concat([ans, selection], axis=0)

    return ans.drop_duplicates()

def make_y(df, method='binary'):
    if method == 'binary':
        y = df['status'].map(
            lambda x: 1 if x=='ipo' else 0
        )
    elif method == 'multi':
        class_dict = {
            'closed': 0,
            'operating': 1,
            'acquired': 2,
            'ipo': 3
        }
        y = df['status'].map(class_dict)
    return y

class NumericalTransformer:

    def fit(self, X, y=None):
        self.median = X.mean() 

    def transform(self, X, y=None):
        return X.fillna(self.median)

    def fit_transform(self, X, y=None):
        self.fit(X)
        return self.transform(X)

class FundingTransformer:

    def fit(self, X, y=None):
        pass

    def transform(self, X, y=None):
        return X.fillna(0)

    def fit_transform(self, X, y=None):
        self.fit(X)
        return self.transform(X)

class FrequencyTransformer:
    
    def fit(self, X, y=None):
        self.columns = X.columns
        self.dict = {
            column:dict(X[column].value_counts()) 
            for column in self.columns
        }
        self.medians = {
            column:np.mean(X[column].value_counts().values) 
            for column in self.columns
        }
        #print(self.medians)
    
    def transform(self, X, y=None):
        res = pd.DataFrame()
        for column in self.columns:
            df = X[column].map(self.dict[column])
            df.fillna(self.medians[column], inplace=True)
            df.columns = ['column']
            res = pd.concat([res, df], axis=1)
        return res

    def fit_transform(self, X, y=None):
        self.fit(X)
        return self.transform(X)

class TimeTransformer:
    
    def fit(self, X, y=None):
        self.columns = X.columns
        df = self.date2year(X)
        self.median = df.mean()

    def transform(self, X, y=None):
        df = self.date2year(X)
        return df.fillna(self.median)
        
    def fit_transform(self, X, y=None):
        self.fit(X)
        return self.transform(X)

    def date2year(self, X, y=None):
        res = pd.DataFrame()
        for column in self.columns:
            df = pd.to_datetime(X[column], errors='coerce').dt.year
            df.columns = column
            res = pd.concat([res, df], axis=1)
        res['num_years_funding'] = res['last_funding_on'] - \
            res['founded_on']
        res['num_years_funding'].map(lambda x: x if x >= 0 else None)
        res['num_years_before_public'] = res['went_public_on'] - \
            res['founded_on']
        res['num_years_before_public'].map(lambda x: x if x >= 0 else None)
        return res[['num_years_funding', 'num_years_before_public']]