import datetime
import json
import os
import random
import re
import string
import tempfile
import time
import traceback

from datetime import date, time

import requests

import pandas as pd
from bs4 import BeautifulSoup, NavigableString, Tag
from db import Mdb
from pytz import timezone
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from utils import get_request_headers, scraper_csv_write, sleep_scrapper


class AnyWebsiteScraper:

    def __init__(self):
        self.mdb = Mdb()

    def run(self):
        try:

            url = 'https://www.countryliving.com/food-drinks/' #input("Enter url to be scrapped: ")
            # url1 = url.split('/')
            # print(url1)
            # #url2 = url1.split('/').pop()
            # url2 = url1[3]
            
            

            print ('[AnyWebsiteScraper] :: fetching data from url: ', url)
            r = requests.get(url, headers=get_request_headers())
            if not r.status_code == 200:
                print ("[AnyWebsiteScraper] :: Failed to get " \
                        "content of url: %s" % url)
                return
            html_doc = r.content
            soup = BeautifulSoup(html_doc, 'html.parser')
            div22 = soup.find('div',class_='site-content')
            div11= soup.find('div',class_='feed feed-grid')
            for div33 in div11.find_all('div',class_='simple-item'):
                self.scrap_result_row(div33)
            sleep_scrapper('AnyWebsiteScraper')
     #infinite scrolling logic start
                        #infinitescrollingUrl ##################### Input here 
            base_url = 'https://www.countryliving.com/ajax/infiniteload/?id=34aae02d-c035-47e5-95c5-b87ba30c1dd8&class=CoreModels%5Csections%5CSectionModel&viewset=section&cachebuster=&page='

            for i in range(2, 100, 1):
                url = base_url + str(i)
                
                print ('[AnyWebsiteScraper] :: fetching data from url: ', url)
                r = requests.get(url, headers=get_request_headers())
                if not r.status_code == 200:
                    print ("[AnyWebsiteScraper] :: Failed to get " \
                        "content of url: %s" % url)
                    return
                html_doc = r.content
                soup = BeautifulSoup(html_doc, 'html.parser')
                div22 = soup.find('div',class_='site-content')
                div11= soup.find('div',class_='feed feed-grid')
                for div33 in div11.find_all('div',class_='simple-item'):
                    self.scrap_result_row(div33)
                sleep_scrapper('AnyWebsiteScraper')

    #Infinite Scroll Logic Ends            
        except Exception as exp:
            print ('[AnyWebsiteScraper] :: run() :: Got exception: %s'\
                  % exp)
            print(traceback.format_exc())        
                   
            
            

        

    def scrap_result_row(self, div33):

        try:
            

            #blog author name
            #blog_link
            div44=div33.find('a',{'class':'simple-item-image item-image'})
            link=div33.find('a',{'class':'simple-item-image item-image'})['href']
            #making blog folder starts here
            #blog_website
            prefix='https://www.countryliving.com'
            blog_link = prefix + link
            blog_name=link.split('/')
            file1=(blog_name[3])
            blog1_name=blog_name
            directory = file1
            parent_dir = '/home/soumya/Documents/scrappeddata/Food-Drink' #input("Enter the folder path where to store data: ") 
            blog_path = os.path.join(parent_dir,directory)
            os.mkdir(blog_path)         
            print('[AnyWebsiteScraper] :: blog_Folder has been created:',blog_path)
            path1=os.chdir(blog_path)

            #for blog_posting_date
            div66=div33.find('div',class_='simple-item-metadata')
            blog_date=div66.find('div',class_='publish-date simple-item-publish-date js-date').text.strip()
            date_string = blog_date
            # date_time_obj = datetime.datetime.strptime(date_time_str, '%b %d %Y %I:%M%p')
            print("date_string =", date_string)
            print("type of date_string =", type(date_string))
            date_object = datetime.datetime.strptime(date_string, "%b %d, %Y")
            print("date_object =", date_object)
            date = str(date_object)
            print("type of date_object =", type(date_object))
            datetime_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            datetime_obj_utc = datetime_obj.replace(tzinfo=timezone('UTC'))
            UTC_blog_date=datetime_obj_utc.strftime("%Y-%m-%d %H:%M:%S %Z%z")
            print('[AnyWebsiteScraper] :: blog_date:',UTC_blog_date)
            #blog_picture
            picture=div44.find('span')['data-lqip']
            picture1=picture.split('?')
            blog_picture=(picture1[0])
            blog_image_name=blog_picture.split('/').pop()
            print(blog_image_name)
            raw1_media=requests.get(blog_picture , stream=True)
            with open(blog_image_name,"wb") as f:
                f.write(raw1_media.content)
                print('IMAGE DOWNLOADED',f)
            print('current working directory',os.getcwd())
            path=os.getcwd()
            directory=blog_image_name
            path = os.path.join(path,directory)
            image_list=[]
            video_list=[]
            pdf_list=[]
            blog_author = '' 
            blog_subtitle = ''
            
                
            image_list.append(path)
            print('[AnyWebsiteBlogScraper] :: blog_description  :: BLOG_media:',path)
            #for blog_title
            blog_title=div33.find('a',class_='simple-item-title item-title').text.strip()
            print('[AnyWebsiteScraper] :: blog_title:',blog_title)
            #for blog_short_desc
            blog_short_desc=div33.find('div',class_='simple-item-dek item-dek').text.strip()
            blog_subtitle = blog_short_desc
            print('[AnyWebsiteScraper] :: blog_short_desc:',blog_subtitle)
            #Making blog folder ends here
            #recursively getting all blog data 
            print('[AnyWebsiteScraper] :: blog_link:',blog_link)
            try:
                url = blog_link
                print ('[AnyWebsiteScraper] :: fetching data from blog_link: ', url)
                r = requests.get(url, headers=get_request_headers())
                print(r,'rrrrrr')
                if not r.status_code == 200:
                    print ("[AnyWebsiteScraper] :: Failed to get " \
                        "content of url: %s" % url)
                    return
                html_doc = r.content
                soup = BeautifulSoup(html_doc, 'html.parser')
                div111=soup.find('div',class_='site-content')
                #extratcion rule for normal blogs
                print('Normal blog:::::::.............')
                #blog_author name
                
                author=div111.find('div',class_='content-info-metadata')
                auth1=author.find('div',class_='byline-with-image')
                blog_author=auth1.find('div',class_='byline').text.strip()
                blog_author1 = (blog_author)
                print('[AnyWebsiteBlogScraper] :: blog_author:',blog_author1)
                div2222=div111.find('div',class_='content-container standard-container')
                if(div2222): 
                    blog_description=''
                    div333=div2222.find('div',class_='standard-body')
                    div8899=div333.find('div',class_='content-lede-image-wrap aspect-ratio-freeform')
                    div8889=div333.find('div',class_='article-body-content standard-body-content')
                    blog_description=div8889.find('p',class_='body-text').text.strip()
                    blog_desc = blog_description + '\n' + blog_author1
                    print('[AnyWebsiteBlogScraper] :: blog_description:', blog_desc.encode('utf-8'))
                else:
                    pass
                try:
                #extraction rule for slides container blogs
                    blog_description=''
                    div777=div111.find('div',class_='slideshow-outer')
                    div456=div777.find('div',class_='slideshow-lede active')
                    blog_description=div456.find('div',class_='slideshow-desktop-dek').text.strip()
                    blog_desc = blog_description + '\n' + blog_author1
                    print('[AnyWebsiteBlogScraper] :: blog_description:',blog_desc.encode('utf-8'))
                except:
                    pass
                if(div777):
                    print('Slides Blog:::::::::')
                    #self.Slide_blog(div777)
                
                
            except AttributeError as e:
                print ('[AnyWebsiteScraper] :: run() :: Got exception: %s'\
                  % e) 
                blog_author = ''
                url = blog_link
                print ('[AnyWebsiteScraper] :: fetching data from blog_link: ', url)
                r = requests.get(url, headers=get_request_headers())
                print(r,'rrrrrr')
                if not r.status_code == 200:
                    print ("[AnyWebsiteScraper] :: Failed to get " \
                        "content of url: %s" % url)
                    return
                html_doc = r.content
                soup = BeautifulSoup(html_doc, 'html.parser')
                div111=soup.find('div',class_='site-content')
                    #extratcion rule for normal blogs
                print('Normal blog:::::::.............')
                    #blog_author name
                
            
                blog_author1 = (blog_author)
                print('[AnyWebsiteBlogScraper] :: blog_author:',blog_author1)
                div2222=div111.find('div',class_='content-container standard-container')
                if(div2222): 
                    blog_description=''
                    div333=div2222.find('div',class_='standard-body')
                    div8899=div333.find('div',class_='content-lede-image-wrap aspect-ratio-freeform')
                    div8889=div333.find('div',class_='article-body-content standard-body-content')
                    blog_description=div8889.find('p',class_='body-text').text.strip()
                    blog_desc = blog_description + '\n' + blog_author1
                    print('[AnyWebsiteBlogScraper] :: blog_description:', blog_desc.encode('utf-8'))
                else:
                    pass
                try:
                    #extraction rule for slides container blogs
                    blog_description=''
                    div777=div111.find('div',class_='slideshow-outer')
                    div456=div777.find('div',class_='slideshow-lede active')
                    blog_description=div456.find('div',class_='slideshow-desktop-dek').text.strip()
                    blog_desc = blog_description + '\n' + blog_author1
                    print('[AnyWebsiteBlogScraper] :: blog_description:',blog_desc.encode('utf-8'))
                except:
                    pass
                if(div777):
                    print('Slides Blog:::::::::')

     

                data = {
                    "blog_title":blog_title , 
                    "blog_sub_title":blog_subtitle,
                    "blog_author":blog_author,
                    "blog_date":UTC_blog_date,
                    "blog_url":blog_link,
                    "blog_text":blog_description,
                    "blog_storage_path":blog_path,
                    "blog_image_name":blog_image_name,
                    "blog_image_list":image_list,
                    "blog_video_list":video_list,
                    "blog_pdf_list":pdf_list
                   }
        
                with open('personal.json', 'w') as json_file:
                    print('json file is created')
                    json.dump(data, json_file)
                
            data = {
                "blog_title":blog_title , 
                "blog_sub_title":blog_subtitle,
                "blog_author":blog_author,
                "blog_date":UTC_blog_date,
                "blog_url":blog_link,
                "blog_text":blog_description,
                "blog_storage_path":blog_path,
                "blog_image_name":blog_image_name,
                "blog_image_list":image_list,
                "blog_video_list":video_list,
                "blog_pdf_list":pdf_list
                }
        
            with open('personal.json', 'w') as json_file:
                 print('json file is created')
                 json.dump(data, json_file)
            
        # except Exception as exp:
        #     print ('[AnyWebsiteScraper] :: scrap_result_row() :: ' \
        #           'Got exception : %s' % exp)
        #     print(traceback.format_exc())
        except UnicodeEncodeError as exp:
                print ('[AnyWebsiteScraper] :: run() :: Got exception: %s'\
                  % exp)
                blog_subtitle.encode('utf-8')
                
                url = blog_link
                print ('[AnyWebsiteScraper] :: fetching data from blog_link: ', url)
                r = requests.get(url, headers=get_request_headers())
                print(r,'rrrrrr')
                if not r.status_code == 200:
                    print ("[AnyWebsiteScraper] :: Failed to get " \
                         "content of url: %s" % url)
                    return
                html_doc = r.content
                soup = BeautifulSoup(html_doc, 'html.parser')
                div111=soup.find('div',class_='site-content')
                    #extratcion rule for normal blogs
                print('Normal blog:::::::.............')
                    #blog_author name
                
                author=div111.find('div',class_='content-info-metadata')
                auth1=author.find('div',class_='byline-with-image')
                blog_author=auth1.find('div',class_='byline').text.strip()
                blog_author1 = (blog_author)
                print('[AnyWebsiteBlogScraper] :: blog_author:',blog_author1)
                div2222=div111.find('div',class_='content-container standard-container')
                if(div2222): 
                    
                    div333=div2222.find('div',class_='standard-body')
                    div8899=div333.find('div',class_='content-lede-image-wrap aspect-ratio-freeform')
                    div8889=div333.find('div',class_='article-body-content standard-body-content')
                    blog_description=div8889.find('p',class_='body-text').text.strip()
                    blog_desc = blog_description + '\n' + blog_author1
                    print('[AnyWebsiteBlogScraper] :: blog_description:', blog_desc.encode('utf-8'))
                else:
                    pass
                try:
                    #extraction rule for slides container blogs
                    
                    div777=div111.find('div',class_='slideshow-outer')
                    div456=div777.find('div',class_='slideshow-lede active')
                    blog_description=div456.find('div',class_='slideshow-desktop-dek').text.strip()
                    blog_desc = blog_description + '\n' + blog_author1
                    print('[AnyWebsiteBlogScraper] :: blog_description:',blog_desc.encode('utf-8'))
                except:
                    pass
                if(div777):
                    print('Slides Blog:::::::::')

     

                data = {
                "blog_title":blog_title , 
                "blog_sub_title":blog_subtitle,
                "blog_author":blog_author,
                "blog_date":UTC_blog_date,
                "blog_url":blog_link,
                "blog_text":blog_description,
                "blog_storage_path":blog_path,
                "blog_image_name":blog_image_name,
                "blog_image_list":image_list,
                "blog_video_list":video_list,
                "blog_pdf_list":pdf_list
                }
        
                with open('personal.json', 'w') as json_file:
                     print('json file is created')
                     json.dump(data, json_file)
        

    
    # def Nomral_blog(self,div333):
                
                


    def Slide_blog(self,div777):
                print('Slide Blog Function')
                try:
                    #blog_slides_content
                    div888=div777.find('div',class_='slide-container')
                    
                    for div999 in div888.find_all('div',class_='slideshow-slide slideshow-slide-portrait slideshow-slide-image loaded'):
                        self.slide_content(div999) 
                except Exception as exp:
                    print('[AnyWebsiteBlogScraper] :: run() :: Got exception: %s'\
                    % exp)
                    print(traceback.format_exc())

    def slide_content(self,div999):
        print('I am Slide Content')
        try:
            #blog_media_starts_here
           image=''
           _media=div999.find('picture',class_='zoomable')
           slice_media=_media.find('img',class_='lazyimage lazyload')
           Slice_media=(slice_media)['data-src']
           file=Slice_media.split('?')

           image_filename=(file[0])
           image_name=image_filename.split('/').pop()
           raw_media=requests.get(image_filename , stream=True)
           with open(image_name,"wb") as f:
                f.write(raw_media.content)
           path=os.getcwd()
           directory=image_name
           slide_path = os.path.join(path,directory)      
           print('[AnyWebsiteBlogScraper] :: blog_description  :: blog_slide_media:',slide_path)
           #slide_title
           slide_title=div999.find('div',class_='slideshow-slide-hed').text.strip()
           slide_desc=div999.find('div',class_='slideshow-slide-dek').text.strip()
           print('[AnyWebsiteBlogScraper] :: blog_description  :: blog_slide_title:',slide_title)
           print('[AnyWebsiteBlogScraper] :: blog_description  :: blog_slide_desc:',slide_desc)
        except Exception as exp:
            print('[AnyWebsiteBlogScraper] :: run() :: Got exception: %s'\
                 % exp)
            print(traceback.format_exc())

if __name__ == '__main__':

    any_blog_data = AnyWebsiteScraper()
    any_blog_data.run()
