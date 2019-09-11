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
class ESPNScraper:
    def __init__(self):
        self.mdb = Mdb()
    
    def run(self):
        try:
            #Teams news scrapping 'https://www.espn.in/cricket/team/_/id/1/england',
                                #   'https://www.espn.in/cricket/team/_/id/2/australia',
                                #   'https://www.espn.in/cricket/team/_/id/3/south-africa',
                                #   'https://www.espn.in/cricket/team/_/id/4/west-indies',
                                #   'https://www.espn.in/cricket/team/_/id/5/new-zealand',
                                #   'https://www.espn.in/cricket/team/_/id/6/india',
                                #   'https://www.espn.in/cricket/team/_/id/7/pakistan',
                                #   'https://www.espn.in/cricket/team/_/id/8/sri-lanka',
                                #   'https://www.espn.in/cricket/team/_/id/9/zimbabwe',
                                #   'https://www.espn.in/cricket/team/_/id/25/bangladesh/',
            cricketTeams_URLs = [ 
                                  'http://www.espn.in/cricket/team/_/id/1/england',
                                  'http://www.espn.in/cricket/team/_/id/2/australia',
                                  'http://www.espn.in/cricket/team/_/id/3/south-africa',
                                  'http://www.espn.in/cricket/team/_/id/4/west-indies',
                                  'http://www.espn.in/cricket/team/_/id/5/new-zealand',
                                  'http://www.espn.in/cricket/team/_/id/6/india',
                                  'http://www.espn.in/cricket/team/_/id/7/pakistan',
                                  'http://www.espn.in/cricket/team/_/id/8/sri-lanka',
                                  'http://www.espn.in/cricket/team/_/id/9/zimbabwe',
                                  'http://www.espn.in/cricket/team/_/id/25/bangladesh/'                              
                                 ]
            
            for url in cricketTeams_URLs:
                print("PART_________________________________A")
                print ('[ESPNScrapper] :: fetching data from TEAMS url: ', url)
                r = requests.get(url, headers=get_request_headers())
                if not r.status_code == 200:
                    print ("[ESPNScrapper] :: Failed to get " \
                        "content of url: %s" % url)
                    return
                html_doc = r.content
                soup = BeautifulSoup(html_doc, 'html.parser')
                sect1= soup.find('section', id='pane-main')
                sect11= sect1.find('section',id='main-container')
                sect2= sect11.find('section',id='news-feed')
                news_feed_list = sect2.find('div',class_='container')
                section_news = news_feed_list.find_all("article", {"class":"news-feed-item news-feed-story-package"})
                Headlines = news_feed_list.find_all("article", {"class":"news-feed-item news-feed-story-package is-headline"})
                team_parsed_urls = []
                for news in Headlines:
                    print("PART______________________________A.A")
                    news_ = news.find("a",{"class":"story-link"})
                    if(news):
                        news_url= (news_)['data-popup-href']
                        #self.scrape_post_content(news_url)
                        team_parsed_urls.append(news_url)
                                
                for news in section_news:
                    print("PART______________________________A.B")
                    print('You are now scrapping regular news fro webpage !!.. ')
                    news_ = news.find("a",{"class":"story-link"})
                    if(news):
                        news_url= (news_)['data-popup-href']
                        print('[ESPNScrapper] :: section news URL: ', news_url)
                        #self.scrape_post_content(news_url)
                        team_parsed_urls.append(news_url)
                
                infnite_scroll_url = 'https://secure.espn.com/core/minifeed?render=true&partial=newsfeed&limit=20&xhr=1&template=clubhouse&headlinestack=true&site=espn&lang=en&region=in&sport=cricket&pubkey=cricket-clubhouse&insider=false&device=desktop&country=in&lang=en&region=in&site=espn&edition-host=espn.in&site-type=full&userab=0&offset=' 
                ur_l = url.split('/')
                print('url to be scrolled infinite',ur_l)
                team = '&team=' + ur_l[7]
                for i in range(0,100,25):
                    scroll_url = infnite_scroll_url + str(i) + team
                    print("PART____________AUTO-SCROLL______________________A.C")
                    print ('[ESPNScrapper] :: fetching data from infinite-url: ',scroll_url)
                    try:
                        raw_json = requests.get(scroll_url).text
                        data = json.loads(raw_json)
                        qw = (data['content']['html']['items'][0]['html'])
                        for data in data['content']['html']['items']:
                            qw = data['html']
                            try:

                                qwe = json.dumps(qw)
                                soup = BeautifulSoup(qwe, 'html.parser')
                                section_ = soup.find("a")['data-popup-href']
                                print(section_)
                                sect = section_.replace('\\"','')
                                if re.search('clip',sect):
                                    print("NEWS only contains video, no text , no image , so skipping this News")
                                else:
                                    team_parsed_urls.append(sect)
                                    self.scrape_post_content(sect)
                                
                            except Exception as exp:
                                print ('[ESPNscrapper] :: run() :: Got exception at fetching data from TEAMSurl: %s'\
                                    % exp)
                                print(traceback.format_exc())
                    
                    except Exception as exp:
                        print ('[ESPNscrapper] :: run() :: Got exception at fetching data from TEAMSurl: %s'\
                            % exp)
                        print(traceback.format_exc())       
                    sleep_scrapper('ESPNScrapper')
                sleep_scrapper('ESPNScrapper')
                    
                base_url = 'https://www.espn.in/cricket/'
                parent_fol = base_url.split('/')
                print(parent_fol)
                print("PART_______________________________B")
                print ('[ESPNScrapper] :: fetching data from BASE Url: ', base_url)
                ree = requests.get(base_url, headers=get_request_headers())
                if not ree.status_code == 200:
                    print ("[ESPNScrapper] :: Failed to get " \
                        "content of url: %s" % base_url)
                    return
                html_doc = ree.content
                soup = BeautifulSoup(html_doc, 'html.parser')
                col2_feed = soup.find('section',class_='col-two contentFeed')
                contentf= col2_feed.find_all("section",{"class":"contentItem"})
                for content in contentf:
                    print('contentfeedsections')
                    self.scrape_sports(content,cricketTeams_URLs)
                contentf= col2_feed.find_all("article",{"class":"contentItem"})
                for contentfeed in contentf:
                    print('contentfeedARTICLES')
                    self.scrape_sports(contentfeed,cricketTeams_URLs)
                    #scrape only 26 posts of the starting webpage
            
                #Infinite loading URL 
                infinite_url = 'https://onefeed.fan.api.espn.com/apis/v3/cached/contentEngine/oneFeed/leagues/cricket?source=ESPN.com%2B-%2BFAM&showfc=true&region=in&limit=15&lang=en&authorizedNetworks=espn_free&editionKey=espnin-en&device=desktop&pubkey=espncricinfo-en-in-cricket-index&isPremium=true&locale=in&featureFlags=expandAthlete&featureFlags=mmaGB&offset='
                #for 10 times scrolling
                for i in range(10,100,15):
                    scroll_url = infinite_url + str(i)
                    print ('[ESPNScrapper] :: fetching data from infinite-url: ',scroll_url)

                    r = requests.get(scroll_url, headers=get_request_headers())
                    try:
                        raw_json = requests.get(scroll_url).text
                        dataa = json.loads(raw_json)
                        for data in dataa['feed']:
                            qw = (data['data']['now'][0])
                            try:
                                keys = sorted(qw.items())
                                result = [(key, value) for key, value in keys if key.startswith("links")]
                                result11 = result[0]
                                result33 = list(result11)
                                reo = result33[1]
                                scroll_news_url = reo['web']['href']
                                print('FETCHING post from scroll URL')
                                self.scrape_post_content(scroll_news_url)
                                
                            except Exception as exp:
                                print ('[ESPNscrapper] :: run() :: Got exception at fetching data from TEAMSurl: %s'\
                                    % exp)
                                print(traceback.format_exc())
                    
                    except Exception as exp:
                        print ('[ESPNscrapper] :: run() :: Got exception at fetching data from TEAMSurl: %s'\
                            % exp)
                        print(traceback.format_exc()) 
                
                sleep_scrapper('ESPNScrapper')


        except Exception as exp:
            print ('[ESPNscrapper] :: run() :: Got exception at fetching data from TEAMSurl: %s'\
                  % exp)
            print(traceback.format_exc())


    def scrape_home_infinite_articles(self,contentfeed,cricketTeams_URLs):
        try:
            without_clickable_header_section = contentfeed.findall("section",{"class":"contentItem__content contentItem__content--story"})
            if(without_clickable_header_section):
                 for i in without_clickable_header_section:
                    try:
                        news_ = i.find("a",{"class":"contentItem__padding contentItem__padding--border"})
                        news_url= (news_)['href']
                        print('SCRAPPING DATA FROM NON-CLICKABLE HEADER SECTIONS at INFINITE SCROll')
                        self.scrape_post_content(news_url)
                    except Exception as exp:
                        print ('[ESPNscrapper] :: run() :: Got exception at fetching data from HOME PAGE INFINITE ARTIClES: %s'\
                            % exp)
                        print(traceback.format_exc())
    
            
        except Exception as exp:
            print ('[ESPNscrapper] :: run() :: Got exception at fetching data from HOME PAGE INFINITE ARTIClES: %s'\
                     % exp)
            print(traceback.format_exc())
    

    def scrape_post_content(self,news_url):
        try:
            print('feTCHNg data fromm post url')
            print ('[ESPNScrapper] :: fetching data from Headlines post url: ', news_url)
                                
            r = requests.get(news_url, headers=get_request_headers())
            if not r.status_code == 200:
                print ("[ESPNScrapper] :: Headline Posts URL Failed to get " \
                    "content of post_url: %s" % news_url)
                return
            html_doc = r.content
            soup = BeautifulSoup(html_doc, 'html.parser')
            sect1= soup.find('section', id='pane-main')
            sect11= sect1.find('section',id='main-container')
            sect111=sect11.find("div",{"class":"main-content"})
            sect2= sect111.find('section',id='article-feed')
            div555 = sect2.find('div',class_='container')
            article_header = div555.find('header',class_='article-header').text.strip()
            art__ =div555.find('div',class_='article-body')
            art_ = art__.find('div',class_='article-meta')
            POST_DATE=art_.find('span',class_='timestamp')
            
            POST_LOCAL_TIME = (POST_DATE).text.strip()
            print('[ESPNScrapper] :: fetching data from Post :: POST_LOCAL_TIME : ', POST_LOCAL_TIME)
            
            POST_UTC_DATE=(POST_DATE)['data-date']
            print('[ESPNScrapper] :: fetching data from Post :: UTC TIMESTAMP : ', POST_UTC_DATE)
            utc_date = POST_UTC_DATE.split('T')
            utc_date1 = utc_date[1].split(':')
            print('utc_date1',utc_date1)
            fold = utc_date1[0] + ' ' + utc_date1[1] + ' ' + utc_date1[2]
            utc = utc_date[0] + ' ' + fold
            print('folder name',utc)
            directory = utc
            parent_dir = 'C:/Users/lenovo/Desktop/scholarsbook_scrappers_data/ESPN.in/cricket/' #input("Enter the folder path where to store data: ") 
            blog_path = os.path.join(parent_dir,directory)
            
            os.mkdir(blog_path)         
            print('[AnyWebsiteScraper] :: blog_Folder has been created:',blog_path)
            path1=os.chdir(blog_path)
            print('currentpath',os.getcwd())

            print('[ESPNScrapper] :: fetching data from Post :: header : ', article_header)                   
            img1 = div555.find('figure',class_='article-figure dim16x9')
            pic__=''
            if(img1):

                img2 = img1.find('div',class_='img-wrap')
                pic__ = img2.find('source')['srcset']
                print('[ESPNScrapper] :: fetching data from Post :: Image_URL : ', pic__)
                pic_ = pic__.split('?').pop()
                pic11 = pic_.split('2F').pop()
                pic111 = pic11.split('&')
                image_name = (pic111[0])
                raw1_media=requests.get(pic__ , stream=True)
                with open(image_name,"wb") as f:
                    f.write(raw1_media.content)
                    print('IMAGE DOWNLOADED',f)
            else:
                print('IT a video post.......')
                aside = art__.find('aside',class_='inline inline-photo full')
                if(aside):
                    aside_ = aside.find('figure')
                    videoPostImage = aside_.find('source')['data-srcset']
                    print('[ESPNScrapper] :: fetching data from Post :: Image_URL : ', videoPostImage)
                    pic_ = pic__.split('?').pop()
                    pic11 = pic_.split('2F').pop()
                    pic111 = pic11.split('&')
                    image_name = (pic111[0])
                    raw1_media=requests.get(videoPostImage , stream=True)
                    with open(image_name,"wb") as f:
                       f.write(raw1_media.content)
                       print('IMAGE DOWNLOADED',f)
                else:
                    print('This post is a live report . Sorry not HAVE any image')

                
           
            post_author=art_.find('ul',class_='authors').text.strip()
            print('[ESPNScrapper] :: fetching data from Post :: POST AUTHOR : ', post_author)
            po= (art__).text.strip()
            print('[ESPNScrapper] :: fetching data from Post :: POST TEXT : ', po)
            self.parse_data_to_json(news_url, article_header, pic__, POST_UTC_DATE, POST_LOCAL_TIME, post_author, po)
            
        except Exception as exp:
            print ('[POSTSCRAPPER] :: run() :: Got exception at news_url: %s'\
            % exp)
            print(traceback.format_exc())

    
    def scrape_sports(self, contentfeed, cricketTeams_URLs):
        try:
            home_page_section_urls = []
            post_header = contentfeed.find('header',class_='contentItem__header')
            section_heading_url = post_header.find('a' , class_='contentItem__header__wrapper')['href']
            if(section_heading_url):
                try:

                    
                    
                         
                    if not section_heading_url.startswith('http'):
                        print('raw_-------url',section_heading_url)
                        url = 'https://www.espn.in/cricket/'
                        _url = url.split('/')
                        _1url=_url[0]
                        _2url=_url[2]
                        _3url='//'
                        base_url = _1url + _3url + _2url
                        post_url = base_url + section_heading_url
                        section_heading_url = post_url
                    if section_heading_url not in cricketTeams_URLs: 
                        home_page_section_urls.append(section_heading_url)
                        print("UNQUE URL AT HOME IS SCRAPPING")
                        self.scrape_home_sections(section_heading_url)
            

                except Exception as exp:
                    print ('[ESPNscrapper] :: run() :: Got exception at fetching data from Home PAGE: %s'\
                        % exp)
                    print(traceback.format_exc())
            else:
                pass

            #sections dont have Header , 
            without_clickable_header_section = contentfeed.findall("section",{"class":"contentItem__content contentItem__content--story"})
            if(without_clickable_header_section):
                 for i in without_clickable_header_section:
                    try:
                        news_ = i.find("a",{"class":"contentItem__padding contentItem__padding--border"})
                        news_url= (news_)['href']
                        print('SCRAPPING DATA FROM NON-CLICKABLE HEADER SECTIONS')
                        self.scrape_post_content(news_url)
                    except Exception as exp:
                        print ('[ESPNscrapper] :: run() :: Got exception at fetching data from HOME PAGE NON-CLICKABLE HEADER: %s'\
                            % exp)
                        print(traceback.format_exc())
    
            
        except Exception as exp:
            print ('[ESPNscrapper] :: run() :: Got exception at fetching data from HOME PAGE: %s'\
                     % exp)
            print(traceback.format_exc())
    
    def scrape_home_sections(self, section_heading_url):
        try:
            print('[ESPNscrapper] :: fetching data from section url :', section_heading_url)
            r = requests.get(section_heading_url, headers=get_request_headers())
            if not r.status_code == 200:
                print ("[ESPNScrapper] :: Failed to get " \
                        "content of url: %s" % section_heading_url)
                return
            html_doc = r.content
            soup = BeautifulSoup(html_doc, 'html.parser')
            col2_feed = soup.find('section',class_='col-two contentFeed')
            contentf= col2_feed.find_all("section",{"class":"contentItem"})
            for contentfeed in contentf:
                
                div_content = contentfeed.find_all('section',class_='contentItem__content contentItem__content--story has-image has-video contentItem__content--collection')
                if(div_content):

                    for post in div_content:
                        news_1 = post.find("a", {"class":"contentItem__padding contentItem__padding--border"})
                        news_url = (news_1)['href']
                        print(news_url)
                       
                        self.scrape_section_posts(news_url)
                else:
                    print('section has video NEWS only !!')
            contentf= col2_feed.find_all("article",{"class":"contentItem"})
            for contentfeed in contentf:
                
                div_content = contentfeed.find_all('section',class_='contentItem__content contentItem__content--story has-image has-video contentItem__content--collection')
                if(div_content):
                    print('now scrapping posts from articles in Home_Sections_scrapping')
                    for post in div_content:
                        news_1 = post.find("a", {"class":"contentItem__padding contentItem__padding--border"})
                        news_url = (news_1)['href']
                        print(news_url)
                       
                        self.scrape_section_posts(news_url)
                else:
                    print('section has video NEWS only !!')

        except AttributeError as e:
            print('THIS Section is scraped already !!!.....Sorry, cant get data: %s')
            print ('[ESPNscrapper] :: run() :: Got exception at fetching data from section url: %s'\
                     % e)
            print(traceback.format_exc()) 
        
        except TypeError as er:
            print('THIS Section is For Viewing Ads !!: %s')

            print ('[ESPNscrapper] :: run() :: Got exception at fetching data from section url: %s'\
                     % er)
            print(traceback.format_exc()) 
        
        
        except Exception as exp:
            print ('[ESPNscrapper] :: run() :: Got exception at fetching data from section url: %s'\
                     % exp)
            print(traceback.format_exc()) 


    def scrape_section_posts(self,news_url):
        try:
            if not news_url.startswith('http'):
                url = 'https://www.espn.in/cricket/'
                _url = url.split('/')
                _1url=_url[0]
                _2url=_url[2]
                _3url='//'
                base_url = _1url + _3url + _2url
                post_url = base_url + news_url
                news_url = post_url
            print('home secton post url')
            print ('[ESPNHOMEScrapper] :: fetching data from HOME POST url: ', news_url)
                                
            r = requests.get(news_url, headers=get_request_headers())
            if not r.status_code == 200:
                print ("[ESPNHOMEScrapper] ::Posts URL Failed to get " \
                    "content of post_url: %s" % news_url)
                return
            html_doc = r.content
            soup = BeautifulSoup(html_doc, 'html.parser')
            sect1= soup.find('section', id='pane-main')
            sect11= sect1.find('section',id='main-container')
            sect111=sect11.find("div",{"class":"main-content"})
            sect2= sect111.find('section',id='article-feed')
            div555 = sect2.find('div',class_='container')
            article_header = div555.find('header',class_='article-header').text.strip()
            art__ =div555.find('div',class_='article-body')
            art_ = art__.find('div',class_='article-meta')
            POST_DATE=art_.find('span',class_='timestamp')
            POST_UTC_DATE=(POST_DATE)['data-date']
            print('[ESPNScrapper] :: fetching data from Post :: UTC TIMESTAMP : ', POST_UTC_DATE)
            utc_date = POST_UTC_DATE.split('T')
            utc_date1 = utc_date[1].split(':')
            print('utc_date1',utc_date1)
            fold = utc_date1[0] + ' ' + utc_date1[1] + ' ' + utc_date1[2]
            utc = utc_date[0] + ' ' + fold
            print('folder name',utc)
            directory = utc
            parent_dir = 'C:/Users/lenovo/Desktop/scholarsbook_scrappers_data/ESPN.in/cricket/' #input("Enter the folder path where to store data: ") 
            blog_path = os.path.join(parent_dir,directory)
            os.mkdir(blog_path)         
            print('[AnyWebsiteScraper] :: blog_Folder has been created:',blog_path)
            path1=os.chdir(blog_path)
            print('currentpath',os.getcwd())
            print('[ESPNScrapper] :: fetching data from Post :: header : ', article_header)                   
            img1 = div555.find('figure',class_='article-figure dim16x9')
            pic__=''
            if(img1):

                img2 = img1.find('div',class_='img-wrap')
                pic__ = img2.find('source')['srcset']
                pic_ = pic__.split('?').pop()
                pic11 = pic_.split('2F').pop()
                pic111 = pic11.split('&')
                image_name = (pic111[0])
                print('[ESPNScrapper] :: fetching data from Post :: Image_URL : ', pic__)
                raw1_media=requests.get(pic__ , stream=True)
                with open(image_name,"wb") as f:
                    f.write(raw1_media.content)
                    print('IMAGE DOWNLOADED',f)
            else:
                print('IT a video post.......')
                aside = art__.find('aside',class_='inline inline-photo full')
                if(aside):
                    aside_ = aside.find('figure')
                    videoPostImage = aside_.find('source')['data-srcset']
                    raw1_media=requests.get(videoPostImage , stream=True)
                    with open(image_name,"wb") as f:
                        f.write(raw1_media.content)
                        print('IMAGE DOWNLOADED',f)
                    print('[ESPNScrapper] :: fetching data from Post :: Image_URL : ', videoPostImage)
                else:
                    print('This post is a live report . Sorry not HAVE any image')

                
           
            
            
            POST_LOCAL_TIME = (POST_DATE).text.strip()
            print('[ESPNScrapper] :: fetching data from Post :: POST_LOCAL_TIME : ', POST_LOCAL_TIME)
            post_author=art_.find('ul',class_='authors').text.strip()
            print('[ESPNScrapper] :: fetching data from Post :: POST AUTHOR : ', post_author)
            po= (art__).text.strip()
            print('[ESPNScrapper] :: fetching data from Post :: POST TEXT : ', po)
            self.parse_data_to_json(news_url, article_header, pic__, POST_UTC_DATE, POST_LOCAL_TIME, post_author, po)
        except Exception as exp:
            print ('[POSTSCRAPPER] :: run() :: Got exception at HOME NEWS_url: %s'\
            % exp)
            print(traceback.format_exc())
    def parse_data_to_json(self,news_url,article_header,pic__,POST_UTC_DATE,POST_LOCAL_TIME,post_author,po):
        try:
            base_directory = 'C:/Users/lenovo/Desktop/scholarsbook_scrappers_data/ESPN.in/cricket/'
            data = {
                "news_url":news_url,
                "article_header":article_header,
                "post_Image_url": pic__,
                "post_UTC_DATE":POST_UTC_DATE,
                "Post-local_date":POST_LOCAL_TIME,
                "post_author":post_author,
                "post_text":po
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
    espnscrapper = ESPNScraper()
    espnscrapper.run()
                    
                