#!/usr/bin/env python3

# module including some settings of the app
# feature variable of the data
numerical_features = [
    'Total Equity Funding Amount Currency (in USD)',
    'Total Funding Amount Currency (in USD)',
    'Number of Acquisitions',
    'Price Currency (in USD)',
    'Number of Founders',
    'Number of Funding Rounds',
    'Last Funding Amount Currency (in USD)',
    'Last Equity Funding Amount Currency (in USD)',
    'Number of Investments',
    'Number of Lead Investors',
    'Number of Investors',
    'Money Raised at IPO Currency (in USD)',
    'Valuation at IPO Currency (in USD)',
    'IPqwery - Patents Granted',
    'IPqwery - Trademarks Registered',
    'Number of Events',
    'Similar Companies'
]

text_features = ['Description', 'Full Description']

location_features = ['City', 'State', 'Country']

categorical_features = [
    'Industries', 
    'Last Funding Type',
    'IPO Status',
    'Operating Status',
    'Number of Employees',
    'Acquisition Status',
    'Estimated Revenue Range',
    'Funding Status',
    'Last Equity Funding Type'
]

countries = dict(US='United States')

# supervised = dict(
#     RF='Random Forest',
#     LR='Logistic Regression',
#     XB='XGBoost',
#     NN='Neural Network'
# )

# unsupervised = dict(
#     CL='Clustering',
#     KM='k-means',
#     MM='mixture models',
#     DB='DBSCAN'
# )

# nlp = dict(
#     ST='Sentiment',
#     MK='Morkov Chain',
#     NN='Neural Network'
# )

ML = dict(
    rf='Random Forest', 
    lr='Logistic Regression'
)
