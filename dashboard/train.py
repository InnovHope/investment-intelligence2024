#!/usr/bin/env python3

import joblib

from utils.columns import *
from utils.transformers import *
from utils.utils import *
from utils.ml import *

def compare_models(X, y):
    mt = ModelTraining()
    ans = {}
    for model in mt.models:
        report = mt.train_and_validate_model(X, y, model)
        ans.update({model:report})
    return ans

if __name__ == '__main__':
    print('Loading data for ML ...')
    dl = DataLoader()
    df_ml = dl.load_data_ml()
    print('Select the categories of interest ...')
    df_ml = select_categories(df_ml, focus_categories)
    X = df_ml[all_features_ml]
    y = make_y(df_ml)
    mt = ModelTraining()
    mt.train_and_validate_model(X, y, 'gbc')
    best_model = joblib.load(get_path() + 'model/model_gbc.joblib')
    search_results = dl.load_search_results()
    results = [x[1] for x in best_model.predict_proba(search_results)]
    print(results)