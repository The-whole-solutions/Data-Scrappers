# Packagename : careers360Scrapper
# Author      : Tanuj Sharma
# Developed_on: 9 sept , 2019 
# website     : https://www.careers360.com
# Parts --> A. parse -> https://engineering.careers360.com/colleges/ranking/2019
#       --> B. parse -> University General Information page. 
#       --> C. parse -> https://www.careers360.com/university/university-name
#       --> D. Search-> for 'click-here' text in general information page
#       --> E. Extract-> website link from this page
#       --> F. search-> website_link/contact webapge 
#       --> G. use_regex-> search entire webpage(F.)for phone number and email regex function   








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
from lxml import html

class Careers360Scrapper:
    def __init__(self):
        self.mdb = Mdb()
    
    def run(self):
        try:
            url = 'https://engineering.careers360.com/colleges/ranking/2019'
            r = requests.get(url, headers=get_request_headers())
            if not r.status_code == 200:
                print ("[Careers360Scrapper] :: Failed to get " \
                    "content of url: %s" % url)
                return
            html_doc = r.content
            soup = BeautifulSoup(html_doc, 'html.parser')
           
            # tree = html.fromstring(html_doc)
            # #x = html.parse(html_doc)
            # college_list = tree.xpath(" /html[1]/body[1]/div[2]/section[1]/div[3]/div[2]/table[1]/tbody")
            # print('colllegelistttttttttttt',college_list)
            # #print('collegesssssssss',college_list)
            # for i in college_list[1:90]:
            #     #  //td[2]/a[1]/text()              #
            #     for row in i.xpath("./tr"):
            #         tds = row.xpath("./td[2]/a[1]/text() ")
            #         print('tdssssssssss',tds)

                
            #print(soup)
            # section_1 = soup.find('section',class_='sectionLayout grayBg rankignMain')
            # print(section_1)
            # #div_1 = section_1.find('div',class_='container')

            # div_2 = soup.find('div',class_='rankingTable clearfix') 
            # print(div_2)
            # table_1 = div_2.find('table',class_='table-striped')
            # tbody = table_1.find('tbody')
            tr = soup.find_all('tr')
            for row in tr:
                self.CollegeList(row)
            sleep_scrapper('Careeers360Scrapper')
                    

        
        except Exception as exp:
            print ('[Careers360Scrapper] :: run() :: Got exception at fetching data from run(): %s'\
                % exp)
            print(traceback.format_exc())
    
    def CollegeList(self,row):
        try:
            td = row.find('td',class_='colgName')
            a  = td.find('a')
            college_general_info_link = a['href']
            college_name = a.text.strip()
            print('[Careers360]: College Name::',college_name)
            if(college_general_info_link):
                self.ParseCollegeGeneralInfo(college_general_info_link)
            
            
        except Exception as exp:
            print ('[Careers360Scrapper] :: run() :: Got exception at fetching data from run(): %s'\
                % exp)
            print(traceback.format_exc())  
    
    def ParseCollegeGeneralInfo(self,url):
        try:
            r = requests.get(url, headers=get_request_headers())
            if not r.status_code == 200:
                print ("[Careers360Scrapper] :: Failed to get " \
                    "content of url: %s" % url)
                return
            html_doc = r.content
            soup = BeautifulSoup(html_doc, 'html.parser')
            tree = html.fromstring(html_doc)
            college_web = tree.xpath("//a[contains(text(),'Click here')]/@href")
            college_website_url = college_web[0]
            div25 = soup.find('div',class_='adrsDetail')
            college_address = div25.find('address').text.strip() 
            print('[Careers360]: Website Url ::',college_website_url)
            print('[Careers360]: College Address::',college_address)
            if(college_website_url):
                self.ParseCollegeWebsite(college_website_url)



        except Exception as exp:
            print ('[Careers360Scrapper] :: run() :: Got exception at fetching data from run(): %s'\
                % exp)
            print(traceback.format_exc())
    
    def ParseCollegeWebsite(self,url):
        try:
            r = requests.get(url, headers=get_request_headers())
            if not r.status_code == 200:
                print ("[Careers360Scrapper] :: Failed to get " \
                    "content of url: %s" % url)
                return
            html_doc = r.content
            htl = html_doc.decode('utf-8')
            soup = BeautifulSoup(html_doc, 'html.parser')
            #print('collegesoup',soup)
            
            rr = re.findall(r'^\{d12} | ^\{+d12}',htl)
            print(rr)

        
        except Exception as exp:
            print ('[Careers360Scrapper] :: run() :: Got exception at fetching data from run(): %s'\
                % exp)
            print(traceback.format_exc())


if __name__ == "__main__":
    career360  = Careers360Scrapper()
    career360.run()