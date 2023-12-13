 # /usr/bin/env python3
import re
import pandas as pd
import spacy
from spacy.matcher import PhraseMatcher
from news_scraper import *
from news_patterns import *

class NewsUtls:
    
    def __init__(self, keyword):
        self.keyword = keyword 
    
    def reg_pattern_generator(self):
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(self.keyword)
        key = self.keyword.lower()
        
        #manipulate the keywords lemma o lower, getting the pattern answer
        ans_list = []
        for token in doc:
            ans_list.append(token.lemma_.lower())
        ans = ' '.join(ans_list)
        
        if key == ans:
            ans = [ans]
        else:
            ans = [key, ans]
        
        #manipulate long term key words
        if len(ans_list) >= 3:
            noun_list = []
            other_list = []
            for token in doc:
                if token.pos_ == 'NOUN':
                    noun_list.append(token.lemma_.lower())
                else:
                    other_list.append(token.lemma_.lower())
            temp  = [x + ' ' + y for x in noun_list for y in other_list]
            ans += temp    
        #key in str, ans in list
        return key, ans
    
    def adv_pattern_generator(self, patterns):
        key = self.keyword.lower()
        if type(patterns) == list:
            ans = patterns
        else:
            ans = [patterns] 
        return key, ans

    def scraping_news(self, tech, web):
        """
        scrape info from certain outlets
        """
        nsp = NewsScraper()
        if web == 'BBC':
            return nsp.bbc(tech)
        if web == 'CNN':
            return nsp.cnn(tech)
        if web == 'Yahoo':
            return nsp.yahoo(tech)
        if web == 'CNBC':
            return nsp.cnbc(tech)
        if web == 'Fox':
            return nsp.fox(tech)
    
    def rel_adj(self, df, key_list, col_attr):
        index = []
        if df.empty:
            return df
        
        def replace_all_blank(value):
            result = re.sub('\W+', '', value).replace('_', '')
            return result

        for i in range(len(df)):
            test = df[col_attr].str.split()[df.index[i]]
            for j in range(len(test)):
                test[j] = replace_all_blank(test[j]).lower()
            
            bn = False
            for x in key_list:
                if x in test:
                    bn = True
                else:
                    bn = False
                    break
            if bn:
                index.append(df.index[i])
        return df.iloc[index] 
    
    def rel_adj_nlp(self, df, keyword, col_attr):
        index = []
        if df.empty:
            return df
        
        nlp = spacy.load('en_core_web_sm')
        matcher = PhraseMatcher(nlp.vocab, attr='LOWER')
        phrase_patterns = [nlp(x) for x in keywords_phrase_list[keyword.lower()]]
        
        try:
            matcher.add(keyword, *phrase_patterns)
        except:
            matcher.add(keyword, phrase_patterns)
        
        for i in range(len(df)):
            found_matches = matcher(nlp(df[col_attr][df.index[i]]))
            if found_matches:
                index.append(df.index[i])
        return df.iloc[index]
        
    
    def get_data(self, first_pages, web):
        res = pd.DataFrame()
        keyword_list = [x for x in self.keyword.split(' ')]
        search_insertion = '+'.join(keyword_list)
        n = 1  #function for number of pages for output
        count = 1  #function for error times count
        
        while n <= first_pages:
            if web == 'BBC':
                link_part1 = 'https://www.bbc.co.uk/search?q='
                link_part2 = '&page='
                link = link_part1 \
                    + search_insertion \
                    + link_part2 \
                    + str(n) 
                print(link)
                tech = get_soup(link, 'reg')

            if web == 'Yahoo':
                link_part1 = 'https://news.search.yahoo.com/search?p='
                link_part2 = '&pz=10&fr=news&fr2=piv-web&bct=0&b='
                link_part3 = '1&pz=10&bct=0&xargs=0'
                link = link_part1 \
                    + search_insertion \
                    + link_part2 \
                    + str(n-1) \
                    + link_part3 
                print(link)
                tech = get_soup(link, 'reg')
                
            if web == 'Fox':
                link_part1 = 'https://www.foxbusiness.com/search?q='
                link_part2 = '&start='
                link = link_part1 \
                    + search_insertion \
                    + link_part2 \
                    + str((n - 1) * 10)
                print(link)
                tech = get_driver(link)
            
            if web == 'CNN':
                link_part1 = 'https://www.cnn.com/search?q='
                link_part2 = '&from='
                link_part3 = '&size=10&page='
                link_part4 = '&sort=relevance&types=all&section='
                link = link_part1 \
                    + search_insertion \
                    + link_part2 \
                    + str((n - 1) * 10) \
                    + link_part3 \
                    + str(n) \
                    + link_part4
                print(link)
                tech = get_driver(link)

            if web == 'CNBC':
                link_part1 = 'https://www.cnbc.com/search/?query='
                link = link_part1 \
                    + search_insertion
                print(link)
                tech = get_driver(link)
                for i in range(first_pages + 1):
                    tech.execute_script("window.scrollBy(0, 3000)")
                    time.sleep(random.uniform(2, 3))
                n = first_pages
            n += 1
            
            #set temp for test if driver works correctly(especially for Fox)
            temp = self.scraping_news(tech, web)
            if  temp.empty and count <= 3:
                print('Retrying...' + str(count) + ' times')
                #break out loop if we have tried 3 times
                if count == 3:
                    try:
                        tech.quit()
                    except:
                        pass
                    break
                count += 1
                n -= 1
            else:
                count = 1
                res = pd.concat([res, temp])
            #close the driver if we use selenium
            try:
                tech.quit()
            except:
                pass
        
        res['tag'] = ''
        #relevance detection and manipulation on res
        res = res.reset_index(drop=True)
        res1 = self.rel_adj_nlp(res, self.keyword, 'title')
        res1['tag'] = '1'
        res = res.drop(list(res1.index))
        res = res.reset_index(drop=True)
        res2 = self.rel_adj_nlp(res, self.keyword, 'summary')
        res2['tag'] = '2'
        
        res = pd.concat([res1, res2])
        #drop duplicate news in title and summary
        res = res.drop_duplicates(subset=['title'])
        res = res.drop_duplicates(subset=['summary'])
        return res

    def get_all_data(self, first_pages):
        try:
            res = pd.DataFrame()
            outlets = ['BBC','Yahoo','Fox','CNN','CNBC']
            for web in outlets:
                res = pd.concat([res, self.get_data(first_pages, web)])     
            res['keywords'] = self.keyword.lower()
            res.to_csv("Testing Folder/All 20 samples/'" 
                       + str(self.keyword)+"'.csv", 
                       index = False)
            print("\n\n\n")
            return res
        except Exception as e: 
            print("\n\n\n")
            # print(str(self.keyword)+" faces some bug")
            print(e)
            print("\n\n\n")
            return pd.DataFrame()


def scraper_appender(first_pages, keyword_list):
    res = pd.DataFrame()
    for x in keyword_list:
        res = pd.concat([res, NewsUtls(x).get_all_data(first_pages)])
    res.to_csv("Testing Folder/news_search_results.csv", 
               index = False)
    return res