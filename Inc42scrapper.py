import requests
import traceback
from db import Mdb
from bs4 import BeautifulSoup
from bs4 import NavigableString
from bs4 import Tag
from utils import sleep_scrapper, get_request_headers, scraper_csv_write

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import re
import os
import time
import random
import string
import tempfile
import json
import datetime
import sys
import pytz
from datetime import date
from datetime import datetime
from datetime import time
from pytz import timezone
from dateutil.tz import tzutc, tzlocal
from pprint import pprint

class Inc42Scrapper:
    def __init__(self):
        self.mdb = Mdb()
    
    def run(self):
        try:
            base_url = 'https://inc42.com/buzz/'
            r = requests.get(base_url,headers=get_request_headers())
            print ('[IncScrapper] :: fetching data from TEAMS url: ', base_url)
            if not r.status_code == 200:
                print ("[IncScrapper] :: Failed to get " \
                    "content of url: %s" % base_url)
                return
            html_doc = r.content
            soup = BeautifulSoup(html_doc, 'html.parser')
            div1 = soup.find('div',class_="site-content")
            inc_news = div1.find_all("div",{"class":"card-wrapper horizontal-card"})
            for news in inc_news:
                self.scrape_home(news)
            sleep_scrapper('Inc42scrapper')
            #next pages data
            for i in range(2,100,1):
                page = 'page'
                url = base_url + page + str(i)
                r = requests.get(url,headers=get_request_headers())
                print ('[IncScrapper] :: fetching data from TEAMS url: ', url)
                if not r.status_code == 200:
                    print ("[IncScrapper] :: Failed to get " \
                        "content of url: %s" % url)
                    return
                html_doc = r.content
                soup = BeautifulSoup(html_doc, 'html.parser')
                div1 = soup.find('div',class_="site-content")
                inc_news = div1.find_all("div",{"class":"card-wrapper horizontal-card"})
                for news in inc_news:
                    self.scrape_home(news)
                sleep_scrapper('Inc42scrapper')    
        except Exception as exp:
            print ('[Inc42Scrapper] :: run() :: Got exception at fetching data from INC42 Homepage: %s'\
                % exp)
            print(traceback.format_exc())
    
    def scrape_home(self,news):
        try:
            news_image = news.find('figure',class_='card-image')
            news__ = news_image.find('a')
            news_=(news__['href'])
            news_l = news_.split('?')
            news_link = news_l[0]
            news_lin = news_link.split('/')
            folder_name=news_lin[4]
            directory = folder_name
            parent_dir = 'C:/Users/lenovo/Desktop/scholarsbook_scrappers_data/Inc42/' #input("Enter the folder path where to store data: ") 
            blog_path = os.path.join(parent_dir,directory)
            
            os.mkdir(blog_path)         
            print('[AnyWebsiteScraper] :: blog_Folder has been created:',blog_path)
            os.chdir(blog_path)
            #print('currentpath',os.getcwd())
            print('[Inc42Scrapper]::::::::::: NEWS_Link',news_link)
            img = news__.find('img')['src']
            img_ = img.split('?')
            News_Image_url = img_[0]
            print('[Inc42Scrapper]::::::::::: NEWS_Image_URL',News_Image_url)
            News_Image = News_Image_url.split('/').pop()
            raw1_media=requests.get(News_Image_url, stream=True)
            with open(News_Image,"wb") as f:
                f.write(raw1_media.content)
                print('IMAGE DOWNLOADED',f)
            news_title_ = news.find('div',class_='card-content')
            news_title = news_title_.find('h2',class_='entry-title').text.strip()
            print('[Inc42Scrapper]::::::::::: NEWS_Title',news_title)

            news_url = news_link
            #parsing the news-link
            try:
                r = requests.get(news_url,headers=get_request_headers())
                print ('[Inc42Scrapper] :: fetching data from TEAMS url: ', news_url)
                if not r.status_code == 200:
                    print ("[Inc42Scrapper] :: Failed to get " \
                        "content of url: %s" % news_url)
                    return
                html_doc = r.content
                soup = BeautifulSoup(html_doc, 'html.parser')
                div1_=soup.find('div',class_='site-content')
                div5_ = div1_.find('div',class_='meta-wrapper single-meta-wrapper single-meta-wrapper-top entry-meta clearfix') 
                div7_ =div5_.find('div',class_='post-meta large-7 medium-6 small-12 columns')
                #print(div7_)
                news_author = div7_.find('div',class_='author-name large').text.strip()
                #news-author
                print('[Inc42Scrapper]::::::::::: NEWS_Author_name',news_author)
                news_date = div5_.find('div',class_='date').text.strip()
                #news_date
                print('[Inc42Scrapper]::::::::::: NEWS_date',news_date)
                #news-subtitle
                date_object = datetime.datetime.strptime(news_date, "%b %d, %Y")
                #print("date_object =", date_object)
                date = str(date_object)
                datetime_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
                print(datetime_obj)
                datetime_obj_utc = datetime_obj.replace(tzinfo=timezone('UTC'))
                UTC_blog_date=datetime_obj_utc.strftime("%Y-%m-%d %H:%M:%S %Z%z")

                print('BlOG________________DATE',UTC_blog_date)
                news_subtitles = div1_.find('div',class_='single-post-summary').text.strip()
                print('[Inc42Scrapper]::::::::::: NEWS_subtitles',news_subtitles)
                #news-description
                news_text = div1_.find('div',class_='entry-content clearfix').text.strip()
                print('[Inc42Scrapper]::::::::::: NEWS_Description',news_text)
                
            except AttributeError:
                print('this post dont have author')
                news_author =''
                print('[Inc42Scrapper]::::::::::: NEWS_author',news_date)
                #news-subtitle
                news_subtitles = div1_.find('div',class_='single-post-summary').text.strip()
                print('[Inc42Scrapper]::::::::::: NEWS_subtitles',news_subtitles)
                #news-description
                news_text = div1_.find('div',class_='entry-content clearfix').text.strip()
                print('[Inc42Scrapper]::::::::::: NEWS_Description',news_text)
            

            except Exception as exp:
                print ('[Inc42Scrapper] :: run() :: Got exception at fetching data from INC42 post url: %s'\
                    % exp)
                print(traceback.format_exc())

            self.parse_to_json(news_link, news_title, news_subtitles, News_Image_url, news_author, news_date,blog_path, news_text)

        except Exception as exp:
            print ('[Inc42Scrapper] :: run() :: Got exception at fetching data from INC42 Homepage: %s'\
                % exp)
            print(traceback.format_exc())
    def parse_to_json(self,news_link,news_title,news_subtitles,News_Image,news_author,news_date,news_text,blog_path):
        try:
            base_directory = 'C:/Users/lenovo/Desktop/scholarsbook_scrappers_data/ESPN.in/cricket/'
            data = {
                "blog_path":blog_path,
                "news_url":news_link,
                "news_title":news_title,
                "news_subtitle":news_subtitles,
                "New_Image_name":News_Image,
                "news_date":news_date,
                "news_author":news_author,
                "news_text":news_text
                }
            with open('blog_post.json', 'w') as json_file:
                print('json file is created')
                json.dump(data, json_file)
            os.chdir(base_directory)

        except Exception as exp:
            print ('[POSTSCRAPPER] :: run() :: Got exception at HOME NEWS_url: %s'\
            % exp)
            print(traceback.format_exc())

if __name__ == "__main__":
    Inc42scrapper = Inc42Scrapper()
    Inc42scrapper.run()
            
                    
            