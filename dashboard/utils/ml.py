#!/usr/bin/env python3

# import sys
# sys.path.append("/home/cm/innovhope_projects/dashboard_latest/utils/")

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from xgboost import XGBClassifier

from sklearn.metrics import classification_report
from sklearn.metrics import roc_curve, auc

import joblib

from utils.columns import *
from utils.transformers import *
from utils.utils import *

class ModelTraining:

    def __init__(self):
        self.models = {
            'lrc': LogisticRegression(
                class_weight='balanced', max_iter=10000, n_jobs=-1
                ),
            'rfc': RandomForestClassifier(n_jobs=-1),
            'gbc': GradientBoostingClassifier(),
            'xgbc': XGBClassifier()
        }
    
    def make_pipeline(self, algo):
        print('Build numerical transformer ...')
        numeric_preprocessor = Pipeline(
            steps=[('nt', NumericalTransformer())]
        )
        print('Build funding data transformer ...')
        funding_preprocessor = Pipeline(
            steps=[('fdt', FundingTransformer())]
        )
        print('Build frequency transformer ...')
        frequency_preprocessor = Pipeline(
            steps=[('ft', FrequencyTransformer())]
        )
        print('Build time-related transformer ...')
        time_preprocessor = Pipeline(
            steps=[('tt', TimeTransformer())]
        )
        print('Build preprocessor ...')
        preprocessor = ColumnTransformer(
            [
                ('numerical', numeric_preprocessor, numerical_features),
                ('funding', funding_preprocessor, funding_features),
                ('frequency', frequency_preprocessor, freqs_features),
                ('time', time_preprocessor, time_features)
            ]
        )
        steps = [
            #('dft', DataFormatter()),
            ('pp', preprocessor),
            ('scale', MinMaxScaler()),
            (algo, self.models[algo])
        ]
        return Pipeline(steps)

    def train_and_validate_model(self, X, y, algo):
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=46
        )
        print('Build the ML pipeline ...')
        pipe = self.make_pipeline(algo)
        print('Split data into train vs test ...')
        print(f'Training the model using {algo}')
        model = pipe.fit(X_train, y_train)
        #pickle.dump(model, open(f'model_{algo}.pkl', 'w'))
        joblib.dump(model, get_path() + f'model/model_{algo}.joblib')
        print('Generate reports...')
        report_train = classification_report(
            y_train, model.predict(X_train)
        )
        report_test = classification_report(
            y_test, model.predict(X_test)
        )
        print('Model training results:')
        print(report_train)
        print('Model testing results:')
        print(report_test)
        return [report_train, report_test]

def compare_models(X, y):
    mt = ModelTraining()
    ans = {}
    for model in mt.models:
        report = mt.train_and_validate_model(X, y, model)
        ans.update({model:report})
    return ans

# if __name__ == '__main__':
#     print('Loading data for ML ...')
#     dl = DataLoader()
#     df_ml = dl.load_data_ml()
#     print('Select the categories of interest ...')
#     df_ml = select_categories(df_ml, focus_categories)
#     X = df_ml[all_features_ml]
#     y = make_y(df_ml)
#     mt = ModelTraining()
#     mt.train_and_validate_model(X, y, 'lrc')
#     best_model = joblib.load(get_path() + 'model_lrc.joblib')
#     search_results = dl.load_search_results()
#     results = [x[1] for x in best_model.predict_proba(search_results)]
#     print(results)