#!/usr/bin/env python3

# import sys
# sys.path.append("/home/cm/innovhope_projects/dashboard_latest/utils/")

from datetime import datetime
import pickle
import spacy
from spacy.matcher import PhraseMatcher
import multiprocessing as mp
from utils.utils import *

file_path = get_path()
model_direcotry = get_path() + 'model/'

class KeywordMatcher:

    nlp = spacy.load("en_core_web_sm")
    matcher = PhraseMatcher(nlp.vocab)

    def __init__(self):
        self.matcher_file = model_direcotry + 'matcher.sav'
        
    def add_matches(self, category, terms):
        print('adding keywords to the matcher ...')
        all_terms = [x for x in terms.lower().split(', ')]
        print(f'Search term list = {all_terms}')
        pattern = [
            KeywordMatcher.nlp(term) 
            for term in all_terms
        ]
        self.matcher.add(category, pattern)
        print('Save the matcher ...')
        pickle.dump(
            KeywordMatcher.matcher, open(self.matcher_file, 'wb')
        )

    def load_matcher(self):
        self.matcher = pickle.load(
            open(self.matcher_file, 'rb')
        )

    def match(self, text):
        doc = self.nlp(text.lower())
        self.load_matcher()
        ans = self.matcher(doc)
        return len(ans) != 0

    def search(self, df):
        print(f'Starting time: {datetime.now().strftime("%H:%M:%S")}')
        print('Building multiprocessing pipeline ...')
        pool = mp.Pool(mp.cpu_count()-4)
        print('Search for keywords ...')
        results = pool.map(self.match, df['short_description'])
        pool.close()
        print(f'Finishing time: {datetime.now().strftime("%H:%M:%S")}')
        df = df[results]
        print('Save the search results ...')
        df.to_csv(file_path + 'search_results.csv')
        print('Search complete!')
        return df
        
    # def search(self, texts):
    #     return [self.match(text) for text in texts]
