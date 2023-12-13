import pandas as pd
import time
import requests
import random
import datetime
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup
from fake_headers import Headers
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import undetected_chromedriver as uc


headers = Headers(browser="chrome", os="win", headers=True)

def get_soup(link, choice):
    if choice == 'uc':
        driver = uc.Chrome()
        driver.get(link)
        time.sleep(random.uniform(1, 3))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
    elif choice == 'reg':
        response = requests.get(
            link, headers=headers.generate()
        ).text
        time.sleep(random.uniform(1, 3))
        soup = BeautifulSoup(response, 'html.parser')
    return soup

def get_driver(link):
    driver = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub', desired_capabilities=DesiredCapabilities.CHROME)
    time.sleep(random.uniform(1, 3))
    driver.get(link)
    time.sleep(8)
    return driver


class NewsScraper:
    
    def bbc(self, soup):
        """
        BBC News Outlets
        """
        res1, res2, res3 = [], [], []
        for content in soup.find_all('div',{'spacing':'2'}):
            title = content.select_one('span').text
            try:
                title_link = content.select_one('a')['href']
            except:
                continue
                
            res1.append(
                {
                    'title': title,
                    'title_link': title_link
                }
            )
            
        for content in soup.find_all(
            'p', 
            {"class": "ssrcss-1q0x1qg-Paragraph eq5iqo00"}
        ):
            summary = content.text
            
            res2.append(
                {
                    'summary': summary
                }
            )
           
        #Solve the problem sometimes we may not have the summary
        if len(res2) < len(res1):
            res2 = []
            for i in range(len(res1)):
                res2.append({'summary': ''})
            
        for content in soup.find_all('div', {"spacing":"4"}):
            if content.select_one('span'):
                date = \
                content.select_one('span').select_one('span').text
            
                res3.append(
                    {
                        'date': date
                    }
                )
            
        for i in range(len(res1)):
            res1[i].update(res2[i])
            res1[i].update(res3[i])
            
        df = pd.DataFrame.from_dict(res1)
        
        #Time Adjustment Part directly on dataframe
        if not df.empty:
            df['date'] = df['date'].astype(str)

            df.loc[(df['date'].str[-1] == 's'), 'date'] = ' '
            df1 = df.loc[df['date'] == ' ']
            df2 = df.loc[(df['date'].str[-3:] == 'ago')
                         | (df['date'] == 'Today')]
            df3 = df.loc[(df['date'].str[-1].str.isdigit() == False) 
                         & (~df['date'].isin(df1['date']))
                         & (~df['date'].isin(df2['date']))]
            df4 = df.loc[(~df['date'].isin(df1['date']))
                         & (~df['date'].isin(df2['date']))
                         & (~df['date'].isin(df3['date']))]
            df1['date'] = ''

            if not df1.empty:
                df1['date'] = pd.to_datetime(df1['date'])
            if not df4.empty:
                df4['date'] = pd.to_datetime(df4['date'])
                df4['date'] = df4['date'].dt.date
            if not df2.empty:
                for i in range(1,31):
                    df2.loc[(df2['date'].astype(str).str[0:3] 
                             == str(i)+' d'),'date'] \
                    = pd.datetime.now().date() + datetime.timedelta(-i)
                df2[df2['date'].apply(lambda x: isinstance(x, str))] \
                = pd.datetime.now().date()
            if not df3.empty:
                df3['date'] += ' 2022'
                df3['date'] = pd.to_datetime(df3['date'])
                df3['date'] = df3['date'].dt.date

            date_series = df1['date']
            date_series = date_series.append(df2['date'])
            date_series = date_series.append(df3['date'])
            date_series = date_series.append(df4['date'])

            df['date'] = date_series
        return df

    def yahoo(self, soup):
        """
        Yahoo News Outlets
        """
        res1, res2, res3 = [], [], []
        for content in soup.find_all('a',{"style":"font-size:16px;"}):
            title = content.text
            try:
                title_link = content['href']
            except:
                continue

            res1.append(
                {
                    'title': title,
                    'title_link': title_link
                }
            )
            
        for content in soup.find_all('p',{"class":"s-desc"}):
            summary = content.text
            
            res2.append(
                {
                    'summary': summary
                }
            )

        if len(res2) < len(res1):
            res2 = []
            for i in range(len(res1)):
                res2.append({'summary': ''})
            
        for content in soup.find_all('span',{"fc-2nd s-time mr-8"}):
            date = content.text

            res3.append(
                {
                    'date': date
                }
            )

        for i in range(len(res1)):
            res1[i].update(res2[i])
            res1[i].update(res3[i])
            
        df = pd.DataFrame.from_dict(res1)
        
        #Time Adjustment Part directly on dataframe
        if not df.empty:
            df['date'] = df['date'].astype(str)
            df['date'] = df['date'].apply(lambda x: x[2:])

            df2 = df.loc[df['date'].str.contains('day')]
            df3 = df.loc[df['date'].str.contains('month')]
            df4 = df.loc[df['date'].str.contains('year')]
            df1 = df.loc[(~df['date'].isin(df2['date'])) \
                         & (~df['date'].isin(df3['date'])) \
                         & (~df['date'].isin(df4['date']))]

            if not df1.empty:
                for i in range(1,25): #hours
                    try:
                        df1.loc[((df1['date'].str[0] == str(i)) \
                                 | (df1['date'].str[:2] == str(i))),'date'] \
                        = pd.datetime.now().date()
                    except:
                        break
            if not df2.empty:
                for i in range(1,32): #days
                    try:
                        df2.loc[((df2['date'].str[0] == str(i)) 
                                 | (df2['date'].str[:2] == str(i))),'date'] \
                        = pd.datetime.now().date() + relativedelta(days=-i)
                    except:
                        break
            if not df3.empty:
                for i in range(1,13): #months
                    try:
                        df3.loc[((df3['date'].str[0] == str(i)) \
                                 | (df3['date'].str[:2] == str(i))),'date'] \
                        = pd.datetime.now().date() + relativedelta(months=-i)
                    except:
                        break
            if not df4.empty:
                for i in range(1,6): #years
                    try:
                        df4.loc[(df4['date'].str[0] == str(i)),'date'] \
                        = pd.datetime.now().date() + relativedelta(years=-i)
                    except:
                        break

            date_series = df1['date']
            date_series = date_series.append(df2['date'])
            date_series = date_series.append(df3['date'])
            date_series = date_series.append(df4['date'])

            df['date'] = date_series
        return df
  
    def fox(self, driver):
        """
        Fox News Outlets
        """
        res1, res2, res3, res4 = [], [], [], []
        temp = driver.find_elements(By.CLASS_NAME,"title")
        
        #test if the driver works correctly
        if len(temp) <= 1:
            return pd.DataFrame()
        
        for content in temp[1:]:
            title = content.text

            res1.append(
                {
                    'title': title
                }
            )

        for content in driver.find_elements(By.CSS_SELECTOR,".title [href]"):
            title_link = content.get_attribute('href')

            res2.append(
                {
                    'title_link': title_link
                }
            )
            
        for content in driver.find_elements(By.CLASS_NAME,"dek"):
            summary = content.text

            res3.append(
                {
                    'summary': summary
                }
            )

        if len(res3) < len(res1):
            res3 = []
            for i in range(len(res1)):
                res3.append({'summary': ''})
            
        for content in driver.find_elements(By.CLASS_NAME,"time"):
            date = content.text

            res4.append(
                {
                    'date': date
                }
            )
             
        for i in range(len(res1)):
            res1[i].update(res2[i])
            res1[i].update(res3[i])
            res1[i].update(res4[i])
            
        df = pd.DataFrame.from_dict(res1)
          
        #Time Adjustment Part directly on dataframe
        if not df.empty:
            df['date'] = df['date'].astype(str)
            
            df1 = df.loc[(df['date'].str[-3:] == 'ago')]
            df2 = df.loc[(~df['date'].isin(df1['date'])) 
                         & (df['date'].str[-5] == ' ')]
            df3 = df.loc[(~df['date'].isin(df1['date'])) 
                         & (~df['date'].isin(df2['date']))] + ', 2022'
            
            if not df1.empty:
                df1['date'] = pd.datetime.now().date()
                         
            date_series = df1['date']
            date_series = date_series.append(df2['date'])
            date_series = date_series.append(df3['date'])
            
            df['date'] = date_series
            df['date'] = pd.to_datetime(df['date']).dt.date
            df.loc[df['date'] > pd.datetime.now().date(), 'date'] \
            += relativedelta(years=-1)
        return df            
 
    def cnn(self, driver):
        """
        CNN News Outlets
        """
        res1, res2, res3, res4 = [], [], [], []
        temp = driver.find_elements(By.CLASS_NAME, "container__headline")
        
        #test if the driver works correctly
        if len(temp) <= 1:
            return pd.DataFrame()
        
        for content in temp:
            title = content.text

            res1.append(
                {
                    'title': title
                }
            )

        for content in driver.find_elements(By.CSS_SELECTOR, ".card [href]"):
            title_link = content.get_attribute('href')

            res2.append(
                {
                    'title_link': title_link
                }
            )
            
        for content in \
        driver.find_elements(By.CLASS_NAME, "container__description"):
            summary = content.text[:1000]
            
            res3.append(
                {
                    'summary': summary
                }
            )

        if len(res3) < len(res1):
            res3 = []
            for i in range(len(res1)):
                res3.append({'summary': ''})
                
        for content in driver.find_elements(By.CLASS_NAME, "container__date"):
            date = content.text

            res4.append(
                {
                    'date': date
                }
            )
             
        for i in range(len(res1)):
            res1[i].update(res2[i])
            res1[i].update(res3[i])
            res1[i].update(res4[i])
            
        df = pd.DataFrame.from_dict(res1)
        
        #Time Adjustment Part directly on dataframe
        if not df.empty:        
            df['date'] = df['date'].astype(str)
            df['date'] = pd.to_datetime(df['date']).dt.date
        return df

    def cnbc(self, driver):
        """
        CNBC News Outlets
        """
        res1, res2, res3, res4 = [], [], [], []
        temp = driver.find_elements(By.CLASS_NAME, 
                                    "SearchResult-searchResultTitle")
        
        #test if the driver works correctly
        if len(temp) <= 1:
            return pd.DataFrame()
        
        for content in temp:
            title = content.text

            res1.append(
                {
                    'title': title
                }
            )

        for content in \
        driver.find_elements(By.CSS_SELECTOR, \
                             ".SearchResult-searchResultTitle [href]"):
            title_link = content.get_attribute('href')

            res2.append(
                {
                    'title_link': title_link
                }
            )
         
        for content in \
        driver.find_elements(
            By.CLASS_NAME, "SearchResult-searchResultPreview"
        ):
            summary = content.text
            
            res3.append(
                {
                    'summary': summary
                }
            )

        if len(res3) < len(res1):
            res3 = []
            for i in range(len(res1)):
                res3.append({'summary': ''})

        for content in \
        driver.find_elements(By.CLASS_NAME,"SearchResult-publishedDate"):
            date = content.text

            res4.append(
                {
                    'date': date
                }
            )
             
        for i in range(len(res1)):
            res1[i].update(res2[i])
            res1[i].update(res3[i])
            res1[i].update(res4[i])
            
        df = pd.DataFrame.from_dict(res1)
        
        #Time Adjustment Part directly on dataframe
        if not df.empty:
            df['date'] = df['date'].astype(str)
            df['date'] = df['date'].apply(lambda x: x.split()[0])
            df['date'] = \
            df['date'].apply(lambda x: \
                             datetime.datetime.strptime(x, '%m/%d/%Y').date())
        return df